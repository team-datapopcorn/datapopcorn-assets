# 피치클락은 KBO 경기를 얼마나 줄였나? (재현 패키지)

[![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/team-datapopcorn/datapopcorn-assets/blob/main/kbo-pitch-clock/kbo_pitch_clock_analysis.ipynb)

데이터팝콘 테크블로그 글 [피치클락 2초 줄였는데 경기는 왜 길어졌을까? KBO 5,024경기로 직접 검증해봤습니다](https://datapopcorn.ai/blog/kbo-pitch-clock-game-time-analysis)의 모든 숫자와 차트를 다시 만드는 노트북과 데이터입니다.

위 배지를 누르면 Colab에서 바로 열립니다. `런타임 → 모두 실행`을 누르면 1분 안에 끝납니다.

## 파일

| 경로 | 내용 |
|---|---|
| `kbo_pitch_clock_analysis.ipynb` | 분석 노트북 (Step 0~8). 수집 코드 포함 |
| `collect_kbo.py` | 로컬에서 쓰는 같은 수집 스크립트 (`python collect_kbo.py 2019 2021 2022 2023 2024 2025 2026`) |
| `data/raw_kbo_2019_2026.tar.gz` | KBO 홈페이지 게임센터 원본 JSON(경기별 스코어보드 + 박스스코어), 5,024경기 |
| `data/games.csv` | 원본을 경기 1행으로 정리한 표. 노트북이 원본을 다시 파싱해 이 파일과 같은지 확인합니다 |

## 출처와 수집

- KBO 홈페이지 게임센터의 공개 JSON: `GetScheduleList`(경기 목록), `GetScoreBoardScroll`(경기시간 `USE_TM`, 관중, 개시·종료), `GetBoxScoreScroll`(양 팀 투수 기록 TOTAL: 투구 수, 상대 타자 수, 4사구, 삼진, 실점, 피안타)
- 범위: 2019, 2021~2026 정규시즌. 2020은 무관중·일정 변동이 커서 제외. 2026은 수집일까지 끝난 704경기
- 수집일: 2026-10-07 16:01~16:08 (KST)

## 정의

- 정규이닝 경기: `realMaxInning == 9`이고 두 팀 투수 이닝 합 17 이상(9회말 생략 포함). 4,610경기
- 경기시간: KBO가 기록한 `USE_TM`(우천 중단 시간 제외)
- 투구 1개당 평균 소요시간 = 경기시간 ÷ 투구 수. 이닝 교대, 투수 교체, 판독 시간이 포함되므로 피치클락이 재는 투구 간격과 다릅니다

## 결론 요약

- 같은 투구 수·타자 수 기준 경기시간은 2019~2023년 2023년 대비 약 ±1.2분 안에서 평평했고, 2024년 −6.2분, 2025년 −9.0분이 됐습니다
- 2023→2025 단축(−9.3분)은 거의 전부 투구 1개당 소요시간 몫이었습니다(−8.9분)
- 2025→2026 증가(+3.5분)는 대부분 투구 수 증가 몫(+3.1분)이고, 투구 수 증가는 타석 수(안타·득점) 증가에서 왔습니다. 투구 1개당 소요시간 몫은 +0.4분(95% 구간 −0.7~+1.5분)으로 0과 구분되지 않습니다
- 같은 해 여러 규칙이 함께 바뀌었고 비교군이 없어, 피치클락 하나의 인과효과로 확정하지 않습니다
