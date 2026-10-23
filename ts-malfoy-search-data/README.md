# 사람들은 왜 '말포이'보다 '악역영애 말포이'를 더 검색했을까?

DataPopcorn 테크블로그 글 [datapopcorn.ai/blog/ts-malfoy-search-data](https://datapopcorn.ai/blog/ts-malfoy-search-data)의 재현 패키지입니다.

[![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/team-datapopcorn/datapopcorn-assets/blob/main/ts-malfoy-search-data/ts_malfoy_analysis.ipynb)

## 들어 있는 것

| 파일 | 내용 |
|---|---|
| `ts_malfoy_analysis.ipynb` | 글의 숫자와 차트 6개를 다시 만드는 노트북 (API 키 없이 실행) |
| `data/searchad_monthly.txt` | 네이버 검색광고 키워드도구 최근 30일 검색수 (2026-10-23 조회) |
| `data/daily_compare.json` | 네이버 데이터랩 일간: 말포이 / 악역영애 말포이 / TS말포이 등 / 해리포터 (2026-08-01~10-22) |
| `data/daily_gender_female.json`, `data/daily_gender_male.json` | 데이터랩 일간 성별 필터 (2026-09-01~10-22) |
| `data/week_mal_ay.json` | 데이터랩 주간: 말포이 / 악역영애 말포이 (2016~2026) |
| `data/pixiv_tagmode_check.json` | pixiv 'Malfoid' 태그 부분일치·완전일치 총계 비교, 비로그인 목록 상한 관찰 기록 |
| `data/pixiv_counts.json` | pixiv 태그 검색 총계. 'Malfoid'·'ドラコ・マルフォイ' 일별(2026-09-01~10-22), 'ドラコ・マルフォイ'·'女体化マルフォイ' 월별(2016-01~2026-10) |

## 주의

- 데이터랩 값은 요청마다 최고값을 100으로 맞춘 상대지수입니다. 같은 파일 안의 그룹끼리만 비교하세요.
- pixiv 총계는 태그 부분일치(`s_mode=s_tag`), 업로드 날짜(일본 시간) 필터로 받은 값입니다. 그림 파일과 작품 정보는 저장하지 않았습니다.
- 2026년 10월 월별 값은 10월 23일 조회 시점까지입니다.
