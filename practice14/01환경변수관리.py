# 14-1. 환경 변수 관리

# 환경 변수는 코드에 직접 넣으면 안 되는 설정값을 외부에서 주입하는 방식이야.

# 예를 들면 이런 값들:

# DATABASE_URL
# JWT_SECRET_KEY
# OPENAI_API_KEY
# REDIS_HOST
# SERVER_PORT
# DEBUG
# 왜 환경 변수를 쓰는가?

# 코드에 이런 식으로 쓰면 안 좋아.

# OPENAI_API_KEY = "sk-xxxx"
# DATABASE_URL = "postgresql://user:pass@localhost:5432/app"

# 문제는:

# 1. GitHub에 올라가면 보안 사고
# 2. dev / prod 환경마다 값을 바꾸기 어려움
# 3. 배포 서버마다 설정이 달라질 수 있음
# 4. 비밀번호, API Key가 코드에 남음

# 그래서 설정값은 코드 밖으로 분리한다.

# FastAPI에서 기본 사용 방식
# 1. OS 환경 변수 읽기
# import os

# database_url = os.getenv("DATABASE_URL")
# debug = os.getenv("DEBUG", "false")
# print(database_url)
# print(debug)

# os.getenv()는 환경 변수를 읽는 기본 방식이야.

# 기본값 설정
# port = os.getenv("PORT", "8000")

# 뜻은:

# PORT 환경 변수가 있으면 그 값 사용
# 없으면 "8000" 사용
# 주의할 점

# 환경 변수는 기본적으로 문자열로 들어온다.

# debug = os.getenv("DEBUG", "false")

# 이 값은 Boolean이 아니라 문자열이야.

# print(type(debug))
# # <class 'str'>

# 그래서 직접 변환이 필요하다.

# debug = os.getenv("DEBUG", "false").lower() == "true"
# 실무에서는 Settings 클래스로 관리

# FastAPI에서는 보통 pydantic-settings를 많이 사용해.

# pip install pydantic-settings
# from pydantic_settings import BaseSettings

# class Settings(BaseSettings):
#     database_url: str
#     jwt_secret_key: str
#     debug: bool = False

# settings = Settings()

# 이렇게 하면 환경 변수를 자동으로 읽는다.

# 예를 들어 환경 변수에 아래 값이 있으면:

# DATABASE_URL=postgresql://user:pass@localhost:5432/app
# JWT_SECRET_KEY=my-secret
# DEBUG=true

# Python에서는 이렇게 사용한다.

# print(settings.database_url)
# print(settings.jwt_secret_key)
# print(settings.debug)
# FastAPI에서 사용 예시
# from fastapi import FastAPI
# from pydantic_settings import BaseSettings

# class Settings(BaseSettings):
#     app_name: str = "My FastAPI App"
#     debug: bool = False
#     database_url: str

# settings = Settings()

# app = FastAPI(title=settings.app_name)

# @app.get("/config")
# def get_config():
#     return {
#         "app_name": settings.app_name,
#         "debug": settings.debug,
#         "database_url": settings.database_url
#     }

# 실제 응답:

# {
#   "app_name": "My FastAPI App",
#   "debug": true,
#   "database_url": "postgresql://user:pass@localhost:5432/app"
# }

# 단, 실제 서비스에서는 database_url, secret_key 같은 값은 API 응답으로 노출하면 안 돼.

# 정리

# 환경 변수 관리는 한 줄로 말하면:

# 환경마다 달라지는 값과 민감한 값을 코드에서 분리해서 외부에서 주입하는 방식

# FastAPI에서는 보통:

# os.getenv()

# 또는

# pydantic-settings의 BaseSettings

# 를 사용한다.

# 실무 기준으로는 BaseSettings 방식이 더 좋다.