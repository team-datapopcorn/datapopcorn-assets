"""원자료를 처음부터 다시 받는 스크립트 (선택).
노트북은 이미 받아 둔 data/ 파일을 읽으므로 이 스크립트 없이도 모든 결과가 재현됩니다.
API 키 두 개가 필요합니다.
  SAFETYDATA_KEY : 재난안전데이터공유플랫폼(safetydata.go.kr) '행정안전부_긴급재난문자' 이용신청 후 발급되는 서비스키 (신청 시 등록한 IP에서만 호출됩니다)
  DATAGOKR_KEY   : 공공데이터포털 '기상청_지상(종관, ASOS) 일자료 조회서비스' 활용신청 후 받는 일반 인증키(Decoding)
"""
import os, json, time, urllib.parse, urllib.request
SAFETY = os.environ['SAFETYDATA_KEY']; DGK = os.environ['DATAGOKR_KEY']
def get(url):
    for i in range(3):
        try: return json.loads(urllib.request.urlopen(url, timeout=60).read().decode('utf-8'))
        except Exception as e: time.sleep(1 + i); err = e
    raise err
# 1) 재난문자: 1,000건씩 전체 페이지 (기본 정렬은 오래된 순)
first = get(f'https://www.safetydata.go.kr/V2/api/DSSP-IF-00247?serviceKey={SAFETY}&pageNo=1&numOfRows=1000&returnType=json')
pages = -(-first['totalCount'] // 1000); rows = []
for p in range(1, pages + 1):
    rows += get(f'https://www.safetydata.go.kr/V2/api/DSSP-IF-00247?serviceKey={SAFETY}&pageNo={p}&numOfRows=1000&returnType=json')['body']
assert len({r['SN'] for r in rows}) == len(rows), 'SN 중복: 수집 중 새 문자가 들어와 페이지가 밀렸을 수 있습니다. 다시 실행하세요.'
json.dump(rows, open('alerts_raw.json', 'w'), ensure_ascii=False)
# 2) ASOS 일자료: 지점별 2023-09-01 ~ 어제
stations = [int(l.split(',')[0]) for l in open('../data/station_sido.csv').read().splitlines()[1:]]
end = time.strftime('%Y%m%d', time.localtime(time.time() - 86400)); asos = {}
for s in stations:
    out, p = [], 1
    while True:
        j = get('https://apis.data.go.kr/1360000/AsosDalyInfoService/getWthrDataList?' + urllib.parse.urlencode(
            dict(serviceKey=DGK, pageNo=p, numOfRows=999, dataType='JSON', dataCd='ASOS', dateCd='DAY', startDt='20230901', endDt=end, stnIds=s)))
        out += j['response']['body']['items']['item']
        if len(out) >= j['response']['body']['totalCount']: break
        p += 1
    asos[s] = out
json.dump(asos, open('asos_raw.json', 'w'), ensure_ascii=False)
print(len(rows), 'alerts,', sum(len(v) for v in asos.values()), 'station-days')
