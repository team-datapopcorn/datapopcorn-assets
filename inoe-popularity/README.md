# 사람들은 왜 '인외'에 빠졌을까? 재현 패키지

DataPopcorn 테크블로그 글 「사람들은 왜 '인외'에 빠졌을까? 검색·웹소설·블로그 데이터로 뜯어보기」의 데이터와 노트북입니다.

[![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/team-datapopcorn/datapopcorn-assets/blob/main/inoe-popularity/inoe_analysis.ipynb)

## 들어 있는 것

| 경로 | 내용 | 수집일 |
|---|---|---|
| `inoe_analysis.ipynb` | 글의 숫자와 차트를 다시 만드는 노트북. API 키 없이 실행됩니다 | |
| `data/naver_datalab/` | 네이버 데이터랩 검색어트렌드 API 응답 원본(JSON). 주별 2016~, 일별 2025~, 롯데월드 키워드 비교, 성별·연령 필터 결과(`demo_anchor.json`) | 2026-10-20 |
| `data/naver_searchad/` | 검색광고 API 최근 30일 검색수(`searchad_volumes.json`), 키워드도구 상세 화면의 월별 검색수·성별·연령(`searchad_ui_detail.json`, 차트 좌표에서 역산) | 2026-10-21 |
| `data/google_trends/` | 구글 트렌드(대한민국) 월별·일별 CSV, 관련 검색어 | 2026-10-21 |
| `data/ridi/ridi_books.csv` | 리디 로맨스·로판 키워드 검색 `인외존재` 1,837종, `회귀/타임슬립` 1,980종과 작품별 출간일 | 2026-10-21 |
| `data/ridi/ridi_tag_cooccur.json` | `인외존재` × 남자 주인공·관계 태그 55개 동시 출현 작품 수 | 2026-10-21 |
| `data/blog/blog_coded.csv` | 네이버 블로그 1,047건의 주소·작성일·맥락/이유 분류 결과(0/1). 원문은 저작권 때문에 싣지 않습니다 | 2026-10-21 |
| `data/blog/validation_sample.csv` | 사전 분류 정확도 점검 표본 40건과 수동 판정(1=의도한 의미) | 2026-10-21 |

## 주의

- 데이터랩 값은 요청마다 최고 시점을 100으로 놓는 상대지수입니다. 같은 파일 안의 키워드끼리만 크기를 비교할 수 있습니다.
- 키워드도구 상세 화면 값은 차트 좌표를 숫자로 옮긴 것이라 수십 회, 0.3%p 수준의 반올림 오차가 있습니다.
- 리디 데이터는 조회 시점에 판매 중인 작품만 잡힙니다. 태그가 생기기 전 작품은 덜 잡히므로 연도별 비교는 2023년부터만 해석합니다.
- 블로그 분류는 단어 사전 방식입니다. 표본 40건을 직접 읽어 확인한 결과 31건(약 78%)이 의도한 의미였습니다.
