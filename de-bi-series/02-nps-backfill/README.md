# 2편: 월별 스냅샷 백필

```bash
pip install duckdb
python backfill.py 2024-10-01 2026-10-31   # 등록일 범위. 최신 파일은 항상 포함
python build_monthly.py                    # raw/ym=*/nps.csv.gz → staging/ym=*/nps.parquet
```

- `backfill.py`: 포털의 과거 파일 목록을 읽고, 파일 안의 `자료생성년월`로 `raw/ym=YYYY-MM/`에 원본을 gzip 보관하고 `manifest.csv`에 기록합니다. 이미 받은 과거 파일은 다시 받지 않습니다.
- `build_monthly.py`: CP949 원본을 UTF-8로 읽어 컬럼 이름과 타입을 정리한 parquet 사본을 만듭니다.
- `manifest.csv`: 글에서 받은 25개 파일(자료생성년월 2024-09 ~ 2026-09)의 행 수, 바이트 수, sha256.

과거 파일 목록은 공식 오픈API가 아니라 포털 화면이 쓰는 요청이라 예고 없이 바뀔 수 있습니다. 포털에 부담을 주지 않도록 파일 사이에 2초씩 쉽니다. 25개월치 원본은 gzip으로 약 850MB입니다.
