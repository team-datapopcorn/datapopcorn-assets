"""TabPFN-2 vs XGBoost benchmark (CPU, Apple M4 sandbox).
Part A: 6 small public datasets, 5 random 70/30 splits.
Part B: learning curve on adult (cls) and california housing (reg), n_train in {100,300,1000,3000}, fixed 2000 test rows, 3 seeds.
Results appended row by row to results.csv.
"""
import os, sys, time, warnings, csv
os.environ.setdefault("TABPFN_ALLOW_CPU_LARGE_DATASET", "1")
warnings.filterwarnings("ignore")
import numpy as np, pandas as pd
import optuna, xgboost as xgb
from sklearn.datasets import load_breast_cancer, load_diabetes, fetch_openml, fetch_california_housing
from sklearn.model_selection import train_test_split, StratifiedKFold, KFold, cross_val_score
from sklearn.metrics import roc_auc_score, mean_squared_error, r2_score
from tabpfn import TabPFNClassifier, TabPFNRegressor
from tabpfn.constants import ModelVersion
optuna.logging.set_verbosity(optuna.logging.WARNING)

HERE = os.path.dirname(os.path.abspath(__file__))
DATA = os.path.join(HERE, "data")
OUT = os.path.join(HERE, "results.csv")
N_TRIALS = 30

def load(name):
    if name == "breast_cancer":
        X, y = load_breast_cancer(return_X_y=True, as_frame=True); return X, y, "cls"
    if name == "diabetes_reg":
        X, y = load_diabetes(return_X_y=True, as_frame=True); return X, y, "reg"
    if name == "california":
        X, y = fetch_california_housing(return_X_y=True, as_frame=True, data_home=DATA); return X, y, "reg"
    ids = {"credit_g": 31, "pima_diabetes": 37, "blood_transfusion": 1464, "adult": 1590, "auto_mpg": 196}
    try:
        d = fetch_openml(data_id=ids[name], as_frame=True, data_home=DATA, parser="auto")
    except TypeError:
        d = fetch_openml(data_id=ids[name], as_frame=True, data_home=DATA, parser="liac-arff")
    X, y = d.data, d.target
    task = "reg" if name == "auto_mpg" else "cls"
    if task == "cls":
        y = pd.Series(pd.factorize(y, sort=True)[0], index=y.index)
    else:
        y = y.astype(float)
    return X, y, task

def prep(X):
    """Return (numeric matrix for TabPFN, categorical idx, frame for XGB)."""
    X = X.copy()
    cat_cols = [c for c in X.columns if not pd.api.types.is_numeric_dtype(X[c])]
    for c in cat_cols:
        X[c] = X[c].astype(str).fillna("missing").astype("category")
    Xn = X.copy()
    for c in cat_cols:
        Xn[c] = Xn[c].cat.codes.astype(float)
    idx = [X.columns.get_loc(c) for c in cat_cols]
    return Xn.to_numpy(dtype=float), idx, X

def xgb_model(task, **p):
    base = dict(tree_method="hist", enable_categorical=True, n_jobs=8, verbosity=0)
    base.update(p)
    return xgb.XGBClassifier(eval_metric="logloss", **base) if task == "cls" else xgb.XGBRegressor(**base)

def score(task, y, p):
    if task == "cls":
        return {"auc": roc_auc_score(y, p)}
    return {"rmse": float(np.sqrt(mean_squared_error(y, p))), "r2": r2_score(y, p)}

def pred(m, task, X):
    return m.predict_proba(X)[:, 1] if task == "cls" else m.predict(X)

def run_one(dataset, task, Xtr_f, Xte_f, Xtr_n, Xte_n, cat_idx, ytr, yte, seed, n_train, rows):
    # 1) XGBoost default
    t = time.time(); m = xgb_model(task, random_state=seed); m.fit(Xtr_f, ytr)
    rows.append(dict(model="XGBoost 기본값", **(lambda sc: {**sc, "sec": time.time() - t})(score(task, yte, pred(m, task, Xte_f)))))
    # 2) XGBoost tuned (Optuna, 3-fold CV on train only)
    t = time.time()
    cv = StratifiedKFold(3, shuffle=True, random_state=seed) if task == "cls" else KFold(3, shuffle=True, random_state=seed)
    scoring = "roc_auc" if task == "cls" else "neg_root_mean_squared_error"
    def obj(tr):
        p = dict(n_estimators=tr.suggest_int("n_estimators", 50, 800, log=True),
                 learning_rate=tr.suggest_float("learning_rate", 0.005, 0.3, log=True),
                 max_depth=tr.suggest_int("max_depth", 2, 10),
                 subsample=tr.suggest_float("subsample", 0.5, 1.0),
                 colsample_bytree=tr.suggest_float("colsample_bytree", 0.4, 1.0),
                 min_child_weight=tr.suggest_float("min_child_weight", 0.5, 20, log=True),
                 reg_lambda=tr.suggest_float("reg_lambda", 1e-3, 10, log=True))
        return cross_val_score(xgb_model(task, random_state=seed, **p), Xtr_f, ytr, cv=cv, scoring=scoring).mean()
    st = optuna.create_study(direction="maximize", sampler=optuna.samplers.TPESampler(seed=seed))
    st.optimize(obj, n_trials=N_TRIALS)
    m = xgb_model(task, random_state=seed, **st.best_params); m.fit(Xtr_f, ytr)
    rows.append(dict(model=f"XGBoost 튜닝({N_TRIALS}회)", **(lambda sc: {**sc, "sec": time.time() - t})(score(task, yte, pred(m, task, Xte_f)))))
    # 3) TabPFN-2, no tuning
    t = time.time()
    cls = TabPFNClassifier if task == "cls" else TabPFNRegressor
    m = cls.create_default_for_version(ModelVersion.V2, device="cpu", random_state=seed,
                                       categorical_features_indices=cat_idx or None, ignore_pretraining_limits=True)
    m.fit(Xtr_n, ytr.to_numpy())
    rows.append(dict(model="TabPFN-2 (튜닝 없음)", **(lambda sc: {**sc, "sec": time.time() - t})(score(task, yte, pred(m, task, Xte_n)))))

def write(rows, meta):
    new = not os.path.exists(OUT)
    keys = ["part", "dataset", "task", "n_rows", "n_feat", "n_train", "seed", "model", "auc", "rmse", "r2", "sec"]
    with open(OUT, "a", newline="") as f:
        w = csv.DictWriter(f, fieldnames=keys)
        if new: w.writeheader()
        for r in rows:
            w.writerow({**meta, **r})

def main(part):
    done = set()
    if os.path.exists(OUT):
        d = pd.read_csv(OUT); done = set(zip(d.part, d.dataset, d.n_train, d.seed))
    if part in ("A", "all"):
        for name in ["breast_cancer", "credit_g", "pima_diabetes", "blood_transfusion", "diabetes_reg", "auto_mpg"]:
            X, y, task = load(name)
            Xn, cat_idx, Xf = prep(X)
            for seed in range(5):
                strat = y if task == "cls" else None
                itr, ite = train_test_split(np.arange(len(y)), test_size=0.3, random_state=seed, stratify=strat)
                if ("A", name, len(itr), seed) in done: continue
                rows = []
                run_one(name, task, Xf.iloc[itr], Xf.iloc[ite], Xn[itr], Xn[ite], cat_idx, y.iloc[itr], y.iloc[ite], seed, len(itr), rows)
                write(rows, dict(part="A", dataset=name, task=task, n_rows=len(y), n_feat=X.shape[1], n_train=len(itr), seed=seed))
                print("A", name, seed, [(r["model"], round(r.get("auc", r.get("rmse", 0)), 4), round(r["sec"], 1)) for r in rows], flush=True)
    if part in ("B", "all"):
        for name in ["adult", "california"]:
            X, y, task = load(name)
            Xn, cat_idx, Xf = prep(X)
            for seed in range(3):
                rng = np.random.RandomState(100 + seed)
                perm = rng.permutation(len(y)); ite = perm[:2000]; pool = perm[2000:]
                for n in [100, 300, 1000, 3000]:
                    if ("B", name, n, seed) in done: continue
                    itr = pool[:n]
                    if task == "cls" and len(np.unique(y.iloc[itr])) < 2: continue
                    rows = []
                    run_one(name, task, Xf.iloc[itr], Xf.iloc[ite], Xn[itr], Xn[ite], cat_idx, y.iloc[itr], y.iloc[ite], seed, n, rows)
                    write(rows, dict(part="B", dataset=name, task=task, n_rows=len(y), n_feat=X.shape[1], n_train=n, seed=seed))
                    print("B", name, n, seed, [(r["model"], round(r.get("auc", r.get("rmse", 0)), 4), round(r["sec"], 1)) for r in rows], flush=True)

if __name__ == "__main__":
    main(sys.argv[1] if len(sys.argv) > 1 else "all")
