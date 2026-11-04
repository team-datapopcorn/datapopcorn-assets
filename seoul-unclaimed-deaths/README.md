# 무연고 사망, 독거노인 이야기일까? (서울 4개 구 데이터)

DataPopcorn 테크블로그 글 「무연고 사망, 독거노인 이야기일까? 서울 4개 구 데이터로 본 50~60대 남성」의 재현 패키지입니다.

[![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/team-datapopcorn/datapopcorn-assets/blob/main/seoul-unclaimed-deaths/seoul_unclaimed_deaths.ipynb)

## 들어 있는 것
- `seoul_unclaimed_deaths.ipynb`: 6개 구 파일 정리 → 사망자·인구 분모 결합 → 비중·비율 → 민감도 점검 → 차트
- `data/raw/gu_*.csv`: 공공데이터포털 원본 파일(조회 2026-11-03). 15133632 중랑구, 15133646 동대문구, 15132709 성북구, 15132710 용산구, 15132694 은평구, 15133976 광진구
- `data/denominators/deaths_long.csv`: 구·연도·성·10세 연령별 사망자 수(국가데이터처 인구동향조사, 한국여성정책연구원 성인지통계 DT_2FB0211R 경유)
- `data/denominators/population_long.csv`: 구·연도·성·10세 연령별 연말 주민등록인구(KOSIS DT_1B04005N)
- `data/denominators/retrieval.md`: 분모 자료 조회 방법과 합계 검산

## 주의
- 서울 25개 구 중 무연고 사망 파일을 공개한 6개 구만 다룹니다. 비율 계산은 성별·연령·연도가 모두 있는 4개 구만 씁니다.
- 무연고 사망과 고독사는 다른 통계입니다. 이 데이터에는 원인 정보가 없습니다.
- 개인을 알아볼 수 있는 정보는 없습니다. 모두 구가 공개한 집계표입니다.

로컬에서 돌릴 때는 `DATA_DIR=./data`로 폴더를 지정하면 됩니다.
