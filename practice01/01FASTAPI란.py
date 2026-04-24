# 좋아. 그럼 1. 기본 개념은 아래 순서로 나눠서 학습하자.

# FastAPI란 무엇인가
# ASGI vs WSGI
# 동기 vs 비동기
# FastAPI의 특징
# 전체 정리 + 면접식 답변

# 먼저 FastAPI란 무엇인가부터 시작.

# 1. FastAPI란 무엇인가

# FastAPI는 Python으로 API 서버를 빠르고 명확하게 만들기 위한 웹 프레임워크다.

# 쉽게 말하면,

# 클라이언트가 요청을 보내면
# 서버가 데이터를 처리하고
# JSON 형태로 응답하는 API 서버를 만드는 도구

# 라고 보면 된다.

# 예를 들어 프론트엔드에서 이런 요청을 보낸다.

# GET /users/1

# FastAPI 서버는 이 요청을 받아서 이런 응답을 줄 수 있다.

# {
#   "id": 1,
#   "name": "Kim"
# }
# FastAPI의 위치

# 백엔드 개발 관점에서 비교하면 이렇게 보면 된다.

# 언어	프레임워크
# Java	Spring Boot
# Python	FastAPI
# JavaScript	Express, NestJS
# Ruby	Rails
# PHP	Laravel

# 즉, FastAPI는 Python 생태계에서 Spring Boot처럼 API 서버를 만들 때 쓰는 프레임워크라고 보면 된다.

# 왜 FastAPI를 쓰는가?

# FastAPI는 특히 이런 용도에 많이 쓴다.

# 용도	설명
# REST API 서버	일반적인 백엔드 API
# LLM API 서버	모델 호출 API 제공
# RAG 서버	벡터 검색 + LLM 응답
# AI 추론 서버	ML/DL 모델 서빙
# 내부 관리 API	배치, 관리자, 자동화 API

# 특히 요즘은 LLM 서비스, AI 모델 서빙, RAG 서버에서 많이 사용된다.

# 아주 간단한 코드
# from fastapi import FastAPI

# app = FastAPI()

# @app.get("/hello")
# def hello():
#     return {"message": "Hello FastAPI"}

# 이 코드는 /hello로 요청이 오면 JSON을 반환한다.

# {
#   "message": "Hello FastAPI"
# }