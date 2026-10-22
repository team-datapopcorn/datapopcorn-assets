# 소매유통업 경기전망: 수준과 변화

대한상공회의소 2026년 4분기 RBSI 공식 집계표로 차트 4개를 재현합니다. 응답자별 원시자료가 아닙니다.

- `retail-outlook-gap.ipynb`: Colab에서 전체 실행. 인증키 불필요.
- `data/rbsi_sectors.csv`: 전체 및 5개 업태, 3분기·4분기 전망지수.
- `data/rbsi_quarterly.csv`: 2024Q3~2026Q4 전체 지수 10개.
- `data/source_metadata.json`: 출처 URL, 수집 시각, PDF SHA-256, 조사 정의.

로컬은 DATA_DIR을 이 폴더의 data 절대경로로 지정합니다. KOREAN_FONT는 사용 가능한 한글 TTF 절대경로, CHART_DIR는 생성 차트 저장 경로입니다. Python pandas, matplotlib, numpy, nbformat, nbclient, ipykernel이 필요합니다.

## 데이터 사전
- sector: 업태 이름. 전체 행은 5개 업태의 산술평균으로 재계산하지 않음.
- q3_2026 / q4_2026: 각 분기 경기 전망 RBSI. 100은 호전·악화 응답 균형.
- quarter: 전망 대상 분기, 조사 시점이나 실적 분기가 아님.
- rbsi: 공식 전체 지수.
- CSV 인코딩: UTF-8 BOM.

## 범위와 한계
조사 2026-08-31~09-18, 서울 및 6대 광역시 500개 업체 대상. 응답 총수·업태별 응답 수는 공개 원문에 명시되지 않음. 계절조정 전 원계열. 매출·소비자 의견·인과효과를 뜻하지 않음. 공식 자료의 집계 사실만 전사했으며 PDF/기사 본문/원본 차트 이미지는 패키지에 포함하지 않았습니다.
