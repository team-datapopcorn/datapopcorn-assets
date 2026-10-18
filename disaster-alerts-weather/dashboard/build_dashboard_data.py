"""data/의 정리된 파일로 웹 대시보드용 data.json을 만듭니다.
실행: python dashboard/build_dashboard_data.py  (disaster-alerts-weather 폴더에서)"""
import json, os, datetime as dt
import numpy as np, pandas as pd
import statsmodels.api as sm, statsmodels.formula.api as smf
HERE = os.path.dirname(os.path.abspath(__file__)); ROOT = os.path.dirname(HERE)
a = pd.read_csv(os.path.join(ROOT, 'data/alerts.csv.gz'))
w = pd.read_csv(os.path.join(ROOT, 'data/asos_daily.csv.gz'))
stn = pd.read_csv(os.path.join(ROOT, 'data/station_sido.csv'))
SIDO = ['서울','부산','대구','인천','광주전남','대전','울산','세종','경기','강원','충북','충남','전북','경북','경남','제주']
N_SGG = {'서울':25,'부산':16,'대구':9,'인천':10,'광주전남':27,'대전':5,'울산':5,'세종':1,'경기':31,'강원':18,'충북':11,'충남':15,'전북':14,'경북':22,'경남':18,'제주':2}
start, end = a.date.min(), a.date.max()
days = pd.date_range(start, end).strftime('%Y-%m-%d').tolist(); di = {d: i for i, d in enumerate(days)}
months = sorted({d[:7] for d in days}); mi = {m: i for i, m in enumerate(months)}
types = a.DST_SE_NM.fillna('미상').value_counts().index.tolist(); ti = {t: i for i, t in enumerate(types)}
a['t'] = a.DST_SE_NM.fillna('미상').map(ti); a['m'] = a.date.str[:7].map(mi); a['d'] = a.date.map(di)
a['wd'] = pd.to_datetime(a.date).dt.dayofweek  # 0=월
# 1) 전국(문자 1건=1) 월×유형, 일×유형(상위 유형), 시간×요일×유형
nat_mt = a.groupby(['m', 't']).size().reset_index().values.tolist()
nat_dt = a.groupby(['d', 't']).size().reset_index().values.tolist()
hwt = a.groupby(['hour', 'wd', 't']).size().reset_index().values.tolist()
# 2) 시도(여러 시도에 간 문자는 시도마다 1건) 월×시도×유형, 일×시도 합계
ex = a.assign(s=a.sido_list.fillna('').str.split('|')).explode('s'); ex = ex[ex.s.isin(SIDO)]
ex['si'] = ex.s.map({s: i for i, s in enumerate(SIDO)})
sido_mt = ex.groupby(['m', 'si', 't']).size().reset_index().values.tolist()
sido_d = ex.groupby(['d', 'si']).size().reset_index().values.tolist()
sido_d_heat = ex[ex.DST_SE_NM == '폭염'].groupby(['d', 'si']).size().reset_index().values.tolist()
sido_d_rain = ex[ex.DST_SE_NM == '호우'].groupby(['d', 'si']).size().reset_index().values.tolist()
# 3) 날씨 패널
wn = w[~w.stnId.isin(stn.loc[stn.island_excluded, 'stnId'])]
P = wn.groupby(['sido', 'tm']).agg(feels=('feelsMax', 'max'), tmax=('maxTa', 'max'), tmin=('minTa', 'min'), rain=('sumRn', 'max')).reset_index()
wx = {}
for s in SIDO:
    q = P[P.sido == s].set_index('tm').reindex(days)
    wx[s] = {k: [None if pd.isna(v) else round(float(v), 1) for v in q[k]] for k in ['feels', 'tmax', 'tmin', 'rain']}
# 4) 분석 결과(블로그와 같은 정의)
GAP = ('2025-09-26', '2025-10-26')
ex2 = ex[~ex.date.between(*GAP)]
pan = P.rename(columns={'tm': 'date'})
for typ, col in [('폭염', 'heat'), ('호우', 'rain_alert')]:
    c = ex2[ex2.DST_SE_NM == typ].groupby(['s', 'date']).size().rename(col)
    pan = pan.merge(c, left_on=['sido', 'date'], right_index=True, how='left')
pan = pan.fillna({'heat': 0, 'rain_alert': 0}); pan = pan[~pan.date.between(*GAP)]
pan['year'] = pan.date.str[:4].astype(int); pan['month'] = pan.date.str[5:7].astype(int)
S = pan[pan.month.isin([6, 7, 8, 9]) & pan.year.isin([2024, 2025, 2026])].dropna(subset=['feels']).copy()
S['hit'] = (S.heat > 0).astype(int); S['fbin'] = np.clip(np.floor(S.feels), 26, 37).astype(int); S['fb36'] = np.clip(S.fbin, 26, 36)
dose = S.groupby('fbin').agg(p=('hit', 'mean'), n=('hit', 'size')).reset_index()
curve = S.groupby(['year', 'fb36']).heat.mean().unstack(0)
S = S.sort_values(['sido', 'date']); S['hot'] = (S.feels >= 33).astype(int)
S['run10'] = np.minimum(S.groupby('sido').hot.transform(lambda x: x.groupby((x != x.shift()).cumsum()).cumsum()) * S.hot, 10)
g = S.sido.astype('category').cat.codes
po = smf.glm('heat ~ C(year) + C(fbin) + C(sido) + C(month) + run10', data=S, family=sm.families.Poisson()).fit(cov_type='cluster', cov_kwds={'groups': g})
nb = smf.negativebinomial('heat ~ C(year) + C(fbin) + C(sido) + C(month) + run10', data=S).fit(disp=0, maxiter=300, cov_type='cluster', cov_kwds={'groups': g})
def irr(m, y):
    k = f'C(year)[T.{y}]'; b, se = m.params[k], m.bse[k]
    return [round(float(np.exp(b)), 2), round(float(np.exp(b - 1.96 * se)), 2), round(float(np.exp(b + 1.96 * se)), 2), round(float(m.pvalues[k]), 3)]
hot = S[S.hot == 1]
reg = hot.groupby('sido').agg(per_hot_day=('heat', 'mean'), p_any=('hit', 'mean'), hot_days=('heat', 'size'))
reg['per_sgg'] = reg.per_hot_day / pd.Series(N_SGG)
hs = hot.groupby(['sido', 'year']).heat.mean().unstack()
h = a[(a.DST_SE_NM == '폭염')].copy(); h['year'] = h.date.str[:4].astype(int); h['sgg'] = h.RCPTN_RGN_NM.str.strip().str.split().str[:2].str.join(' ')
h = h[h.year.isin([2024, 2025, 2026])]
rep = (h.groupby(['year', 'date', 'sgg']).size() >= 2).groupby('year').mean()
rep_d = (h.drop_duplicates(['date', 'sgg', 'msg_hash']).groupby(['year', 'date', 'sgg']).size() >= 2).groupby('year').mean()
R = pan.copy(); R['hit'] = (R.rain_alert > 0).astype(int)
R['rb'] = pd.cut(R.rain, [-1, 0.1, 10, 30, 60, 100, 1000], right=False, labels=['0', '0.1~10', '10~30', '30~60', '60~100', '100+'])
rain = R.groupby('rb', observed=True).hit.agg(['mean', 'size'])
analysis = {
  'heat_dose': {'bins': dose.fbin.tolist(), 'p': dose.p.round(3).tolist(), 'n': dose.n.tolist()},
  'heat_curve': {'bins': curve.index.tolist(), **{str(y): curve[y].round(2).tolist() for y in curve.columns}},
  'by_year': {str(y): {'hot_days': int((hot.year == y).sum()), 'p_any': round(float(hot[hot.year == y].hit.mean()), 3), 'per_hot_day': round(float(hot[hot.year == y].heat.mean()), 2)} for y in [2024, 2025, 2026]},
  'irr': {'poisson': {str(y): irr(po, y) for y in [2025, 2026]}, 'negbin': {str(y): irr(nb, y) for y in [2025, 2026]}},
  'repeat_share': {str(k): round(float(v), 3) for k, v in rep.items()}, 'repeat_share_dedup': {str(k): round(float(v), 3) for k, v in rep_d.items()},
  'sgg_sending': {str(k): int(v) for k, v in h.groupby('year').sgg.nunique().items()},
  'region': {s: {'per_hot_day': round(float(r.per_hot_day), 2), 'per_sgg': round(float(r.per_sgg), 2), 'p_any': round(float(r.p_any), 3), 'hot_days': int(r.hot_days), 'n_sgg': N_SGG[s], 'ratio_2025_2024': (None if pd.isna(hs.loc[s, 2024]) or hs.loc[s, 2024] == 0 else round(float(hs.loc[s, 2025] / hs.loc[s, 2024]), 2))} for s, r in reg.iterrows()},
  'rain_dose': {'bins': [str(k) for k in rain.index], 'p': rain['mean'].round(3).tolist(), 'n': rain['size'].astype(int).tolist()},
}
out = {
  'meta': {'generated_at': dt.datetime.now(dt.timezone(dt.timedelta(hours=9))).strftime('%Y-%m-%d %H:%M KST'),
           'alerts_range': [start, end], 'asos_range': [w.tm.min(), w.tm.max()], 'n_alerts': int(len(a)), 'n_stations': int(w.stnId.nunique()),
           'gap': list(GAP), 'gap_note': '2025-09-26 국가정보자원관리원 대전센터 화재 이후 31일간 플랫폼 기록 0건(분석에서 제외)',
           'blog': 'https://datapopcorn.ai/blog/disaster-alerts-weather-analysis',
           'colab': 'https://colab.research.google.com/github/team-datapopcorn/datapopcorn-assets/blob/main/disaster-alerts-weather/disaster_alerts_weather_analysis.ipynb',
           'repo': 'https://github.com/team-datapopcorn/datapopcorn-assets/tree/main/disaster-alerts-weather'},
  'days': days, 'months': months, 'types': types, 'sido': SIDO, 'n_sgg': N_SGG,
  'nat_mt': nat_mt, 'nat_dt': nat_dt, 'hwt': hwt, 'sido_mt': sido_mt, 'sido_d': sido_d, 'sido_d_heat': sido_d_heat, 'sido_d_rain': sido_d_rain,
  'step': a.EMRG_STEP_NM.fillna('미상').value_counts().to_dict(), 'wx': wx, 'analysis': analysis,
}
json.dump(out, open(os.path.join(HERE, 'data.json'), 'w'), ensure_ascii=False, separators=(',', ':'))
print('data.json', round(os.path.getsize(os.path.join(HERE, 'data.json')) / 1024), 'KB', out['meta'])
