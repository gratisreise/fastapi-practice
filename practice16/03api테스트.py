# 3. API 테스트
# ✔️ 한 줄 정의

# TestClient로 API를 호출하고 pytest로 결과를 검증하는 것

# ✔️ 기본 구조 (실무 템플릿)
# from fastapi.testclient import TestClient
# from main import app

# client = TestClient(app)

# def test_api():
#     response = client.get("/hello")

#     assert response.status_code == 200
#     assert response.json() == {"msg": "hello"}
# ✔️ 1. POST (생성 API)
# def test_create_user():
#     response = client.post(
#         "/users",
#         json={"name": "jung"}
#     )

#     assert response.status_code == 200
#     assert response.json()["name"] == "jung"
# ✔️ 2. GET (조회 API)
# def test_get_user():
#     response = client.get("/users/1")

#     assert response.status_code == 200
# ✔️ 3. Query Parameter
# def test_query():
#     response = client.get("/items", params={"limit": 10})

#     assert response.status_code == 200
# ✔️ 4. Header (인증 포함)
# def test_auth():
#     response = client.get(
#         "/me",
#         headers={"Authorization": "Bearer test-token"}
#     )

#     assert response.status_code == 200
# ✔️ 5. 실패 케이스 (중요)

# 👉 이거 안 하면 테스트 의미 없음

# def test_not_found():
#     response = client.get("/users/999")

#     assert response.status_code == 404
# ✔️ 6. 응답 검증 패턴 (실무 핵심)
# def test_response():
#     response = client.get("/users/1")

#     data = response.json()

#     assert response.status_code == 200
#     assert "id" in data
#     assert data["name"] == "jung"
# ✔️ 7. 전체 흐름 (중요)
# client 요청
#    ↓
# FastAPI 라우팅
#    ↓
# 비즈니스 로직 실행
#    ↓
# Response 생성
#    ↓
# pytest assert 검증

# 👉 즉
# 컨트롤러 + 검증 + 응답까지 전부 테스트

# ✔️ 실무에서 꼭 하는 것
# 성공 케이스
# 실패 케이스 (404 / 400 / 401)
# 인증 테스트
# 데이터 검증
# ✔️ 너 스타일 한 줄 정리

# "API 테스트는 TestClient로 실제 HTTP 요청 흐름을 실행하고 pytest로 응답 상태와 데이터를 검증하는 방식입니다."