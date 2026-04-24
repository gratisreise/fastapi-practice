# 2. ASGI vs WSGI

# 이건 FastAPI 이해에서 핵심 중의 핵심이다.
# 왜냐면 FastAPI가 빠른 이유가 여기서 나온다.

# WSGI란?

# WSGI(Web Server Gateway Interface)는

# Python 웹 서버와 애플리케이션이 통신하는 방식 (표준)

# 이다.

# 쉽게 말하면

# 클라이언트 → 서버 → (WSGI) → Python 코드 → 응답
# 특징
# 동기 방식 (sync)
# 한 번에 하나의 요청 처리
# 요청이 끝날 때까지 블로킹
# 대표 프레임워크
# Django
# Flask
# 문제점 (왜 느린가)

# 예를 들어 이런 상황

# 요청 1 → DB 조회 (3초)
# 요청 2 → 기다림
# 요청 3 → 기다림

# 👉 하나 끝나야 다음 요청 처리됨

# 즉,

# I/O 작업(DB, API 호출)이 많으면 성능이 떨어짐

# ASGI란?

# ASGI(Asynchronous Server Gateway Interface)는

# 비동기 처리를 지원하는 새로운 Python 서버 인터페이스

# 이다.

# 특징
# 비동기 (async/await)
# 동시에 여러 요청 처리 가능
# I/O 작업 동안 다른 요청 처리 가능
# 흐름
# 요청 1 → DB 기다리는 동안
# 요청 2 처리
# 요청 3 처리

# 👉 병렬처럼 처리됨

# 대표 프레임워크
# FastAPI
# Starlette
# 핵심 비교
# 구분	WSGI	ASGI
# 방식	동기	비동기
# 처리	한 번에 하나	여러 개 동시에
# 성능	I/O에서 느림	I/O에서 강함
# 대표	Django, Flask	FastAPI
# 실무 관점 (중요)

# 너 기준으로 보면 이게 핵심이다.

# WSGI
# 전통적인 웹 서비스
# CRUD 중심
# 트래픽 적거나 단순한 서비스
# ASGI
# LLM API 호출
# 외부 API 많이 호출
# WebSocket / 실시간 처리
# AI / RAG / Agent 시스템

# 👉 즉,

# I/O 많은 서비스 = ASGI가 필수

# 한 줄 정리 (면접용)

# WSGI는 동기 기반으로 요청을 순차 처리하는 방식이고, ASGI는 비동기 기반으로 여러 요청을 동시에 처리할 수 있어 I/O 중심 서비스에서 더 높은 성능을 제공합니다.