# 공공데이터로 bar-chart-race 쇼츠 만들기

[![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/team-datapopcorn/datapopcorn-assets/blob/main/bar-chart-race-shorts/bar_chart_race_shorts.ipynb)

세계은행 API(키 불필요)에서 나라별 외환보유액(`FI.RES.TOTL.CD`, 1970~2025)을 받아 32초짜리 세로 영상(1080×1920, 30fps)으로 만드는 노트북입니다.

- 블로그 글: https://datapopcorn.ai/blog/public-data-bar-chart-race-shorts
- 실행: Colab에서 `런타임 → 모두 실행` (무료 런타임, 약 2~3분)
- 결과물 예시: `sample_output/race_final.mp4`, `sample_output/contact_sheet.jpg`

## 파일

| 파일 | 내용 |
|---|---|
| `bar_chart_race_shorts.ipynb` | 수집 → 1위 교체 확인 → 빈 연도 처리 → 프레임 생성 → ffmpeg 인코딩 → 음악 합성 → 검증 |
| `sample_output/race_final.mp4` | 2026-10-09 Colab에서 이 노트북을 실행해 나온 영상 |
| `sample_output/contact_sheet.jpg` | 같은 실행의 4장면 모아보기 |

## 출처와 라이선스

- 데이터: World Bank, World Development Indicators (CC BY 4.0)
- 음악: Kevin MacLeod - Club Diver (incompetech.com, CC BY 4.0). 영상을 게시할 때 출처를 적어야 합니다.
- 글꼴: Pretendard (SIL Open Font License)
