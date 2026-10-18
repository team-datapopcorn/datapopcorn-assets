# 재난문자 63,402건 × 기상청 ASOS 날씨

데이터팝콘 테크블로그 글 [폭염 재난문자, 정말 더워서 늘었을까?](https://datapopcorn.ai/blog/disaster-alerts-weather-analysis)의 재현 패키지입니다.

[![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/team-datapopcorn/datapopcorn-assets/blob/main/disaster-alerts-weather/disaster_alerts_weather_analysis.ipynb)

## 파일

| 경로 | 내용 |
|---|---|
| `disaster_alerts_weather_analysis.ipynb` | 글의 모든 숫자와 차트 7장을 다시 만드는 노트북. API 키 없이 `data/`만 읽습니다 |
| `data/alerts.csv.gz` | 행정안전부 긴급재난문자 63,402건(2023-09-01 ~ 2026-10-18). 발송 시각, 수신 지역, 단계, 재난 유형, 정리한 시도 목록, 키워드 플래그, 본문 해시 |
| `data/asos_daily.csv.gz` | 기상청 ASOS 일자료 97개 지점, 110,867 지점-일(2023-09-01 ~ 2026-10-17). 최고·최저기온, 최소습도, 일강수량 등과 근사 체감온도(`feelsMax`) |
| `data/station_sido.csv` | ASOS 지점 → 시도 대응표. 섬 지점 3곳(백령도·울릉도·흑산도)은 시도 집계에서 뺍니다 |
| `raw/asos_daily_raw_api_2026-10-18.json.gz` | 공공데이터포털 ASOS API 원본 응답(지점별, 2026-10-18 수집) |
| `collect/collect.py` | 두 API에서 원자료를 처음부터 다시 받는 스크립트(키 필요, 선택) |
| `collect/prep.py` | 원자료를 `data/`의 정리된 파일로 바꾸는 스크립트 |

## 웹 대시보드

[재난문자 × 날씨 대시보드](https://datapopcorn.ai/blog/disaster-alerts-dashboard)에서 연도·지역·유형을 골라 볼 수 있습니다. 대시보드는 이 폴더의 `dashboard/data.json`을 읽습니다. `data/`를 새로 받은 뒤 `python dashboard/build_dashboard_data.py`를 실행해 올리면 대시보드도 함께 갱신됩니다.

## 정리 규칙

- **재난문자 본문은 공개하지 않습니다.** 실종자 이름과 인상착의가 들어간 문자가 있어서, 본문 대신 공백을 지운 본문의 SHA-1 앞 12자리(`msg_hash`)만 둡니다. 같은 문자를 반복 저장했는지 확인하는 데는 이것으로 충분합니다.
- **시도 이름은 16개로 맞춥니다.** 2026년 `전남광주통합특별시` 출범 전후 이름이 섞여 있어서 광주광역시·전라남도·전남광주통합특별시를 `광주전남`으로, 전라북도·전북특별자치도를 `전북`으로 묶습니다.
- **한 문자가 여러 시도에 가면 시도마다 한 번씩 셉니다.** 1,408건이 해당합니다.
- **2025-09-26 ~ 2025-10-26은 분석에서 뺍니다.** 이 기간 기록이 0건입니다. 같은 날 밤 국가정보자원관리원 대전센터 화재로 정부 전산망이 멈췄습니다.
- **체감온도는 근사값입니다.** 기상청 여름철 체감온도 식에 일최고기온과 일최소습도를 넣었습니다. 기상청 특보는 시간별 값과 예보로 판단합니다.

## 출처

- 행정안전부 긴급재난문자: 재난안전데이터공유플랫폼 오픈API `DSSP-IF-00247`, 2026-10-18 수집. 이용허락범위 제한 없음
- 기상청 지상(종관, ASOS) 일자료: 공공데이터포털 `AsosDalyInfoService`, 2026-10-18 수집. 공공누리 제1유형(출처표시)

## 원자료부터 다시 만들기

```bash
cd collect
export SAFETYDATA_KEY=...   # 재난안전데이터공유플랫폼 서비스키 (등록한 IP에서만 동작)
export DATAGOKR_KEY=...     # 공공데이터포털 일반 인증키(Decoding)
python collect.py           # alerts_raw.json, asos_raw.json
python prep.py              # ../data/*.csv 생성
gzip -f ../data/alerts.csv ../data/asos_daily.csv
```

수집 시점이 다르면 최근 며칠 치 문자가 더해져 숫자가 조금 달라집니다.
