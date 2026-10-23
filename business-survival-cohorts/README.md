# business-survival-cohorts

DataPopcorn 테크블로그 「1년 생존율은 내리고 5년은 올랐다? 같은 해 신생기업끼리 다시 읽는 7단계」 재현 패키지입니다.

- 원자료: 국가데이터처 「2025년 기업생멸행정통계(잠정) 결과」 보도자료(2026-10-22 발표) PDF 27쪽(인쇄 21쪽) 표19 연도별 신생기업 생존율, 2026-10-24 조회
- 원문 PDF와 기사 본문은 싣지 않았습니다. PDF 주소·SHA-256·쪽 번호는 `data/source_metadata.json`에 있습니다.

## 파일

| 파일 | 내용 |
|---|---|
| `business-survival-cohorts.ipynb` | Colab 노트북. 표 행 텍스트 → CSV → 검증 → 차트 4개. 부록(기본 꺼짐)은 PDF 다운로드·해시 확인·27쪽 재파싱 |
| `reproduce_table19.py` | 같은 파서·검증·차트 코드를 스크립트로. `python reproduce_table19.py` 는 `fig_out/` 에 webp 4개 저장, `--pdf 파일.pdf` 는 pypdf로 27쪽을 다시 읽어 대조 |
| `data/table19_raw_lines.csv` | 표19 영역의 행 텍스트 13줄 (line_no, text, pdf_page, printed_page) |
| `data/survival_rates.csv` | 56행. scope(전체/부동산업 제외), observation_year(2021~2024, 2024는 잠정), horizon_years(1~7), birth_year(=관측-기간), rate_pct(%), pdf_page |
| `data/table19_official_changes.csv` | 표의 '증감' 행 14칸 (scope, horizon_years, change_pp, pdf_page) |
| `data/source_metadata.json` | 출처 URL, SHA-256, 저장 시각, 교차 대조 결과, 정의 위치 |

## 읽을 때 주의

- 같은 관측 연도의 1~7년 생존율은 신생 연도가 다른 7개 집단입니다. 한 집단의 생존 곡선이 아닙니다.
- 36.5/63.9 같은 나눗셈은 분자·분모 집단이 달라 조건부 생존확률이 아닙니다.
- 생존은 소멸되지 않고 지속 존속했다는 뜻이지 이익을 냈다는 뜻이 아닙니다. 원인(경기·금리·정책)은 이 표로 판단할 수 없습니다.
- 원문 유의사항(PDF 83쪽): 과거 수치는 산업분류 갱신 등으로 바뀔 수 있고, 2023년부터 금융·보험업 기업 자료가 추가됐습니다.
