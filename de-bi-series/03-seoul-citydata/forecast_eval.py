import duckdb
con = duckdb.connect("city.duckdb")
con.sql("""
CREATE OR REPLACE VIEW forecast_vs_actual AS
WITH f AS (
  SELECT s.code, s.area_name, s.ppltn_time AS issued_at,
         strptime(fc->>'FCST_TIME', '%Y-%m-%d %H:%M') AS target_time,
         ((fc->>'FCST_PPLTN_MIN')::INT + (fc->>'FCST_PPLTN_MAX')::INT) / 2.0 AS f_mid,
         fc->>'FCST_CONGEST_LVL' AS f_level
  FROM stg_population s, UNNEST(CAST(s.forecast AS JSON[])) AS t(fc)
)
SELECT f.*, (a.ppltn_min + a.ppltn_max) / 2.0 AS a_mid, a.congest_level AS a_level,
       date_diff('minute', f.issued_at, f.target_time) AS lead_min
FROM f JOIN stg_population a ON a.code = f.code AND a.ppltn_time = f.target_time
""")
print(con.sql("""
SELECT strftime(target_time, '%H:%M') AS target, issued_at::TIME AS issued, lead_min,
       COUNT(*) AS places,
       ROUND(MEDIAN(ABS(f_mid - a_mid) / a_mid) * 100, 1) AS median_err_pct,
       ROUND(AVG(CASE WHEN f_level = a_level THEN 1 ELSE 0 END) * 100, 1) AS level_match_pct
FROM forecast_vs_actual
WHERE issued_at = (SELECT MIN(ppltn_time) FROM stg_population)
GROUP BY ALL ORDER BY target
"""))
