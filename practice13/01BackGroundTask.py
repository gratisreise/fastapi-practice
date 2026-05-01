# 1. BackgroundTasks 개념 (핵심 한 줄)

# 👉 응답을 먼저 보내고, 뒤에서 작업을 처리하는 구조

# 2. 왜 쓰냐?

# 대표적으로 이런 케이스:

# 이메일 발송
# 로그 저장
# 이미지 처리
# AI 호출 (LLM 요청)
# 알림 전송

# 👉 공통점
# 사용자는 결과를 기다릴 필요 없음

# 3. 기본 사용법
# from fastapi import FastAPI, BackgroundTasks

# app = FastAPI()

# def write_log(message: str):
#     with open("log.txt", "a") as f:
#         f.write(message + "\n")

# @app.post("/send")
# def send(background_tasks: BackgroundTasks):
#     background_tasks.add_task(write_log, "요청 들어옴")

#     return {"message": "응답 먼저 반환"}
# 동작 흐름
# API 요청 들어옴
# add_task() 등록
# 응답 바로 반환
# 뒤에서 함수 실행
# 4. 실무 관점에서 중요한 포인트
# ❗ 오해 금지

# 👉 BackgroundTasks = "진짜 비동기 처리" 아님

# 같은 프로세스에서 실행됨
# 이벤트 루프 끝나고 실행되는 수준

# 👉 즉
# 가벼운 작업용

# 5. async/await 와의 차이
# 구분	BackgroundTasks	async/await
# 실행 시점	응답 이후	요청 중
# 목적	후처리	I/O 최적화
# 블로킹 영향	없음	있음
# 사용 예	로그, 이메일	DB 호출, API 호출
# 6. 같이 쓰는 구조 (중요🔥)
# import asyncio

# async def async_task():
#     await asyncio.sleep(3)
#     print("비동기 작업 완료")

# def wrapper():
#     asyncio.run(async_task())

# @app.get("/")
# def test(background_tasks: BackgroundTasks):
#     background_tasks.add_task(wrapper)
#     return {"ok": True}

# 👉 핵심

# BackgroundTasks 안에서 async 직접 못 씀
# wrapper 필요
# 7. 실무 아키텍처 비교 (너 기준)
# FastAPI
# BackgroundTasks → 간단 후처리
# 너가 쓰던 구조
# Redis ZSet → 스케줄링
# RabbitMQ → 비동기 이벤트
# Spring Batch → 대용량 처리

# 👉 대응 관계

# FastAPI	Spring
# BackgroundTasks	@Async
# Celery	RabbitMQ
# APScheduler	Batch
# 8. 언제 쓰고 언제 버리냐 (중요🔥)
# ✅ 써도 되는 경우
# 로그 기록
# 간단 알림
# 짧은 작업 (<1~2초)
# ❌ 쓰면 안 되는 경우
# LLM 호출 (시간 오래 걸림)
# 이미지 대량 처리
# DB heavy 작업
# 실패 재처리 필요한 작업

# 👉 이 경우는

# → Celery / Redis Queue / Kafka 가야 함

# 9. 한 줄 정리 (면접용)

# 👉
# "FastAPI의 BackgroundTasks는 응답 이후 가벼운 후처리를 위한 기능이며, 장시간 작업이나 신뢰성이 중요한 비동기 처리는 메시지 큐 기반으로 분리해야 합니다."

# 10. 너 기준 확장 포인트 (중요🔥)

# 너 지금 방향 보면:

# LLM
# Agent
# RAG

# 👉 절대 BackgroundTasks로 하면 안 됨

# 추천 구조:

# API
#  → 작업 요청 저장
#  → 메시지 큐 (Redis / Kafka)
#  → Worker (LLM 호출)
#  → 결과 저장

# 👉 이유

# retry 필요
# timeout 제어
# 비용 관리