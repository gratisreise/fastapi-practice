# ✅ 1. Request 객체 (1단계)
# ✔ 1. 개념 (면접용 한 줄)

# 👉 클라이언트의 HTTP 요청 전체를 담는 객체 (메서드, URL, 헤더, 바디 등)

# ✔ 2. 기본 사용법
from fastapi import FastAPI, Request

app = FastAPI()

@app.get("/request-info")
async def request_info(request: Request):
    return {
        "method": request.method,
        "url": str(request.url)
    }
# ✔ 3. 핵심 속성 (무조건 암기)
# 1) 요청 메서드
# request.method
# # GET, POST, PUT, DELETE
# 2) URL 정보
# request.url
# request.base_url
# request.path_params
# 3) 헤더
# request.headers

# 👉 dict처럼 사용 가능

# 4) 쿼리 파라미터
# request.query_params
# 5) 바디 (중요)
# await request.json()
# await request.body()

# 👉 async 꼭 붙는다 (중요 포인트)

# ✔ 4. 실전 예제 (핵심)
# @app.post("/request-all")
# async def request_all(request: Request):
#     body = await request.json()

#     return {
#         "method": request.method,
#         "url": str(request.url),
#         "headers": dict(request.headers),
#         "query": dict(request.query_params),
#         "body": body
#     }
# ✔ 5. 왜 중요한가 (실무 관점)

# 너 기준으로 중요한 포인트만 찍는다:

# 1) 인증 처리
# Authorization: Bearer token

# → request.headers에서 꺼냄
# → Spring의 Filter 역할 직접 구현 가능

# 2) 로깅 / 추적
# 요청 URL
# 헤더
# 사용자 정보

# 👉 APM / tracing / logging 기본

# 3) 커스텀 미들웨어 구현

# → Request 객체 기반으로 처리

# ✔ 6. FastAPI 스타일 vs Request 직접 사용
# ✔ FastAPI 방식 (권장)
# @app.get("/users")
# def get_users(q: str):
#     return q
# ✔ Request 직접 사용 (낮은 레벨)
# @app.get("/users")
# async def get_users(request: Request):
#     return request.query_params.get("q")
# 🔥 핵심 차이
# 방식	특징
# FastAPI 파라미터	자동 검증 + 타입 안정성
# Request 직접	유연하지만 수동 처리

# 👉 실무에서는 혼합 사용

# 🔥 한 줄 정리

# 👉 Request 객체 = “HTTP 요청 원본 데이터 접근용 저수준 도구”