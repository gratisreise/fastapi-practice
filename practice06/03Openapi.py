# 3. OpenAPI 스펙 이해

# Swagger UI / ReDoc이 자동으로 만들어지는 이유는 하나다.

# 👉 OpenAPI 스펙(JSON) 이 있기 때문

# OpenAPI란?

# OpenAPI는 REST API를 설명하는 표준 명세다.

# 한 줄 정의:

# API를 기계가 이해할 수 있도록 JSON/YAML로 정의한 문서 규격

# FastAPI에서 확인하는 방법

# FastAPI는 OpenAPI JSON을 자동 생성한다.

# http://localhost:8000/openapi.json

# 여기 들어가면 이런 구조가 나온다:

# {
#   "openapi": "3.0.2",
#   "info": {
#     "title": "FastAPI",
#     "version": "0.1.0"
#   },
#   "paths": {
#     "/users": {
#       "post": {
#         "summary": "Create User",
#         "requestBody": {...},
#         "responses": {...}
#       }
#     }
#   }
# }
# 핵심 구조 (진짜 중요)

# OpenAPI는 크게 3개만 이해하면 된다.

# 1. info
# "info": {
#   "title": "My API",
#   "version": "1.0.0"
# }

# 👉 API 기본 정보

# 2. paths (🔥 핵심)
# "paths": {
#   "/users": {
#     "post": {
#       "summary": "Create User",
#       "parameters": [],
#       "requestBody": {...},
#       "responses": {...}
#     }
#   }
# }

# 👉 모든 API 정의가 여기에 들어간다

# 구성:

# URL → HTTP Method → 상세 정의
# 3. components (재사용 구조)
# "components": {
#   "schemas": {
#     "User": {
#       "type": "object",
#       "properties": {
#         "name": {"type": "string"},
#         "age": {"type": "integer"}
#       }
#     }
#   }
# }

# 👉 DTO (Pydantic 모델)가 여기에 정의됨

# FastAPI 코드 → OpenAPI 변환 흐름

# 이거 이해하면 끝이다.

# 코드
# from fastapi import FastAPI
# from pydantic import BaseModel

# app = FastAPI()

# class User(BaseModel):
#     name: str
#     age: int

# @app.post("/users")
# def create_user(user: User):
#     return user
# 내부 변환
# @app.post("/users")
# → paths에 추가됨
# User(BaseModel)
# → components.schemas로 변환
# 타입 힌트
# → JSON Schema로 변환
# 결과 (요약)
# "paths": {
#   "/users": {
#     "post": {
#       "requestBody": {
#         "content": {
#           "application/json": {
#             "schema": {
#               "$ref": "#/components/schemas/User"
#             }
#           }
#         }
#       }
#     }
#   }
# }
# 왜 중요한가? (실무 핵심)

# OpenAPI 하나로 이게 다 된다.

# 1. Swagger UI 생성

# 👉 /docs

# 2. ReDoc 생성

# 👉 /redoc

# 3. 프론트 코드 자동 생성
# openapi-generator

# → TypeScript API client 자동 생성

# 4. API 계약 (Contract)

# 프론트/백엔드 협업 핵심

# "이 JSON 구조로 통신한다"

# 이걸 명확히 보장

# 백엔드 관점 핵심 포인트

# 너 기준으로 중요한 건 이거다:

# 1. "코드 = 문서 = 계약"

# FastAPI는

# 코드 → OpenAPI → 문서 → 테스트

# 전부 자동 연결

# 2. 타입 설계 = API 설계
# class User(BaseModel):
#     name: str
#     age: int

# 이게 곧 API 스펙이다

# 3. 스펙 기반 개발 가능

# Apidog 같은 툴과 동일한 개념

# 👉 먼저 스펙 정의 → 구현

# 한 줄 정리 (면접용)

# OpenAPI는 REST API를 JSON/YAML로 정의하는 표준 명세이며, FastAPI는 타입 힌트와 Pydantic 모델을 기반으로 이를 자동 생성하여 문서, 테스트, 클라이언트 코드 생성을 가능하게 한다.