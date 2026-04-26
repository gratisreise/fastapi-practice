# ✅ 2. Response 객체
# ✔ 1. 개념 (한 줄)

# 👉 서버가 클라이언트에게 보내는 HTTP 응답을 직접 제어하는 객체

# ✔ 2. 기본 사용
# from fastapi import FastAPI, Response

# app = FastAPI()

# @app.get("/response")
# def response_example(response: Response):
#     response.headers["X-Custom"] = "hello"
#     return {"message": "ok"}

# 👉 return 값은 그대로 JSON
# 👉 response 객체로는 부가 정보 제어

# ✔ 3. 핵심 제어 요소 (중요)
# 1) 상태 코드 변경
# response.status_code = 201
# 2) 헤더 설정
# response.headers["X-Token"] = "abc123"
# 3) 쿠키 설정
# response.set_cookie(key="access_token", value="token123")

# 👉 인증/세션에서 핵심

# ✔ 4. Response vs return 차이
# ✔ 일반 return
# return {"msg": "ok"}

# 👉 FastAPI가 자동으로 JSON 변환

# ✔ Response 객체 사용
# def test(response: Response):
#     response.status_code = 202
#     return {"msg": "accepted"}

# 👉 “응답의 메타데이터만 커스터마이징”

# ✔ 5. 완전 제어 (고급)
# from fastapi import Response

# @app.get("/raw")
# def raw_response():
#     return Response(
#         content="plain text",
#         media_type="text/plain",
#         status_code=200
#     )

# 👉 JSON이 아닌 응답도 가능

# ✔ 6. 실무 핵심 포인트
# 1) 인증 (쿠키 vs 헤더)
# response.set_cookie("refresh_token", "xxx", httponly=True)

# 👉 JWT Refresh Token 저장할 때 많이 씀

# 2) 상태 코드 설계
# POST → 201
# DELETE → 204

# 👉 REST 설계 능력 핵심 평가 포인트

# 3) 헤더 기반 제어
# response.headers["Cache-Control"] = "no-store"

# 👉 캐싱 / 보안 / CDN 제어

# ✔ 7. FastAPI 응답 구조 흐름
# return 데이터
#    ↓
# FastAPI 자동 변환
#    ↓
# Response 객체로 최종 응답 생성

# 👉 Response는 “마지막 조작 단계”

# 🔥 한 줄 정리

# 👉 Response 객체 = “응답의 상태코드 / 헤더 / 쿠키를 제어하는 도구”