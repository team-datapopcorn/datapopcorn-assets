# 의료사고로 고소된 의사는 실제로 어디까지 갈까?

DataPopcorn 테크블로그 글 [datapopcorn.ai/blog/medical-accident-criminal-data](https://datapopcorn.ai/blog/medical-accident-criminal-data)의 재현 패키지입니다.

[![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/team-datapopcorn/datapopcorn-assets/blob/main/medical-accident-criminal-data/medical_accident_analysis.ipynb)

## 들어 있는 것

| 파일 | 내용 | 출처 |
|---|---|---|
| `medical_accident_analysis.ipynb` | 글의 숫자와 차트 5개를 다시 만드는 노트북 | |
| `data/suspects_doctor_by_year.csv` | 직업 '의사' 업무상과실치사상 피의자 수 2019~2023 | 대검찰청 범죄분석(보사연 보고서 표3-1-1, p.561 재인용) |
| `data/judgments_by_year.csv` | 의료인 업무상과실치사상 1심 판결 건수 2019~2023 | 보사연 보고서 표3-2-3, p.572 |
| `data/verdicts_192.csv` | 1심 판결 피고인 192명의 선고 결과 | 표3-2-11, p.582 |
| `data/departments_192.csv` | 피고인 진료항목(상위 12개 + 나머지 합) | 표3-2-37, p.602 |
| `data/kmedi_requests.csv` | 의료분쟁 조정·중재 신청 건수 2019~2025 | 한국의료분쟁조정중재원 통계연보 2023·2025 |
| `data/youtube_reaction.json` | '아주대병원 압수수색' 유튜브 검색 상위 영상 조회수와 주제 분류(제목 제외) | 유튜브 검색 결과, 2026-10-25 조회 |

## 원문

- 한국보건사회연구원 「국민중심 의료개혁 추진방안에 관한 연구」(한국형사·법무정책연구원 판결문 분석 포함): https://www.mohw.go.kr/board.es?mid=a10411010100&bid=0019&act=view&list_no=1487190
- 한국의료분쟁조정중재원 통계연보: https://k-medi.or.kr

## 주의

- 판결문 분석은 약식명령·불기소·불송치 사건을 포함하지 않습니다(보고서 p.566~567).
- 피의자 수는 업무상과실치사상 전체로, 의료사고 외 사건이 섞였을 수 있습니다.
- 조정 신청, 피의자, 판결은 서로 다른 통계라 단계 간 비율로 나누지 마세요.
- 유튜브 영상 제목은 개인의 국적 등이 포함돼 있어 싣지 않았고, 단어 기준 주제 분류만 남겼습니다.
