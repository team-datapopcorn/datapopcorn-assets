# 1편: 국민연금 사업장 데이터 첫 점검

[![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/team-datapopcorn/datapopcorn-assets/blob/main/de-bi-series/01-nps-first-look/nps_first_look.ipynb)

`nps_first_look.ipynb`는 글에서 쓴 2026-10-23 등록 파일(자료생성년월 2026-09, 589,413행)을 파일 ID로 고정해 받고, 인코딩 변환 → DuckDB raw 적재 → 의심 체크 5개 → 회사 3곳 조회를 그대로 실행합니다. 받은 파일의 sha256은 `5ce875a10d6bb6f3312af2878ad1cdc65e2a4bfb3dba341bf1a6d32c7fb97d42`입니다.
