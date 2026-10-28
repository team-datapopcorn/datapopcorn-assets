"""서울 실시간 도시데이터(인구) 121곳을 한 번 수집해 원본 그대로 저장한다.

실행할 때마다 raw/dt=YYYY-MM-DD/HHMMSS.jsonl.gz 파일 하나가 생긴다.
한 줄 = 한 장소의 API 응답 원문 + 수집 시각. 실패한 장소도 기록한다.
"""
import concurrent.futures as cf
import datetime as dt
import gzip, json, os, urllib.request

KEY = os.environ["SEOUL_API_KEY"]
PLACES = json.load(open("places.json", encoding="utf-8"))  # [[코드, 장소명], ...]
URL = "http://openapi.seoul.go.kr:8088/{key}/json/citydata_ppltn/1/5/{code}"
KST = dt.timezone(dt.timedelta(hours=9))


def fetch(code):
    try:
        with urllib.request.urlopen(URL.format(key=KEY, code=code), timeout=30) as r:
            return {"code": code, "ok": True, "body": json.loads(r.read())}
    except Exception as e:  # 실패도 버리지 않고 남긴다
        return {"code": code, "ok": False, "error": type(e).__name__}


def main():
    now = dt.datetime.now(KST)
    with cf.ThreadPoolExecutor(8) as ex:
        results = list(ex.map(fetch, [c for c, _ in PLACES]))
    folder = f"raw/dt={now:%Y-%m-%d}"
    os.makedirs(folder, exist_ok=True)
    with gzip.open(f"{folder}/{now:%H%M%S}.jsonl.gz", "wt", encoding="utf-8") as f:
        for r in results:
            r["fetched_at"] = now.isoformat(timespec="seconds")
            f.write(json.dumps(r, ensure_ascii=False) + "\n")
    ok = sum(r["ok"] for r in results)
    print(f"{now:%H:%M:%S} saved {ok}/{len(results)}")


if __name__ == "__main__":
    main()
