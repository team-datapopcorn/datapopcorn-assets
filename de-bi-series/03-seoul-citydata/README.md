# 3편: 서울 실시간 도시데이터 5분 수집기

`raw/`에는 글에서 쓴 수집 결과(2026-10-28 15:33 ~ 16:40, 15회, 121곳)가 들어 있어서 인증키 없이도 글의 숫자를 다시 만들 수 있습니다.

```bash
pip install duckdb
python flatten.py          # raw → city.duckdb의 stg_population (장소, 기준시각 중복 제거)
python forecast_eval.py    # 예측 vs 실제 비교
```

직접 수집하려면 서울 열린데이터광장에서 일반 인증키를 받은 뒤 실행합니다.

```bash
export SEOUL_API_KEY=발급받은키
python collect.py          # 한 번 실행 = 121곳 한 번 수집
```

`loop.sh`는 5분 정각마다 `collect.py`를 실행하는 예시입니다. 키는 같은 폴더의 `.key` 파일에서 읽으니 `.key`는 커밋하지 마세요. 요청이 잘못되면 서버 에러 메시지에 키가 들어간 주소가 그대로 담겨 오니, 에러 로그를 공유할 때 주의하세요.
