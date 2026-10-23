# 기준금리 동결 vs 연초 대비 변화: 재현 패키지

한국은행 「한국은행 기준금리 추이」 변경일자 표(2026-10-23 조회)로 2024-01-01~2026-10-22 일별 기준금리를 복원하고, 2026-10-22 동결 결정(3.00%)을 이번 결정 변화(0%p)와 기준일 대비 변화(2026-01-01 대비 +0.50%p, 2024-01-01 대비 -0.50%p)로 나눠 봅니다.

## 실행
- Colab: `base-rate-hold-history.ipynb`를 열고 `런타임 → 모두 실행`. 차트 4개가 그려집니다. API 키 필요 없음.
- 로컬: `DATA_DIR=./data jupyter nbconvert --execute --to notebook base-rate-hold-history.ipynb`

## data/
| 파일 | 내용 |
|---|---|
| bok_base_rate_table_raw.csv | 표 tbody 61행을 글자 그대로 옮긴 원시 추출(최신순). 노트북은 이 파일만 읽어 다시 계산 |
| rate_changes.csv | 날짜 오름차순 변경행: date, rate_pct(연 %), diff_pp(%p), series_type, in_window_2024_20261022, table_row_order |
| daily_rate.csv | 2024-01-01~2026-10-22 일별 상태(직전 변경값 forward-fill): date, rate_pct, applied_change_date, year |
| days_by_rate_2026.csv | 2026-01-01~10-22(양끝 포함) 금리별 일수 |
| reference_date_comparison.csv | 2024-01-01, 2026-01-01, 2026-10-22 금리와 10/22 대비 차이(%p) |
| source_metadata.json | 출처 URL, 원문 SHA-256, 각주, 단위, 처리 규칙 |

원문 HTML·PDF 전체 대신 수치 추출본을 제공합니다. URL과 SHA-256으로 원출처를 확인하세요.

## 주의
- 표는 금리가 바뀐 날만 기록합니다. 변경행 수는 회의 수가 아닙니다. 10/22 동결은 결정문 확인값이며 변경행으로 넣지 않았습니다.
- 변경일자부터 새 금리를 적용한 계산이며 법적 효력 시각은 검증하지 않았습니다. 2026년은 10/22까지 부분 연도입니다.
- 2008년 2월 이전은 콜금리 목표라 분석에서 제외합니다.
- 기준금리는 대출금리가 아니며, 개인 이자부담이나 향후 금리를 예측하지 않습니다.

## 검증 상태 (2026-10-23)
- 로컬 DATA_DIR 전체 실행: 에러 0, 차트 4개.
- 원격 URL 기준 실행: 아직 미실행(게시 전).
