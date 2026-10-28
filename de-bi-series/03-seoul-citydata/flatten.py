import duckdb
con = duckdb.connect("city.duckdb")
con.sql("""
CREATE OR REPLACE TABLE stg_population AS
WITH src AS (
  SELECT code, fetched_at::TIMESTAMP AS fetched_at,
         json_extract(body, '$."SeoulRtd.citydata_ppltn"[0]') AS p
  FROM read_json('raw/dt=*/*.jsonl.gz', format = 'newline_delimited',
                 columns = {code: 'VARCHAR', ok: 'BOOLEAN', fetched_at: 'VARCHAR', body: 'JSON'})
  WHERE ok
), parsed AS (
  SELECT code, fetched_at,
         p->>'AREA_NM'                         AS area_name,
         strptime(p->>'PPLTN_TIME', '%Y-%m-%d %H:%M') AS ppltn_time,
         (p->>'AREA_PPLTN_MIN')::INT           AS ppltn_min,
         (p->>'AREA_PPLTN_MAX')::INT           AS ppltn_max,
         p->>'AREA_CONGEST_LVL'                AS congest_level,
         p->'FCST_PPLTN'                       AS forecast
  FROM src
)
SELECT * FROM parsed
QUALIFY ROW_NUMBER() OVER (PARTITION BY code, ppltn_time ORDER BY fetched_at) = 1
""")
print(con.sql("SELECT COUNT(*) AS n, COUNT(DISTINCT code) AS places, MIN(ppltn_time), MAX(ppltn_time) FROM stg_population"))
