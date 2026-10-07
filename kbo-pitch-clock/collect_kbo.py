"""KBO 정규시즌 경기별 소요시간·투구수 수집 (KBO 공식 홈페이지 공개 JSON).
Colab/로컬 공용. 원본 응답은 raw/ 에 gzip JSON으로 보존한다."""
import json, re, gzip, os, sys, time, urllib.request, urllib.parse
from concurrent.futures import ThreadPoolExecutor
BASE = 'https://www.koreabaseball.com/ws/Schedule.asmx/'
HDR = {'User-Agent': 'Mozilla/5.0 (datapopcorn research)', 'X-Requested-With': 'XMLHttpRequest',
       'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
       'Referer': 'https://www.koreabaseball.com/Schedule/Schedule.aspx'}
RAW = os.environ.get('RAW_DIR', 'raw')
def post(fn, data, tries=4):
    body = urllib.parse.urlencode(data).encode()
    for a in range(tries):
        try:
            req = urllib.request.Request(BASE + fn, data=body, headers=HDR)
            return json.loads(urllib.request.urlopen(req, timeout=30).read().decode('utf-8'))
        except Exception as e:
            time.sleep(1.5 * (a + 1))
    raise RuntimeError(f'{fn} {data}')
def game_ids(season):
    ids = []
    for m in range(3, 12):
        j = post('GetScheduleList', {'leId': 1, 'srIdList': '0', 'seasonId': season, 'gameMonth': f'{m:02d}', 'teamId': ''})
        for r in j.get('rows', []):
            for c in r['row']:
                g = re.search(r"gameId=(\d{8}[A-Z]{4}\d)&section=REVIEW", c.get('Text') or '')
                if g: ids.append(g.group(1))
    return sorted(set(ids))
def fetch(season, gid):
    path = f'{RAW}/{season}/{gid}.json.gz'
    if os.path.exists(path): return path
    sb = post('GetScoreBoardScroll', {'leId': 1, 'srId': 0, 'seasonId': season, 'gameId': gid})
    bx = post('GetBoxScoreScroll', {'leId': 1, 'srId': 0, 'seasonId': season, 'gameId': gid})
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with gzip.open(path, 'wt', encoding='utf-8') as f:
        json.dump({'scoreboard': sb, 'boxscore': bx, 'retrieved': time.strftime('%Y-%m-%dT%H:%M:%S%z')}, f, ensure_ascii=False)
    time.sleep(0.15)
    return path
if __name__ == '__main__':
    seasons = [int(s) for s in sys.argv[1:]] or list(range(2019, 2027))
    for s in seasons:
        ids = game_ids(s)
        json.dump(ids, open(f'{RAW}/gameids_{s}.json', 'w')) if os.path.isdir(RAW) else None
        with ThreadPoolExecutor(4) as ex: list(ex.map(lambda g: fetch(s, g), ids))
        print(s, len(ids), 'games', flush=True)
