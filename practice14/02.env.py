# 14-2. .env (환경 변수 파일)

# .env는 환경 변수를 파일로 관리하는 방식이야.
# 개발할 때 가장 많이 쓰는 방법이다.

# 왜 .env를 쓰는가?

# 원래 환경 변수는 이렇게 설정해야 한다:

# export DATABASE_URL=postgresql://user:pass@localhost:5432/app
# export JWT_SECRET_KEY=my-secret

# 문제:

# 1. 매번 입력해야 함
# 2. 관리하기 불편함
# 3. 협업 시 공유 어려움

# 그래서 .env 파일로 관리한다.

# 기본 구조

# 프로젝트 루트에 .env 파일 생성

# .env

# 내용:

# DATABASE_URL=postgresql://user:pass@localhost:5432/app
# JWT_SECRET_KEY=my-secret-key
# DEBUG=true
# PORT=8000
# FastAPI에서 .env 사용 방법 (핵심)
# 방법 1: pydantic-settings (🔥 실무 표준)
# from pydantic_settings import BaseSettings

# class Settings(BaseSettings):
#     database_url: str
#     jwt_secret_key: str
#     debug: bool = False

#     class Config:
#         env_file = ".env"

# settings = Settings()

# 이 한 줄이 핵심:

# env_file = ".env"

# 👉 .env 파일 자동 로딩

# 동작 원리
# .env → 환경 변수로 로드 → Settings 클래스에 매핑

# 예:

# DEBUG=true
# settings.debug  # → True (자동 boolean 변환)
# FastAPI 적용 예시
# from fastapi import FastAPI
# from pydantic_settings import BaseSettings

# class Settings(BaseSettings):
#     app_name: str = "My App"
#     database_url: str
#     debug: bool = False

#     class Config:
#         env_file = ".env"

# settings = Settings()

# app = FastAPI(title=settings.app_name)

# @app.get("/")
# def root():
#     return {"debug": settings.debug}
# .env 파일 주의사항 (🔥 중요)
# 1. Git에 올리면 안됨
# .env

# 반드시 .gitignore에 추가:

# .env

# 이유:

# API KEY / DB 비밀번호 유출됨
# 2. .env.example 만들어라 (실무 필수)
# DATABASE_URL=
# JWT_SECRET_KEY=
# DEBUG=

# 👉 실제 값 없이 구조만 공유

# 3. 문자열 따옴표 주의
# # ❌ 이렇게 하지 말 것
# DEBUG="true"

# # ✅ 이렇게
# DEBUG=true
# 4. 공백 주의
# # ❌
# DEBUG = true

# # ✅
# DEBUG=true
# python-dotenv (대안)

# pydantic 안 쓰는 경우:

# pip install python-dotenv
# from dotenv import load_dotenv
# import os

# load_dotenv()

# db_url = os.getenv("DATABASE_URL")
# 언제 .env 쓰고 언제 안 쓰냐?
# 개발(local) → .env 사용
# 운영(prod) → 실제 OS 환경 변수 or 클라우드 설정 사용

# 예:

# AWS / Docker / Kubernetes → 환경 변수로 직접 주입
# 한 줄 정리

# .env는 개발 환경에서 환경 변수를 파일로 쉽게 관리하기 위한 도구이고,
# FastAPI에서는 BaseSettings + env_file 조합이 실무 표준이다.