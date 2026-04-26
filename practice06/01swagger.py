# 1. Swagger UI (/docs)

# FastAPI는 API를 만들면 자동으로 문서 페이지를 생성해준다.

# 기본 주소는:

# http://localhost:8000/docs

# 여기로 들어가면 Swagger UI가 나온다.

# Swagger UI란?

# Swagger UI는 내가 만든 API를 웹 화면에서 확인하고 테스트할 수 있게 해주는 문서 도구다.

# 예를 들어 FastAPI에 이런 API가 있다고 하자.

# from fastapi import FastAPI

# app = FastAPI()

# @app.get("/hello")
# def hello():
#     return {"message": "Hello FastAPI"}

# 서버 실행:

# uvicorn main:app --reload

# 브라우저 접속:

# http://localhost:8000/docs

# 그러면 /hello API가 자동으로 문서에 표시된다.

# Swagger UI에서 할 수 있는 것

# Swagger UI에서는 단순히 문서만 보는 게 아니라 직접 API 테스트도 가능하다.

# 예를 들어 /hello API를 클릭하면:

# GET /hello

# 이렇게 나오고, Try it out 버튼을 누르면 직접 요청을 보낼 수 있다.

# 응답도 바로 확인 가능하다.

# {
#   "message": "Hello FastAPI"
# }
# 왜 유용한가?

# 백엔드 개발할 때 API를 만들면 프론트엔드나 다른 개발자에게 설명해야 한다.

# 예전에는 이런 식으로 문서를 따로 작성해야 했다.

# GET /users/{user_id}
# 설명: 유저 조회 API
# Path Parameter: user_id
# Response: 유저 정보

# 그런데 FastAPI는 코드만 작성해도 자동으로 문서를 만들어준다.

# 즉,

# @app.get("/users/{user_id}")
# def get_user(user_id: int):
#     return {"user_id": user_id}

# 이 코드만으로 Swagger UI에 다음 정보가 자동 표시된다.

# GET /users/{user_id}
# user_id: integer
# 타입 힌트와 자동 문서

# FastAPI 문서 자동 생성의 핵심은 타입 힌트다.

# @app.get("/users/{user_id}")
# def get_user(user_id: int):
#     return {"user_id": user_id}

# 여기서 user_id: int라고 적었기 때문에 문서에 user_id가 정수 타입으로 표시된다.

# 만약 쿼리 파라미터가 있다면:

# @app.get("/items")
# def get_items(keyword: str, page: int = 1):
#     return {
#         "keyword": keyword,
#         "page": page
#     }

# Swagger UI에는 다음처럼 표시된다.

# keyword: string, required
# page: integer, default = 1
# Request Body도 문서화된다

# Pydantic 모델을 사용하면 요청 바디도 자동 문서화된다.

# from fastapi import FastAPI
# from pydantic import BaseModel

# app = FastAPI()

# class UserCreateRequest(BaseModel):
#     name: str
#     age: int
#     email: str

# @app.post("/users")
# def create_user(request: UserCreateRequest):
#     return request

# Swagger UI에서는 요청 바디 예시가 자동으로 나온다.

# {
#   "name": "string",
#   "age": 0,
#   "email": "string"
# }

# 즉, 프론트엔드 개발자가 어떤 JSON을 보내야 하는지 바로 알 수 있다.

# 정리

# Swagger UI는 FastAPI가 자동으로 제공하는 API 테스트 문서다.

# 핵심은 이거다.

# /docs = Swagger UI

# FastAPI는 다음 정보를 기반으로 문서를 자동 생성한다.

# 라우팅 정보
# HTTP Method
# Path Parameter
# Query Parameter
# Request Body
# Response
# 타입 힌트
# Pydantic 모델

# 한 줄로 정리하면:

# Swagger UI는 FastAPI 코드와 타입 힌트를 기반으로 자동 생성되는 API 문서이자 테스트 화면이다.