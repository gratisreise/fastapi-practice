# 1. 작업 비동기 처리 한 줄 정의

# 👉 시간이 오래 걸리는 작업을 요청 흐름과 분리해서 처리하는 것

# 2. 왜 필요하냐 (핵심 이유 3개)
# 1) 응답 속도 개선
# 사용자 요청 → 바로 응답
# 무거운 작업 → 뒤에서 처리
# 2) 시스템 안정성
# 외부 API (LLM, 결제 등) 느려도 영향 최소화
# 3) 확장성
# Worker 늘려서 처리량 증가 가능
# 3. 처리 방식 3단계 (중요🔥)
# 1단계: 단순 비동기 (초급)
# 방법
# async/await
# FastAPI BackgroundTasks
# 특징
# 같은 서버에서 실행
# 간단하지만 한계 있음
# 2단계: 프로세스 분리 (중급)
# 방법
# 큐 + Worker

# 대표 도구:

# Redis Queue
# Celery
# [API 서버]
#    ↓
# [Queue]
#    ↓
# [Worker 서버]

# 👉 가장 많이 쓰는 구조

# 3단계: 이벤트 기반 (고급)
# 방법
# Kafka / RabbitMQ

# 👉 마이크로서비스 구조

# 서비스 A → 이벤트 발행 → 메시지 브로커 → 서비스 B 처리
# 4. FastAPI 기준 구조 비교
# ❌ BackgroundTasks (한계 있음)
# @app.post("/task")
# def task(background_tasks: BackgroundTasks):
#     background_tasks.add_task(do_something)
#     return {"ok": True}

# 👉 문제

# 재시도 없음
# 실패 관리 없음
# 서버 죽으면 작업 날아감
# ✅ 실무 구조 (추천🔥)
# Client 요청
#    ↓
# FastAPI
#    ↓
# Redis Queue
#    ↓
# Worker (Celery)
#    ↓
# DB 저장
# 5. 코드 예시 (Celery 구조 핵심)
# 1) Worker
# from celery import Celery

# celery = Celery("worker", broker="redis://localhost:6379")

# @celery.task
# def process_task(data):
#     print("작업 처리:", data)
# 2) FastAPI
# @app.post("/task")
# def create_task():
#     process_task.delay("hello")
#     return {"status": "queued"}

# 👉 핵심

# .delay() = 비동기 큐 전송
# 6. 너 기준 (Spring 경험 연결🔥)
# 개념	FastAPI	Spring
# 간단 비동기	BackgroundTasks	@Async
# 큐 기반 처리	Celery	RabbitMQ
# 이벤트 기반	Kafka	Kafka
# 배치	APScheduler	Spring Batch
# 7. 언제 어떤 걸 쓰냐 (면접 핵심🔥)
# ✅ BackgroundTasks
# 로그
# 간단 알림
# ✅ Celery / Queue
# 이메일
# 이미지 처리
# LLM 요청
# ✅ Kafka / RabbitMQ
# 서비스 간 이벤트
# 대규모 시스템
# 8. LLM / AI 기준 (너한테 핵심🔥)

# 👉 절대 이렇게 하면 안됨

# API → LLM 직접 호출 (X)

# 👉 이렇게 가야됨

# API
#  → 요청 저장
#  → Queue push
#  → Worker가 LLM 호출
#  → 결과 저장
# 9. 한 줄 정리 (면접용)

# 👉
# "작업 비동기 처리는 요청-응답 흐름에서 시간이 오래 걸리는 작업을 분리하여 시스템의 응답성과 안정성을 높이기 위한 구조이며, 단순한 경우는 BackgroundTasks, 실무에서는 큐 기반 Worker 구조를 사용합니다."