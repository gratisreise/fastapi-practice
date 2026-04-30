# 11-1. FastAPI Middleware 구조

# Middleware는 요청(Request)과 응답(Response) 사이에 끼어드는 공통 처리 계층이야.

# 즉, 클라이언트가 API를 호출하면 흐름은 이렇게 돼.

# Client
#   ↓
# Middleware
#   ↓
# Route Handler
#   ↓
# Middleware
#   ↓
# Client

# 예를 들어 이런 공통 작업을 Middleware에서 처리할 수 있어.

# 요청 로그 기록
# 응답 시간 측정
# 인증 토큰 검사
# CORS 처리
# 에러 공통 처리
# 요청/응답 헤더 추가
# 1. 기본 Middleware 예시
from fastapi import FastAPI, Request
import time

app = FastAPI()

@app.middleware("http")
async def log_middleware(request: Request, call_next):
    start_time = time.time()

    response = await call_next(request)

    process_time = time.time() - start_time
    response.headers["X-Process-Time"] = str(process_time)

    return response

# 2. 핵심 구조
@app.middleware("http")
async def middleware_name(request: Request, call_next):
    # 1. 요청이 라우터에 도달하기 전 처리
    response = await call_next(request)

    # 2. 라우터 처리 후 응답이 나가기 전 처리
    return response

# 여기서 중요한 것
# request

# 클라이언트가 보낸 요청 정보.

# call_next(request)

# 다음 단계로 요청을 넘기는 함수야.
# 즉, 실제 API 라우터를 실행시키는 역할을 해.

# response

# 라우터 실행 결과로 만들어진 응답 객체.

# 3. 흐름 예시
@app.middleware("http")
async def sample_middleware(request: Request, call_next):
    print("1. 요청 들어옴")

    response = await call_next(request)

    print("3. 응답 나감")

    return response


@app.get("/hello")
def hello():
    print("2. 라우터 실행")
    return {"message": "hello"}

# 실행 순서:

# 1. 요청 들어옴
# 2. 라우터 실행
# 3. 응답 나감
# 4. 실무에서 자주 쓰는 예시
@app.middleware("http")
async def add_custom_header(request: Request, call_next):
    response = await call_next(request)
    response.headers["X-App-Name"] = "MyFastAPIApp"
    return response

# 응답 헤더에 공통 정보를 추가할 수 있어.

# 5. Spring Boot와 비교하면

# FastAPI Middleware는 Spring의 이 구조와 비슷해.
# FastAPI Middleware ≒ Spring Filter
# Spring Boot에서 요청이 Controller에 도달하기 전에 Filter를 거치는 것처럼, FastAPI도 Middleware를 통해 공통 로직을 먼저 처리할 수 있어.

# Spring
# Client → Filter → Interceptor → Controller → Response

# FastAPI
# Client → Middleware → Router → Response
# 핵심 정리
# Middleware = 모든 요청/응답에 공통으로 적용되는 중간 처리 계층
# request 전처리 가능
# response 후처리 가능
# call_next(request)를 호출해야 다음 단계로 넘어감
# 대표 사용처:
# Logging, 인증, CORS, 응답 시간 측정, 공통 헤더 추가, 예외 처리

# 다음은 Logging Middleware로 가면 돼.