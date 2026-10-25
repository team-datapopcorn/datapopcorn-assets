# 모던워페어4는 정말 더 관심을 받았을까?

DataPopcorn 테크블로그 글 [datapopcorn.ai/blog/modern-warfare-4-korea-search-data](https://datapopcorn.ai/blog/modern-warfare-4-korea-search-data)의 재현 패키지입니다.

[![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/team-datapopcorn/datapopcorn-assets/blob/main/modern-warfare-4-korea-search-data/mw4_analysis.ipynb)

## 들어 있는 것

| 파일 | 내용 |
|---|---|
| `mw4_analysis.ipynb` | 글의 숫자와 차트 6개를 다시 만드는 노트북 (API 키 없이 실행) |
| `data/week_titles.json` | 데이터랩 주간: 모던워페어4·블랙옵스7·블랙옵스6·모던워페어3·모던워페어2 한 요청 (2022-01~2026-10-23), 작품별 검색어 그룹 포함 |
| `data/daily_mw4.json` | 데이터랩 일간: 모던워페어4 / 콜오브듀티 / 배틀필드6 (2026-05-01~10-23) |
| `data/week_age_mw4_mw2.json` | 데이터랩 주간 연령 필터 5개 집단: 모던워페어4 / 모던워페어2 / 유튜브 |
| `data/week_gender_f.json`, `data/week_gender_m.json` | 데이터랩 주간 성별 필터 |
| `data/searchad_monthly.txt` | 네이버 검색광고 키워드도구 최근 30일 검색수 (2026-10-24 조회) |
| `data/steam_current_players.json` | Steam 현재 동시접속 스냅샷 (작품 앱과 통합 앱 1938090) |
| `data/searchad_intents.txt` | '모던워페어4+단어' 최근 30일 검색수 (네이버 검색광고, 2026-10-25 조회) |
| `data/naver_autocomplete.json` | 네이버 자동완성 단어 (2026-10-25 조회) |
| `data/youtube_top20.json` | 유튜브 '모던워페어4' 이번 주 업로드 검색 첫 페이지 17개 영상의 조회수·제목·유형 |
| `data/naver_reaction_counts.json` | 네이버 뉴스·블로그 검색 API 날짜별 글 수 (검색어당 최대 1,000건 상한) |

## 주의

- 데이터랩 값은 요청마다 최고값을 100으로 맞춘 상대지수입니다. 같은 파일 안의 그룹끼리만 비교하세요.
- 모던워페어4의 최고 주(2026-10-19 주)는 10/23까지 닷새만 들어 있습니다.
- 연령·성별 지수는 집단마다 따로 100입니다. 집단 안의 비율로만 비교하세요.
- Steam 작품 앱의 동시접속 0은 통합 앱으로 접속이 잡히기 때문이며, 플레이어가 없다는 뜻이 아닙니다.
