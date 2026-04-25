# 2. 타입 힌트 기반 검증
# 개념 한 줄

# Python 타입 힌트를 기반으로 FastAPI가 자동으로 요청 데이터를 검증한다

# 왜 중요한가?

# 일반 Python은 타입이 느슨함

# def func(age):
#     return age + 1

# → age="abc" 들어와도 런타임 에러

# FastAPI는 다름

# def func(age: int):
#     return age + 1

# → 여기서 int 타입 힌트를 보고 자동 검증 + 변환 수행

# 기본 예제
# from fastapi import FastAPI

# app = FastAPI()

# @app.get("/items")
# def read_items(limit: int):
#     return {"limit": limit}
# 요청
# GET /items?limit=10

# → 정상

# GET /items?limit=abc

# → 자동 에러 발생

# 핵심 동작 (중요)

# FastAPI는 내부적으로 **Pydantic**을 사용해서:

# 타입 확인
# 타입 변환
# 에러 생성

# 을 자동으로 수행한다.

# 자동 타입 변환 (핵심 포인트)
# @app.get("/items")
# def read_items(limit: int):
#     return {"limit": limit}

# 요청:

# GET /items?limit=10

# 여기서 "10"은 문자열인데도 → int로 변환됨

# 👉 이게 중요한 이유
# → 클라이언트는 항상 문자열로 보내기 때문

# 다양한 타입 검증 예시
# 1. 기본 타입
# def test(
#     age: int,
#     price: float,
#     name: str,
#     is_active: bool
# ):
#     return {}

# 요청:

# ?age=10&price=10.5&name=kim&is_active=true

# → 전부 자동 파싱됨

# 2. bool 파싱 특징 (실무 중요)
# is_active: bool

# 가능한 값들:

# true, True, 1, yes → True
# false, False, 0, no → False

# 👉 Spring보다 유연함

# 3. Path Parameter도 동일
# @app.get("/items/{item_id}")
# def read_item(item_id: int):
#     return {"item_id": item_id}
# /items/123 → OK
# /items/abc → 에러
# 4. Request Body에서도 동일
# from pydantic import BaseModel

# class User(BaseModel):
#     age: int

# @app.post("/users")
# def create_user(user: User):
#     return user

# → JSON 안에서도 타입 검증 동일하게 동작

# 에러 응답 구조

# 타입 틀리면 자동으로 422 반환

# {
#   "detail": [
#     {
#       "loc": ["query", "limit"],
#       "msg": "Input should be a valid integer",
#       "type": "int_parsing"
#     }
#   ]
# }
# 백엔드 관점 핵심 정리

# 너 기준으로 중요한 포인트만 정리하면:

# 1. 검증 로직을 안 써도 된다
# Spring → @Valid, @NotNull, @Min 등 필요
# FastAPI → 타입 힌트만으로 1차 검증 끝
# 2. API 계약이 코드에 그대로 드러난다
# def read_items(limit: int)

# → 이 자체가 스펙

# 3. Swagger 자동 생성

# → 타입 기반으로 요청/응답 문서 자동 생성

# 4. 런타임 안정성 증가

# → 잘못된 데이터가 로직까지 안 들어옴

# 한 줄 정리

# 타입 힌트 = 검증 + 파싱 + 문서화까지 다 해주는 핵심 메커니즘