import json, glob, re, pandas as pd, numpy as np
# ---- stations -> 시도 (harmonized; 광주+전남 merged because of 2026 통합특별시) ----
S = {
 '강원':[90,93,95,100,101,104,105,106,114,121,211,212,216,217],
 '경기':[98,99,119,202,203], '인천':[102,112,201], '서울':[108],
 '경북':[115,130,135,136,137,138,271,272,273,276,277,278,279,281,283],
 '충북':[127,131,181,221,226], '충남':[129,177,232,235,236,238], '대전':[133], '세종':[239],
 '전북':[140,146,172,243,244,245,247,248,251,254], '대구':[143], '울산':[152],
 '경남':[155,162,192,253,255,257,263,264,284,285,288,289,294,295],
 '광주전남':[156,165,168,169,170,174,252,258,259,260,261,262,266,268],
 '부산':[159,296], '제주':[184,185,188,189]}
ISLANDS = {102,115,169}
rows=[]
for v in json.load(open('asos_raw.json')).values():
    rows += v
w = pd.DataFrame(rows)
keep = ['stnId','stnNm','tm','avgTa','minTa','maxTa','minRhm','avgRhm','sumRn','hr1MaxRn','maxWs','maxInsWs','ddMes','sumDpthFhsc']
w = w[keep].copy()
for c in keep[3:]: w[c] = pd.to_numeric(w[c].replace('', np.nan), errors='coerce')
w['stnId']=w['stnId'].astype(int)
w['sumRn']=w['sumRn'].fillna(0.0)   # ASOS: blank sumRn means no precipitation
stn2 = {i:k for k,v in S.items() for i in v}
w['sido']=w['stnId'].map(stn2)
assert w['sido'].notna().all(), w[w.sido.isna()].stnId.unique()
w['island']=w['stnId'].isin(ISLANDS)
# KMA summer feels-like temperature (체감온도), using daily max temp + daily min RH as an approximation of the afternoon peak
Ta, RH = w['maxTa'], w['minRhm']
Tw = Ta*np.arctan(0.151977*np.sqrt(RH+8.313659)) + np.arctan(Ta+RH) - np.arctan(RH-1.67633) + 0.00391838*RH**1.5*np.arctan(0.023101*RH) - 4.686035
w['feelsMax'] = -0.2442 + 0.55399*Tw + 0.45535*Ta - 0.0022*Tw**2 + 0.00278*Tw*Ta + 3.0
w.to_csv('../data/asos_daily.csv', index=False)
pd.DataFrame([(i,n,stn2[i],i in ISLANDS) for i,n in w[['stnId','stnNm']].drop_duplicates().values], columns=['stnId','stnNm','sido','island_excluded']).sort_values('stnId').to_csv('../data/station_sido.csv', index=False)
print('asos', w.shape, w.tm.min(), w.tm.max(), 'stations', w.stnId.nunique())
print('missing maxTa', w.maxTa.isna().sum(), 'missing minRhm', w.minRhm.isna().sum())

# ---- alerts ----
a = pd.DataFrame(json.load(open('alerts_raw.json'))).astype(str)
print('alerts', a.shape, a.SN.nunique())
SIDO = {'서울특별시':'서울','부산광역시':'부산','대구광역시':'대구','인천광역시':'인천','광주광역시':'광주전남','대전광역시':'대전','울산광역시':'울산','세종특별자치시':'세종','경기도':'경기','강원특별자치도':'강원','강원도':'강원','충청북도':'충북','충청남도':'충남','전라북도':'전북','전북특별자치도':'전북','전라남도':'광주전남','전남광주통합특별시':'광주전남','경상북도':'경북','경상남도':'경남','제주특별자치도':'제주','부천시':'경기'}
def sidos(s):
    out=set()
    for part in str(s).split(','):
        t=part.strip().split()
        if t and t[0] in SIDO: out.add(SIDO[t[0]])
    return '|'.join(sorted(out))
a['sido_list']=a['RCPTN_RGN_NM'].map(sidos)
a['n_sido']=a['sido_list'].str.count(r'\|')+ (a['sido_list']!='').astype(int)
dt=pd.to_datetime(a['CRT_DT'], format='%Y/%m/%d %H:%M:%S')
a['date']=dt.dt.strftime('%Y-%m-%d'); a['hour']=dt.dt.hour
msg=a['MSG_CN'].fillna('')
import hashlib
a['msg_hash']=msg.str.replace(r'\s+','',regex=True).map(lambda t: hashlib.sha1(t.encode('utf-8')).hexdigest()[:12])  # 본문 대신 해시만 공개(실종자 개인정보 보호)
a['kw_missing_person']=msg.str.contains('찾습니다|실종|배회', regex=True)
a['kw_shelter']=msg.str.contains('쉼터', regex=False)
a['kw_heat_warning_word']=msg.str.contains('폭염(?:주의보|경보|특보)', regex=True)
pub = a[['SN','CRT_DT','date','hour','RCPTN_RGN_NM','sido_list','n_sido','EMRG_STEP_NM','DST_SE_NM','kw_missing_person','kw_shelter','kw_heat_warning_word','msg_hash']]
pub.to_csv('../data/alerts.csv', index=False, encoding='utf-8')
print('unmapped alerts', (a.sido_list=='').sum(), a.loc[a.sido_list=='','RCPTN_RGN_NM'].str.split().str[0].value_counts().head(5).to_dict())
print('multi-sido alerts', (a.n_sido>1).sum())
