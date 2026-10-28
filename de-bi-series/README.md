# 데이터 엔지니어링·BI 실전 (재현 자료)

데이터팝콘 테크블로그 시리즈 「취준생을 위한 데이터 엔지니어링·BI 실전」의 실습 코드와 데이터입니다. 국민연금 가입 사업장 데이터로 수집부터 데이터마트, BI 대시보드까지 만들고, 서울 실시간 도시데이터로 실시간 수집을 연습합니다.

| 편 | 폴더 | 글 |
|---|---|---|
| 1 | `01-nps-first-look/` | [지원할 회사, 사람이 늘고 있을까? 국민연금 데이터 58만 행 처음 열어 보기](https://datapopcorn.ai/blog/nps-workplace-data-first-look) |
| 2 | `02-nps-backfill/` | [가입자가 한 달 만에 86만 명 늘었다? 국민연금 데이터 25개월치 쌓아 보니 보인 것](https://datapopcorn.ai/blog/nps-monthly-snapshot-backfill) |
| 3 | `03-seoul-citydata/` | [지난 값이 남지 않는 데이터, 5분마다 직접 쌓기](https://datapopcorn.ai/blog/seoul-citydata-5min-collector) |

## 출처

- 국민연금공단_국민연금 가입 사업장 내역, 공공데이터포털 15083277 (월간, 파일데이터)
- 서울 실시간 인구데이터, 서울 열린데이터광장 OA-21778 (오픈API, 인증키 필요)

원본 CSV(파일당 약 110MB)는 저장소에 넣지 않았습니다. 각 폴더의 코드가 포털에서 직접 받고, `02-nps-backfill/manifest.csv`의 sha256으로 같은 파일인지 확인할 수 있습니다.
