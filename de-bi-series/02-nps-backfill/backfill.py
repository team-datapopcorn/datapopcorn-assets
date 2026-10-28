"""국민연금 가입 사업장 내역: 과거 월별 파일 백필 (2편 실습 코드)

- 공공데이터포털의 '주기성 과거 데이터' 목록을 읽고
- 파일마다 다운로드 → 기준월(자료생성년월) 확인 → raw/ym=YYYY-MM/ 에 gzip으로 원본 보관
- manifest.csv에 파일명, 등록일, 기준월, 행 수, 크기, sha256 기록
- 이미 받은 기준월은 건너뛴다(다시 돌려도 결과가 같다)
"""
import csv, gzip, hashlib, io, json, os, re, sys, time
import urllib.parse, urllib.request

BASE = "https://www.data.go.kr"
PK = "15083277"                                        # 국민연금 가입 사업장 내역
DETAIL_PK = "uddi:4f8f48cf-344b-471f-b7f2-c2aa98c210a7"  # 최신 파일의 상세 ID
START_REG, END_REG = sys.argv[1], sys.argv[2]          # 등록일 범위 예: 2024-10-01 2026-10-31
HEADERS = {"User-Agent": "Mozilla/5.0", "X-Requested-With": "XMLHttpRequest",
           "Referer": f"{BASE}/data/{PK}/fileData.do"}


def post(path, data):
    req = urllib.request.Request(BASE + path, data=urllib.parse.urlencode(data).encode(), headers=HEADERS)
    with urllib.request.urlopen(req, timeout=60) as r:
        return r.read().decode("utf-8")


def list_files():
    """과거 파일 목록(최신 파일 포함). [(상세ID, 파일명, 등록일)]"""
    html = post("/tcs/dss/selectHistAndCsvData.do", {"publicDataPk": PK, "publicDataDetailPk": DETAIL_PK})
    rows = re.findall(r'data-public-pk="(uddi:[0-9a-f-]+)"\s+data-public-detail-sn="\d+">\s*([^<]+?)\s*</a>'
                      r'\s*</td>\s*<td>([0-9-]+)</td>', html)
    return [(DETAIL_PK, "최신 파일", "9999-12-31")] + rows


def download(detail_pk):
    meta = json.loads(post("/tcs/dss/selectFileDataDownload.do", {
        "publicDataPk": PK, "publicDataDetailPk": detail_pk, "fileDetailSn": "1",
        "publicDataTyCode": "PR0051", "atchFileId": ""}))
    url = f"{BASE}/cmm/cmm/fileDownload.do?atchFileId={meta['atchFileId']}&fileDetailSn={meta['fileDetailSn']}&insertDataPrcus=N"
    for attempt in range(3):                         # 네트워크 오류면 3번까지 다시 시도
        try:
            with urllib.request.urlopen(urllib.request.Request(url, headers=HEADERS), timeout=300) as r:
                return r.read()
        except Exception as e:
            print("  retry", attempt + 1, e)
            time.sleep(5 * (attempt + 1))
    raise RuntimeError("download failed")


def main():
    os.makedirs("raw", exist_ok=True)
    done, done_files = set(), set()
    if os.path.exists("manifest.csv"):
        for r in csv.DictReader(open("manifest.csv", encoding="utf-8")):
            done.add(r["ym"])
            done_files.add(r["file_name"])
    new_manifest = not os.path.exists("manifest.csv")
    out = open("manifest.csv", "a", newline="", encoding="utf-8")
    w = csv.writer(out)
    if new_manifest:
        w.writerow(["ym", "file_name", "registered", "rows", "bytes", "sha256"])

    for detail_pk, name, reg in list_files():
        if not (START_REG <= reg <= END_REG) and reg != "9999-12-31":
            continue
        if name in done_files and name != "최신 파일":  # 이미 받은 과거 파일은 내려받지도 않는다
            print("skip", name)
            continue
        body = download(detail_pk)
        text = body.decode("cp949")                  # 원본 인코딩은 CP949
        lines = text.splitlines()
        yms = {line.split(",", 1)[0] for line in lines[1:] if line}
        if len(yms) != 1:
            raise ValueError(f"{name}: 기준월이 하나가 아님 {sorted(yms)[:5]}")
        ym = yms.pop()                               # 파일 이름이 아니라 파일 안의 자료생성년월
        if ym in done:
            print("skip", ym, name)
            continue
        os.makedirs(f"raw/ym={ym}", exist_ok=True)
        with gzip.open(f"raw/ym={ym}/nps.csv.gz", "wb") as f:  # 원본 바이트 그대로 압축 보관
            f.write(body)
        w.writerow([ym, name, reg, len(lines) - 1, len(body), hashlib.sha256(body).hexdigest()])
        out.flush()
        done.add(ym)
        print("saved", ym, name, len(lines) - 1, "rows")
        time.sleep(2)                                # 포털에 부담 주지 않게 쉬어 가기


if __name__ == "__main__":
    main()
