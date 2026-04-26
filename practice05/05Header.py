# ✅ 5. Header 처리
# ✔ 1. 개념 (한 줄)

# 👉 HTTP 요청/응답의 메타데이터 (인증, 캐싱, 브라우저 제어 등)

# ✅ 2. 요청 헤더 받기
# ✔ 기본 방식 (FastAPI 스타일)
# from fastapi import Header

# @app.get("/header")
# def get_header(x_token: str = Header(...)):
#     return {"token": x_token}
# ✔ 특징
# 자동으로 헤더 매핑됨
# - → _ 변환됨

# 👉 예:

# X-Token → x_token
# Authorization → authorization
# ✔ 여러 헤더 받기
# @app.get("/headers")
# def get_headers(
#     user_agent: str = Header(None),
#     authorization: str = Header(None)
# ):
#     return {
#         "user_agent": user_agent,
#         "auth": authorization
#     }
# ✔ Raw 방식 (Request 객체)
# from fastapi import Request

# @app.get("/raw-header")
# async def raw_header(request: Request):
#     return dict(request.headers)
# ✅ 3. 응답 헤더 설정
# ✔ Response 객체 사용
# from fastapi import Response

# @app.get("/set-header")
# def set_header(response: Response):
#     response.headers["X-Token"] = "abc123"
#     return {"msg": "ok"}
# ✅ 4. 실무 핵심 사용 사례
# ✔ 1) 인증 (🔥 가장 중요)
# Authorization: Bearer access_token
# @app.get("/secure")
# def secure(authorization: str = Header(...)):
#     return {"token": authorization}

# 👉 JWT 인증의 핵심 흐름
# 👉 Spring Security Filter랑 동일 역할

# ✔ 2) 쿠키 기반 인증
# response.set_cookie(
#     key="refresh_token",
#     value="xxx",
#     httponly=True
# )

# 👉 Refresh Token 저장

# ✔ 3) 캐싱 제어
# response.headers["Cache-Control"] = "no-store"

# 👉 민감 데이터 캐싱 방지

# ✔ 4) CORS (브라우저 통신 핵심)
# Access-Control-Allow-Origin: *

# 👉 프론트 ↔ 백엔드 통신

# ✔ 5) 커스텀 헤더
# response.headers["X-Request-ID"] = "uuid"

# 👉 로그 추적 / 트래킹

# ✅ 5. 실무 패턴 (너 스타일 연결)
# ✔ JWT 인증 구조
# Client
#   ↓
# Header (Authorization)
#   ↓
# FastAPI (Header 읽기)
#   ↓
# 검증
#   ↓
# Response

# 👉 Spring Security Filter 체인 구조랑 동일

# ✅ 6. FastAPI vs Spring 비교
# FastAPI	Spring
# Header(...)	@RequestHeader
# Response.headers	ResponseEntity header
# Request.headers	HttpServletRequest
# 🔥 한 줄 정리

# 👉
# “Header는 인증, 캐싱, 보안 등 HTTP 메타데이터를 처리하는 핵심 요소”

# 🔥 면접용 1분 답변

# 👉
# “HTTP Header는 요청과 응답의 메타데이터를 담고 있으며, 인증 토큰 전달, 캐싱 제어, CORS 처리 등에 사용됩니다.
# FastAPI에서는 Header를 통해 요청 헤더를 받고, Response 객체를 통해 응답 헤더를 설정할 수 있습니다.
# 실무에서는 JWT 인증이나 캐싱 정책 제어에 많이 활용됩니다.”

# 🔥 전체 흐름 정리 (진짜 중요)
# Request → (Header, Body)
#         ↓
# 비즈니스 로직
#         ↓
# Response → (Status Code, Header, JSON)