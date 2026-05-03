# 1. TestClient
# ✔️ 한 줄 정의

# FastAPI 앱을 실제 서버 실행 없이 HTTP 요청으로 테스트하는 도구

# ✔️ 왜 중요하냐 (실무 관점)

# 너 기준으로 말해준다 👇

# 컨트롤러(API) 테스트 = Spring의 MockMvc 같은 역할
# CI/CD에서 자동 테스트 가능
# 실제 요청 흐름 검증 가능 (routing + validation + response까지)
# ✔️ 기본 구조 (필수 암기)
# from fastapi import FastAPI
# from fastapi.testclient import TestClient

# app = FastAPI()

# @app.get("/hello")
# def hello():
#     return {"msg": "hello"}

# client = TestClient(app)

# def test_hello():
#     response = client.get("/hello")

#     assert response.status_code == 200
#     assert response.json() == {"msg": "hello"}
# ✔️ 동작 흐름 (중요)
# client.get("/hello")
#     ↓
# FastAPI 라우터 실행
#     ↓
# 핸들러 함수 실행
#     ↓
# Response 생성
#     ↓
# response 객체 반환

# 👉 즉, 실제 서버 없이 내부에서 요청 처리 전체를 돌린다

# ✔️ 지원 메서드
# client.get()
# client.post()
# client.put()
# client.delete()
# client.patch()
# ✔️ 요청 데이터 보내기
# 1. JSON Body
# response = client.post(
#     "/users",
#     json={"name": "jung"}
# )
# 2. Query Param
# response = client.get("/items?limit=10")

# 또는

# response = client.get("/items", params={"limit": 10})
# 3. Header
# response = client.get(
#     "/secure",
#     headers={"Authorization": "Bearer token"}
# )
# ✔️ Response 다루기
# response.status_code
# response.json()
# response.text
# response.headers
# ✔️ 실패 케이스 테스트 (중요)
# def test_not_found():
#     response = client.get("/not-exist")
#     assert response.status_code == 404

# 👉 이거 안 하면 테스트 의미 없음

# ✔️ 핵심 포인트 (면접용)
# 서버 실행 없이 API 테스트 가능
# 실제 HTTP 흐름을 그대로 시뮬레이션
# FastAPI 내부 ASGI 앱을 직접 호출
# 빠르고 독립적인 테스트 가능
# ✔️ 너 스타일 한 줄 정리

# "TestClient는 FastAPI의 ASGI 앱을 직접 호출해서 실제 HTTP 요청처럼 API를 테스트하는 도구입니다."