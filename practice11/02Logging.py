# 11-2. Logging (FastAPI에서 로깅)

# Middleware를 배웠으면, 가장 먼저 실무에서 붙이는 게 Logging이야.
# 왜냐면 운영에서 “무슨 요청이 들어왔고, 얼마나 걸렸는지”를 반드시 알아야 하기 때문.

# 1. 기본 Logging Middleware
# from fastapi import FastAPI, Request
# import time

# app = FastAPI()

# @app.middleware("http")
# async def logging_middleware(request: Request, call_next):
#     start_time = time.time()

#     print(f"요청 시작: {request.method} {request.url}")

#     response = await call_next(request)

#     process_time = time.time() - start_time
#     print(f"요청 완료: {request.method} {request.url} - {process_time:.4f}s")

#     return response
# 2. 실행 흐름
# 요청 시작 로그 찍힘
# → 라우터 실행
# → 응답 생성
# → 응답 시간 계산
# → 요청 완료 로그
# 3. 로그에 남기면 좋은 정보 (실무 기준)
# HTTP Method (GET, POST)
# URL
# Status Code
# 응답 시간
# Client IP
# Request ID (추적용)
# 4. 실무형 Logging Middleware
# @app.middleware("http")
# async def logging_middleware(request: Request, call_next):
#     start_time = time.time()

#     client_ip = request.client.host

#     response = await call_next(request)

#     process_time = time.time() - start_time

#     print(
#         f"[{request.method}] {request.url} "
#         f"Status: {response.status_code} "
#         f"IP: {client_ip} "
#         f"Time: {process_time:.4f}s"
#     )

#     return response
# 5. print 대신 logging 쓰기 (중요)

# 실무에서는 print 안 씀.
# 파이썬 표준 라이브러리인 logging 사용함.

# import logging

# logging.basicConfig(level=logging.INFO)
# logger = logging.getLogger(__name__)
# @app.middleware("http")
# async def logging_middleware(request: Request, call_next):
#     start_time = time.time()

#     response = await call_next(request)

#     process_time = time.time() - start_time

#     logger.info(
#         f"{request.method} {request.url} "
#         f"{response.status_code} "
#         f"{process_time:.4f}s"
#     )

#     return response
# 6. Spring이랑 비교
# FastAPI Logging Middleware ≒ Spring HandlerInterceptor / Filter Logging

# Spring에서는:

# preHandle → controller → postHandle → afterCompletion

# FastAPI에서는:

# middleware before → router → middleware after
# 7. 한 단계 더 (실무 감각)

# 너 수준에서는 여기까지 이해하면 좋다:

# 단순 로그 → Middleware
# 구조화 로그(JSON) → ELK / Datadog
# Trace → OpenTelemetry
# 핵심 요약
# Logging = 요청/응답 흐름을 기록하는 핵심 장치
# Middleware에서 처리하는 이유:
# → 모든 요청에 공통 적용 가능
# → 성능 측정 가능
# → 장애 분석 가능
# 실무 핵심:
# print ❌
# logging 모듈 ✅