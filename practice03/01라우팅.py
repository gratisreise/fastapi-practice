# 3. 라우팅 (Routing) 핵심 정리
# 1️⃣ HTTP Method (GET / POST / PUT / DELETE)

# FastAPI는 데코레이터로 라우팅을 정의한다.

from fastapi import FastAPI

app = FastAPI()

@app.get("/users")
def get_users():
    return {"message": "GET users"}

@app.post("/users")
def create_user():
    return {"message": "POST user"}

@app.put("/users/{user_id}")
def update_user(user_id: int):
    return {"message": f"PUT user {user_id}"}

@app.delete("/users/{user_id}")
def delete_user(user_id: int):
    return {"message": f"DELETE user {user_id}"}

# ✔️ 개념 한 줄
# GET: 조회
# POST: 생성
# PUT: 전체 수정
# DELETE: 삭제

# 2️⃣ Path Parameter

# URL 경로에 포함되는 값

@app.get("/users/{user_id}")
def get_user(user_id: int):
    return {"user_id": user_id}
# ✔️ 특징
# 타입 자동 변환 (int, str)
# 타입 틀리면 자동 422 에러
# ✔️ 예시
# GET /users/1 → user_id = 1

# 3️⃣ Query Parameter

# URL 뒤에 붙는 파라미터

@app.get("/users")
def get_users(page: int = 1, size: int = 10):
    return {
        "page": page,
        "size": size
    }
# ✔️ 특징
# 기본값 설정 가능
# 선택적 파라미터 처리 가능
# ✔️ 예시
# GET /users?page=2&size=20

# 4️⃣ Request Body (🔥 핵심)

# POST / PUT에서 사용하는 데이터

# 👉 FastAPI는 Pydantic 모델을 사용한다

from pydantic import BaseModel

class User(BaseModel):
    name: str
    age: int

@app.post("/users")
def create_user(user: User):
    return user
# ✔️ 특징
# JSON 자동 파싱
# validation 자동 처리
# 타입 기반 API 설계
# ✔️ 요청 예시
# {
#   "name": "john",
#   "age": 20
# }
# 🔥 전체 흐름 한 번에 보기
# @app.put("/users/{user_id}")
# def update_user(
#     user_id: int,        # Path
#     active: bool = True, # Query
#     user: User           # Body
# ):
#     return {
#         "user_id": user_id,
#         "active": active,
#         "user": user
#     }
# 💡 실무 관점 핵심 포인트

# 너 백엔드 기준으로 중요한 포인트만 찍어준다:

# 1. 타입 기반 API (Spring보다 강력)
# FastAPI = 타입 → validation + docs 자동 생성
# 2. Swagger 자동 생성
# /docs 들어가면 바로 테스트 가능
# 3. DTO 역할 = Pydantic
# Java → DTO
# Python → Pydantic Model
# 💬 면접 1분 답변

# FastAPI의 라우팅은 HTTP 메서드 기반으로 데코레이터를 사용해 정의하며, Path Parameter, Query Parameter, Request Body를 타입 기반으로 처리합니다. 특히 Pydantic 모델을 통해 요청 데이터를 자동 검증하고 JSON을 객체로 매핑하며, 이를 기반으로 Swagger 문서까지 자동 생성되는 것이 특징입니다.