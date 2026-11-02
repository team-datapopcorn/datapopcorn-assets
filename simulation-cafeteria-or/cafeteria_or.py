"""구내식당 점심: OR-Tools CP-SAT 최적 시차 배정 + SimPy 검증 (데이터팝콘 현업 시뮬레이션 진단 샘플)
가상 고객사 A의 가상 데이터. 기준 시각 11:30 = 0분, 12:00 = 30분."""
import math, random, statistics as st
import pandas as pd

START = 11 * 60 + 30
SLOTS = [0, 10, 20, 30, 40, 50]           # 11:30 ~ 12:20 출발 후보
PEAK_FROM, PEAK_TO, NOON = 20, 45, 30     # 11:50~12:15 사이 도착 = 부서 단위로 움직이는 사람

def hm(m): m = int(round(m)) + START; return f"{m // 60}:{m % 60:02d}"
def to_min(s): h, m = s.strip().split(":")[:2]; return int(h) * 60 + int(m) - START

def load_arrivals(path):
    df = pd.read_csv(path)
    t = pd.to_datetime(df.iloc[:, 0])
    a = (t.dt.hour * 60 + t.dt.minute + t.dt.second / 60 - START).tolist()
    return sorted(x for x in a if 0 <= x < 120)

def load_depts(path):
    d = pd.read_csv(path)
    return [dict(name=r["부서"], n=int(r["인원"]), lo=to_min(r["가장 이른 출발"]), hi=to_min(r["가장 늦은 출발"])) for _, r in d.iterrows()]

# ---------- 1. 최적 배정 (OR-Tools CP-SAT) ----------
def cost(d, i, s):
    """1000 × 사람·분(인원 × 12시와의 차이) + 동점 해소용 작은 값. 웹 도구(highs-js)와 같은 목적함수."""
    return 1000 * d["n"] * abs(s - NOON) + (i + 1) * (SLOTS.index(s) + 1)

def solve_plan(depts, T, time_limit=10):
    """가장 몰리는 출발 시각의 인원을 T 이하로 두면서 옮기는 사람·분을 최소화한다."""
    from ortools.sat.python import cp_model
    m = cp_model.CpModel()
    x = {(i, s): m.NewBoolVar(f"x_{i}_{s}") for i, d in enumerate(depts) for s in SLOTS if d["lo"] <= s <= d["hi"]}
    for i in range(len(depts)):
        m.AddExactlyOne(x[i, s] for s in SLOTS if (i, s) in x)
    for s in SLOTS:
        m.Add(sum(depts[i]["n"] * v for (i, t), v in x.items() if t == s) <= T)
    m.Minimize(sum(cost(depts[i], i, s) * v for (i, s), v in x.items()))
    sv = cp_model.CpSolver(); sv.parameters.max_time_in_seconds = time_limit
    r = sv.Solve(m)
    if r != cp_model.OPTIMAL: return None
    plan = [next(s for s in SLOTS if (i, s) in x and sv.Value(x[i, s])) for i in range(len(depts))]
    return dict(T=T, plan=plan, moved=moved_of(depts, plan), peak=peak_of(depts, plan))

def moved_of(depts, plan): return sum(d["n"] * abs(p - NOON) for d, p in zip(depts, plan))
def peak_of(depts, plan): return max(sum(d["n"] for d, p in zip(depts, plan) if p == s) for s in SLOTS)

def peak_grid(depts):
    """몰림 한도 후보: 이론 최저(전체/시각 수, 가장 큰 부서)부터 전체 인원까지 12단계 (웹 도구와 같음)"""
    tot = sum(d["n"] for d in depts); lb = max(math.ceil(tot / len(SLOTS)), max(d["n"] for d in depts))
    g = [lb] + [int(math.floor((lb + (tot - lb) * k / 11) / 5 + 0.5) * 5) for k in range(1, 12)]
    return sorted(set(g))

# ---------- 2. 배정을 실제 도착 기록에 적용 ----------
def apply_plan(arrivals, depts, plan):
    """11:50~12:15에 온 사람을 부서 인원 비율대로 (시간순, 가중 라운드로빈) 나누고 부서 출발 시각만큼 옮긴다.
    JS(/fit/fitlib.js applyPlan)와 같은 규칙이라 두 엔진이 같은 도착 기록을 쓴다."""
    tot = sum(d["n"] for d in depts); cur = [0.0] * len(depts); out = []
    for a in arrivals:
        if PEAK_FROM <= a < PEAK_TO:
            for i, d in enumerate(depts): cur[i] += d["n"] / tot
            k = max(range(len(depts)), key=lambda i: (cur[i], -i)); cur[k] -= 1
            out.append(min(118, max(0.1, a + plan[k] - NOON)))
        else: out.append(a)
    return sorted(out)

def shift_share(arrivals, frac=0.4, delta=-20, seed=7):
    r = random.Random(seed)
    return sorted(min(118, max(0.1, a + delta)) if PEAK_FROM <= a < PEAK_TO and r.random() < frac else a for a in arrivals)

# ---------- 3. SimPy 모델 ----------
def simulate(arrivals, lines=3, serve_sec=14, seats=216, eat_min=18, seed=1):
    import simpy
    rnd = random.Random(seed); env = simpy.Environment()
    L = [simpy.Resource(env, capacity=1) for _ in range(lines)]
    S = simpy.Resource(env, capacity=seats)
    s = serve_sec / 60; rec = []
    def person(a):
        yield env.timeout(a - env.now)
        order = list(range(lines)); rnd.shuffle(order)
        k = min(order, key=lambda j: len(L[j].queue) + L[j].count)
        with L[k].request() as rq:
            yield rq; q0 = env.now
            yield env.timeout(rnd.triangular(0.6 * s, 1.4 * s, s))
        yield env.timeout(0.4); ready = env.now
        rq = S.request(); yield rq; seat_t = env.now
        yield env.timeout(rnd.triangular(0.6 * eat_min, 1.4 * eat_min, eat_min) + 0.1)
        S.release(rq)
        rec.append((q0 - a, seat_t - ready))
    def src():
        for a in arrivals: env.process(person(a))
        yield env.timeout(0)
    env.process(src()); env.run()
    w = sorted(q + t for q, t in rec)
    return dict(avgWait=st.mean(w), avgQueueWait=st.mean(q for q, _ in rec), p90Wait=w[int(len(w) * 0.9)],
                stood=sum(t > 0.25 for _, t in rec))

def run_many(arrivals, n=30, **kw):
    rs = [simulate(arrivals, seed=i, **kw) for i in range(1, n + 1)]
    return {k: round(st.mean(r[k] for r in rs), 1) for k in rs[0]}

