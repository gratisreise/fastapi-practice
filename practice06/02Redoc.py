# 2. ReDoc (/redoc)

# FastAPI는 Swagger UI 말고도 또 하나의 문서를 자동으로 제공한다.

# http://localhost:8000/redoc

# 여기로 들어가면 ReDoc 문서 페이지가 나온다.

# ReDoc이란?

# ReDoc은 읽기 중심(Read-only) API 문서 UI다.

# Swagger UI가 “테스트 도구” 느낌이라면
# ReDoc은 “정리된 기술 문서” 느낌이다.

# Swagger vs ReDoc 차이 (핵심)
# 구분	Swagger UI (/docs)	ReDoc (/redoc)
# 목적	API 테스트	문서 읽기
# Try it out	가능	❌ 없음
# UI	인터랙티브	깔끔/정적
# 사용 대상	개발자 테스트	협업/문서 공유
# 실제 느낌 차이
# Swagger UI
# 버튼 많음
# 바로 API 호출 가능
# 디버깅/테스트용
# ReDoc
# 문서처럼 쭉 읽는 구조
# 섹션별 정리 잘됨
# 설명 위주
# 예제 코드 동일
# from fastapi import FastAPI
# from pydantic import BaseModel

# app = FastAPI()

# class User(BaseModel):
#     name: str
#     age: int

# @app.post("/users")
# def create_user(user: User):
#     return user
# /redoc에서 보이는 것

# ReDoc에서는 다음처럼 정리된다.

# POST /users

# Request Body:
# - name: string
# - age: integer

# Response:
# - name: string
# - age: integer

# 그리고 좌측에 메뉴 트리 형태로 API들이 정리된다.

# 언제 ReDoc 쓰냐?

# 실무 기준으로 구분하면 이렇게 보면 된다.

# Swagger UI 쓰는 상황
# API 테스트
# 개발 중 디버깅
# 파라미터 확인
# ReDoc 쓰는 상황
# 팀 문서 공유
# API 명세서 전달
# 외부 고객 문서
# 커스터마이징도 가능

# FastAPI에서 문서 제목, 설명도 설정 가능하다.

# app = FastAPI(
#     title="My API",
#     description="이건 내 서비스 API 문서입니다",
#     version="1.0.0"
# )

# ReDoc에서는 이 정보가 상단에 크게 표시된다.

# 한 줄 정리

# ReDoc은 OpenAPI 스펙 기반으로 생성되는 “읽기 중심 API 문서 UI”다. (테스트 기능 없음)