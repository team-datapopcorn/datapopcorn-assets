# TabPFN vs XGBoost

데이터팝콘 테크블로그 글 [TabPFN vs XGBoost, 튜닝 없는 AI 모델이 정말 이길까?](https://datapopcorn.ai/blog/tabpfn-vs-xgboost)의 재현 자료입니다.

| 파일 | 내용 |
|---|---|
| `tabpfn_vs_xgboost.ipynb` | Colab에서 `런타임 → 모두 실행`으로 비교를 다시 돌리는 노트북 |
| `bench.py` | 글의 숫자를 만든 원본 벤치마크 스크립트 (결과를 `results.csv`에 한 줄씩 기록) |
| `results.csv` | 2026-11-21 실행 결과 162행 (Apple M4 CPU, tabpfn 10.2.0, xgboost 3.4.1, scikit-learn 1.9.1) |

[![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/team-datapopcorn/datapopcorn-assets/blob/main/tabpfn-vs-xgboost/tabpfn_vs_xgboost.ipynb)

데이터는 모두 scikit-learn 내장 데이터와 OpenML 공개 데이터(ID 31, 37, 196, 1464, 1590)입니다. 모델은 Apache 2.0(출처 표기 조건) 라이선스의 TabPFN-2 가중치를 씁니다.
