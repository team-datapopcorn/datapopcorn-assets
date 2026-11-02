# 구내식당 점심 줄: OR-Tools 최적 시차 배정 + SimPy 검증

데이터팝콘 [현업 시뮬레이션 진단](https://simulation.datapopcorn.ai/business/)의 재현 패키지입니다.

[![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/team-datapopcorn/datapopcorn-assets/blob/main/simulation-cafeteria-or/cafeteria_or_simpy.ipynb)

| 파일 | 내용 |
|---|---|
| `cafeteria_or_simpy.ipynb` | 노트북 본문. 재현 검증 → CP-SAT 최적 배정 → SimPy 30회 검증 → 웹 도구와 대조 |
| `cafeteria_or.py` | 노트북에 들어 있는 모델 코드 (최적화, 배정 적용, SimPy 시뮬레이션) |
| `sample-company-a.csv` | 가상 고객사 A의 입장 태깅 기록 620건 (가상 데이터) |
| `sample-company-a-depts.csv` | 부서 12곳의 인원, 출발 가능 시각, 검토 중인 안 (가상 데이터) |

- 최적화: 부서마다 출발 시각(11:30~12:20, 10분 간격) 하나를 고르고, 가장 몰리는 시각의 인원을 T 이하로 두면서 옮기는 사람·분을 최소화합니다. T를 12단계로 바꿔 가며 풉니다.
- 시뮬레이션: 각 배정을 SimPy로 30번 돌려, 평균 대기 3분과 오래 기다린 10% 8분을 함께 채우는 가장 적은 변경을 고릅니다.
- 웹 도구 [내 데이터로 돌려보기](https://simulation.datapopcorn.ai/fit/cafeteria/)는 같은 문제를 브라우저에서 HiGHS(highs-js)와 자바스크립트 엔진으로 풉니다. 12개 한도 모두 같은 배정이 나왔습니다.

데이터는 모두 설명용 가상 데이터이며 실제 기업 수치가 아닙니다. 문의: contact@datapopcorn.ai
