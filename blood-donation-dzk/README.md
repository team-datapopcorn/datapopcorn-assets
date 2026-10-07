# 두쫀쿠를 주면 헌혈이 늘어날까? (재현 패키지)

[![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/team-datapopcorn/datapopcorn-assets/blob/main/blood-donation-dzk/blood_gift_analysis.ipynb)

데이터팝콘 테크블로그 글 [두쫀쿠를 주면 헌혈이 늘어날까? 공공데이터로 직접 검증해봤습니다](https://datapopcorn.ai/blog/blood-donation-gift-dzk-analysis)의 모든 숫자와 차트를 다시 만드는 노트북과 데이터입니다.

위 배지를 누르면 Colab에서 바로 열립니다. `런타임 → 모두 실행`을 누르면 약 1분 안에 끝납니다.

## 파일

| 경로 | 내용 | 출처 |
|---|---|---|
| `blood_gift_analysis.ipynb` | 분석 노트북 (Step 0~9) | 데이터팝콘 |
| `data/monthly_donations_redcross_2005_2026.csv` | 대한적십자사 월별 헌혈 건수. 2005~2025는 KOSIS, 2026.01~09는 혈액관리본부 페이지 | KOSIS DT_445001_002, bloodinfo.net |
| `data/rbc_stock_daily_winter_2007_2026.csv` | 일별 적혈구제제 보유량(Unit), 매년 11~4월 | bloodinfo.net 혈액보유현황 추이 |
| `data/reported_events_2026.csv` | 두쫀쿠 등 행사의 보도 수치와 기사 링크 | 연합뉴스, 한국경제, 동아일보, 주간경향 |
| `raw/kosis_DT_445001_002_monthly_utf8.csv` | KOSIS에서 내려받은 원본(혈액원별·성별 포함, UTF-8 변환) | KOSIS |
| `raw/bloodinfo_bldStat_20261007.html` | 혈액관리본부 헌혈통계 페이지 원본(2026-10-07 조회) | bloodinfo.net |

## 정의

- 헌혈 건수는 연인원입니다. 한 사람이 두 번 헌혈하면 2건입니다.
- 월별 수치는 대한적십자사 기준입니다. KOSIS의 '합계'(한마음혈액원 등 포함)와 다릅니다.
- 보유량은 매일 0시 기준 적혈구제제 재고이며, 헌혈과 의료기관 사용량에 함께 좌우됩니다.

## 결론 요약

- 행사 당일 해당 헌혈의집의 헌혈은 2~3배가 됐습니다(보도 수치).
- 2026년 1월 전년비 +17.5%의 대부분은 설 연휴가 1월(2025)에서 2월(2026)로 옮겨간 효과와 겹칩니다.
- 1~2월 합계는 +4.2%이며, 세 가지 기준선 모두에서 평년 범위(추세선 95% 예측구간) 안입니다.
- 효과가 없었다는 뜻이 아니라, 공개된 전국 월별 자료로는 구분할 수 없는 크기라는 뜻입니다. 헌혈의집별·일별 자료가 공개되면 이중차분(DiD)으로 다시 검증할 수 있습니다.

수집일: 2026-10-07 (KST)
