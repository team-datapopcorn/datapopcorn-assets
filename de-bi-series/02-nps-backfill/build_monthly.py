"""raw/ym=*/nps.csv.gz (CP949 원본) → staging/ym=*/nps.parquet (UTF-8, 컬럼 타입 정리)

- 원본은 건드리지 않는다. parquet은 언제든 원본에서 다시 만들 수 있는 사본이다.
- 이미 만든 달은 건너뛴다.
"""
import glob, gzip, os, tempfile
import duckdb

con = duckdb.connect()
for src in sorted(glob.glob("raw/ym=*/nps.csv.gz")):
    ym = src.split("ym=")[1].split("/")[0]
    out = f"staging/ym={ym}/nps.parquet"
    if os.path.exists(out):
        continue
    os.makedirs(os.path.dirname(out), exist_ok=True)
    with tempfile.NamedTemporaryFile("w", suffix=".csv", encoding="utf-8", delete=False) as tmp:
        with gzip.open(src, "rt", encoding="cp949") as f:
            for line in f:
                tmp.write(line)
    con.sql(f"""
    COPY (
      SELECT
        자료생성년월                         AS ym,
        사업장명                             AS workplace_name,
        사업자등록번호                       AS bizno6,
        "사업장가입상태코드 1 등록 2 탈퇴"   AS status_code,
        우편번호                             AS zipcode,
        법정동주소광역시도코드               AS sido_code,
        "사업장형태구분코드 1 법인 2 개인"   AS biz_type,
        사업장업종코드                       AS industry_code,
        사업장업종코드명                     AS industry_name,
        적용일자                             AS joined_on,
        탈퇴일자                             AS left_on,
        CAST(가입자수 AS INTEGER)            AS members,
        CAST(당월고지금액 AS BIGINT)         AS billed_amount,
        CAST(신규취득자수 AS INTEGER)        AS new_members,
        CAST(상실가입자수 AS INTEGER)        AS lost_members
      FROM read_csv('{tmp.name}', header = true, all_varchar = true)
    ) TO '{out}' (FORMAT parquet)
    """)
    os.remove(tmp.name)
    print("built", ym)
