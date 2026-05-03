# 1. 왜 필요한가?
# 로그/모니터링은 “에러 났을 때 보는 것”이 아니라, 서비스 상태를 계속 관찰하는 장치다.
# 로그: 무슨 일이 있었는지 기록모니터링: 지금 서비스가 정상인지 수치로 확인알림: 문제가 생기면 바로 감지

# 2. 실무에서 보는 핵심 지표
# 요청 수응답 시간에러율CPU / MemoryDB 커넥션Redis 상태외부 API 실패율
# 특히 LLM 서비스라면:
# LLM 호출 횟수LLM 응답 시간LLM 실패율토큰 사용량Rate Limit 발생 횟수

# 3. 로그 기본 설정
# import logginglogging.basicConfig(    level=logging.INFO,    format="%(asctime)s - %(levelname)s - %(message)s")logger = logging.getLogger(__name__)
# 사용:
# logger.info("User signup requested")logger.warning("Rate limit exceeded")logger.error("Failed to call Gemini API")

# 4. Router / Service에서 로그 찍기
# from fastapi import APIRouterimport loggingrouter = APIRouter()logger = logging.getLogger(__name__)@router.get("/users/{user_id}")def get_user(user_id: int):    logger.info(f"Get user request. user_id={user_id}")    user = user_service.get_user(user_id)    logger.info(f"Get user success. user_id={user_id}")    return user
# 단, 실무에서는 너무 많은 로그를 남기면 안 된다.
# 성공 로그는 적당히실패 로그는 자세히민감정보는 절대 남기지 않기

# 5. 요청 단위 로그 Middleware
# 모든 API 요청을 공통으로 기록하려면 Middleware를 쓴다.
# import timeimport loggingfrom fastapi import Requestlogger = logging.getLogger(__name__)@app.middleware("http")async def logging_middleware(request: Request, call_next):    start_time = time.time()    response = await call_next(request)    process_time = time.time() - start_time    logger.info(        f"method={request.method} "        f"path={request.url.path} "        f"status_code={response.status_code} "        f"process_time={process_time:.4f}s"    )    return response
# 이렇게 남는다.
# method=GET path=/users/1 status_code=200 process_time=0.0342s

# 6. 에러 로그
# 예외가 발생하면 stack trace를 남겨야 한다.
# try:    result = call_external_api()except Exception as e:    logger.exception("External API call failed")    raise
# logger.exception()은 에러 메시지 + stack trace를 같이 남긴다.

# 7. 구조화 로그
# 실무에서는 문자열 로그보다 JSON 로그가 좋다.
# {  "level": "INFO",  "method": "GET",  "path": "/users/1",  "status_code": 200,  "latency_ms": 34,  "user_id": 1}
# 장점:
# 검색하기 좋음필터링하기 좋음Grafana/Loki/ELK 연동에 좋음

# 8. Prometheus 모니터링
# FastAPI에서는 보통 prometheus-fastapi-instrumentator를 많이 쓴다.
# 설치:
# pip install prometheus-fastapi-instrumentator
# 적용:
# from fastapi import FastAPIfrom prometheus_fastapi_instrumentator import Instrumentatorapp = FastAPI()Instrumentator().instrument(app).expose(app)
# 그러면 다음 endpoint가 생긴다.
# /metrics
# Prometheus가 이 /metrics를 주기적으로 긁어간다.

# 9. Prometheus + Grafana 흐름
# FastAPI  ↓ /metricsPrometheus  ↓Grafana
# 역할:
# FastAPI: 지표 노출Prometheus: 지표 수집/저장Grafana: 대시보드 시각화

# 10. Sentry 에러 추적
# Sentry는 예외 추적에 좋다.
# 설치:
# pip install sentry-sdk[fastapi]
# 적용:
# import sentry_sdksentry_sdk.init(    dsn="YOUR_SENTRY_DSN",    traces_sample_rate=1.0,)
# 장점:
# 예외 발생 위치 확인stack trace 확인사용자 요청 정보 확인배포 버전별 에러 추적

# 11. 실무 모니터링 구조
# Client  ↓Nginx  ↓FastAPI  ↓DB / Redis / LLM API
# 각 계층에서 봐야 할 것:
# Nginx:- 요청 수- 4xx / 5xx- upstream timeoutFastAPI:- API latency- error rate- request countDB:- slow query- connection count- lockRedis:- memory usage- hit rate- evicted keysLLM API:- latency- failure count- token usage- rate limit

# 12. 로그 레벨
# DEBUG: 개발 중 상세 확인INFO: 정상 흐름 기록WARNING: 비정상 가능성ERROR: 요청 실패CRITICAL: 서비스 중단급 문제
# 예:
# logger.debug("SQL query params...")logger.info("User created")logger.warning("Redis cache miss increased")logger.error("Failed to save meal analysis")logger.critical("DB connection unavailable")

# 13. 절대 로그에 남기면 안 되는 것
# 비밀번호JWT 토큰Refresh TokenOAuth Access Token주민번호카드번호개인 민감정보API Key
# 나쁜 예:
# logger.info(f"Authorization={request.headers.get('Authorization')}")
# 좋은 예:
# logger.info("Authorization header exists")

# 14. 실무 체크리스트
# 요청 로그 Middleware 적용예외 로그 logger.exception 사용민감정보 마스킹Prometheus /metrics 노출Grafana 대시보드 구성Sentry 연동LLM 호출 지표 별도 기록Redis cache hit/miss 기록Rate Limit 발생 횟수 기록

# 15. 한 줄 정리
# 로그는 문제 원인을 찾기 위한 기록이고,모니터링은 문제가 생기기 전에 감지하기 위한 지표다.
# FastAPI 실무에서는 보통:
# logging + middlewarePrometheus + GrafanaSentry
# 조합으로 가져간다.