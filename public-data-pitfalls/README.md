# 공공데이터 수집에서 막히는 지점 실습

DataPopcorn 테크블로그 글 [공공데이터 수집에서 막히는 6가지와 해결법](https://datapopcorn.ai/blog/public-data-collection-pitfalls)의 실습 노트북입니다.

[![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/team-datapopcorn/datapopcorn-assets/blob/main/public-data-pitfalls/public_data_collection_pitfalls.ipynb)

- 공공데이터포털 인증키 이중 인코딩 오류 재현과 해결 (공정위 브랜드별 가맹점 API)
- PDF 통계표: `pdftotext -layout`의 빈칸 함정, `-bbox-layout` 좌표 파싱
- 교차검증: 회차 합 vs 연간 합계, 다른 파일의 같은 해 값 비교

준비물: 공공데이터포털 활용신청(본인 인증키), topik.go.kr에서 브라우저로 받은 TOPIK 시행 현황 PDF 2개.
2026-10-09 Colab(CPU)에서 전체 셀 실행 확인.
