# 1. Pydantic 모델이란?

# FastAPI에서 요청 데이터의 구조를 정의하고 검증하는 모델이야.

# 쉽게 말하면,

# “클라이언트가 보내는 JSON 데이터는 이런 형태여야 해”

# 라고 정해두는 클래스야.

# 예를 들어 회원가입 API가 있다고 해보자.

# {
#   "name": "kim",
#   "age": 25,
#   "email": "test@example.com"
# }

# 이런 데이터를 받을 때 FastAPI는 그냥 dict로 받는 게 아니라, Pydantic 모델로 받을 수 있어.

# from pydantic import BaseModel

# class UserCreate(BaseModel):
#     name: str
#     age: int
#     email: str

# 여기서 UserCreate가 Pydantic 모델이야.

# FastAPI에서 사용하는 예시
from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()

class UserCreate(BaseModel):
    name: str
    age: int
    email: str

@app.post("/users")
def create_user(user: UserCreate):
    return user

# 클라이언트가 POST /users로 아래 JSON을 보내면

# {
#   "name": "kim",
#   "age": 25,
#   "email": "test@example.com"
# }

# FastAPI가 자동으로 검증해줘.

# 핵심 동작

# Pydantic 모델을 쓰면 FastAPI가 자동으로 해주는 것들이 있어.

# 기능	설명
# JSON → 객체 변환	요청 JSON을 UserCreate 객체로 변환
# 타입 검증	age가 int인지 확인
# 필수값 검증	name, age, email이 있는지 확인
# 에러 응답 자동 생성	잘못된 요청이면 422 응답
# Swagger 문서 자동 반영	요청 Body 스키마 자동 생성
# 잘못된 요청 예시
# {
#   "name": "kim",
#   "age": "abc",
#   "email": "test@example.com"
# }

# age는 int여야 하는데 "abc"가 들어왔기 때문에 FastAPI가 자동으로 에러를 반환해.

# {
#   "detail": [
#     {
#       "loc": ["body", "age"],
#       "msg": "Input should be a valid integer",
#       "type": "int_parsing"
#     }
#   ]
# }
# Spring Boot랑 비교하면

# Spring Boot에서 DTO + Validation을 쓰는 것과 비슷해.

# public class UserCreateRequest {
#     private String name;
#     private Integer age;
#     private String email;
# }

# FastAPI에서는 이 DTO 역할을 Pydantic 모델이 한다고 보면 돼.

# class UserCreate(BaseModel):
#     name: str
#     age: int
#     email: str
# 정리

# Pydantic 모델은 FastAPI에서

# 요청 Body의 구조를 정의하고, 타입과 필수값을 자동 검증하는 DTO 같은 역할