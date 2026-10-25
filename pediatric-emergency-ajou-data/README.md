# 압수수색 영상 250만 번, 소아응급 전담 전문의는 하루 86명?

DataPopcorn 테크블로그 글 [datapopcorn.ai/blog/pediatric-emergency-ajou-data](https://datapopcorn.ai/blog/pediatric-emergency-ajou-data)의 재현 패키지입니다. 사건의 과실·책임은 다루지 않습니다(경찰 수사 중).

[![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/team-datapopcorn/datapopcorn-assets/blob/main/pediatric-emergency-ajou-data/pediatric_emergency_analysis.ipynb)

## 들어 있는 것

| 파일 | 내용 | 출처 |
|---|---|---|
| `pediatric_emergency_analysis.ipynb` | 글의 숫자와 차트 5개를 다시 만드는 노트북 (API 키 없이 실행) | |
| `data/centers_timeline.csv` | 소아전문응급의료센터 수 2020~2026 | [보건복지부 보도자료 2026-05-15](https://www.mohw.go.kr/board.es?mid=a10503010100&bid=0027&act=view&list_no=1490521&tag=&nPage=1) |
| `data/centers_specialists.csv` | 12개 센터 일평균 전담전문의(2024, 2025.6, 2025.12), 2025년 일평균 소아 환자 | [국회예산정책처 2025회계연도 결산 분석](https://www.nabo.go.kr/board/file/down.do?fid=33319416) 283쪽 표(보건복지부 자료), 환자 수는 보건복지부 보도자료 |
| `data/region_adequacy.csv` | 권역별 적정 수(연구 추정)와 2026년 5월 운영 수 | 국회예산정책처 결산 분석(이한나 외 2025 인용), 14곳 명단으로 집계 |
| `data/residents_pediatrics.csv` | 소아청소년과 전공의 확보율 | 국회예산정책처 결산 분석 각주 |
| `data/er_limit_messages.csv` | 응급실 진료제한 메시지와 '인력부족' 분류 건수 | 보건복지부 응급실 수용곤란 고지 통계(국회 제출), [더메디컬 2026-10-02](https://www.themedical.kr/news/articleView.html?idxno=3520) |
| `data/datalab_daily_onerequest.json` | 네이버 데이터랩 일별 응답 원본(2026-09-01~10-24, 네 묶음 한 요청) | 네이버 데이터랩 API, 2026-10-25 조회 |
| `data/youtube_top.json` | 유튜브 '아주대병원 압수수색' 검색 상위 영상 조회수·채널·게시 시점(영상 제목은 제외) | 유튜브 검색 결과, 2026-10-25 조회 |

## 주의

- 보고서 PDF와 기사 원문은 저작권 때문에 싣지 않았습니다. CSV는 원문 표를 옮긴 것이고, 소계(85.59명, 444,436건)가 원문과 일치하는지 확인했습니다.
- 85.59명은 2025년 12월까지 지정된 12곳의 일평균입니다(2026년 5월 신규 2곳 제외).
- 진료제한 '인력부족'은 의원실이 메시지 문구로 분류한 값으로, 실제 수용불가 건수와 다를 수 있습니다.
- 적정 18곳은 연구 추정치입니다.
- 유튜브 검색 결과는 개인화와 조회 시점의 영향을 받습니다. 공개 파일에는 영상 제목을 넣지 않았습니다(당사자 국적 등이 제목에 포함돼 있어서).
