# 좋다. 이제 멀티 워커는 FastAPI 운영에서 핵심이다.
# 백엔드 면접에서도 자주 나온다.

# 1. 멀티 워커란?
# 여러 개의 프로세스를 띄워서 동시에 요청을 처리하는 구조
# 싱글 워커
# uvicorn main:app

# 구조:

# Client → [Uvicorn 1개] → FastAPI

# 👉 한 번에 처리 가능한 요청 수가 제한됨

# 멀티 워커
# gunicorn main:app -k uvicorn.workers.UvicornWorker -w 4

# 구조:

# Client
#   ↓
# Gunicorn
#   ↓
# Worker1
# Worker2
# Worker3
# Worker4
#   ↓
# FastAPI

# 👉 동시에 여러 요청 처리 가능

# 2. 왜 멀티 워커가 필요한가?
# 1) CPU 활용

# Python은 Global Interpreter Lock 때문에
# 하나의 프로세스에서는 CPU를 100% 활용 못함

# 👉 해결:

# 프로세스를 여러 개 띄운다
# 2) 동시 요청 처리
# 사용자 100명 요청
# → 워커 1개: 대기 발생
# → 워커 4개: 병렬 처리
# 3) 장애 대응
# Worker 1 죽음
# → Gunicorn이 재시작
# → 서비스 유지
# 3. 워커 개수 설정 기준 (중요🔥)

# 가장 많이 쓰는 공식:

# CPU 코어 수 × 2 + 1

# 예:

# CPU	워커 수
# 2코어	5
# 4코어	9
# 8코어	17
# 왜 이렇게?
# CPU 작업 + I/O 대기 시간 커버

# 즉:

# 한 워커가 DB 기다리는 동안
# 다른 워커가 요청 처리
# 4. FastAPI에서 멀티 워커 특징

# FastAPI는 비동기라서 이렇게 오해 많이 함 👇

# "비동기니까 워커 1개면 충분한 거 아님?"

# 👉 ❌ 틀림

# 이유
# 1) CPU 작업은 async로 해결 안됨
# # CPU 작업 (이미지 처리, AI, 계산)

# 👉 async 효과 없음 → 워커 필요

# 2) 완전 비동기 아님
# DB
# 외부 API
# 파일 처리

# 👉 중간에 blocking 발생 가능

# 3) 장애 격리
# 워커 1개 = 장애 시 전체 다운
# 워커 여러 개 = 일부만 영향
# 5. Uvicorn에서도 멀티 워커 가능
# uvicorn main:app --workers 4
# 그런데 왜 Gunicorn을 더 쓰냐?
# 구분	Uvicorn	Gunicorn
# 멀티 워커	가능	강력
# 프로세스 관리	약함	강력
# 장애 복구	없음	자동 재시작
# 운영 안정성	낮음	높음

# 👉 그래서 실무는:

# Gunicorn + Uvicorn Worker
# 6. 실무 구조 (중요🔥)
# gunicorn main:app \
#   -k uvicorn.workers.UvicornWorker \
#   -w 4

# 구조:

# Gunicorn (Master)
#   ↓
# Worker 1 (Uvicorn)
# Worker 2 (Uvicorn)
# Worker 3 (Uvicorn)
# Worker 4 (Uvicorn)
# 7. 멀티 워커 사용 시 주의사항 (진짜 중요🔥)
# 1) 메모리 공유 안됨
# 각 워커는 독립 프로세스

# 👉 문제:

# global_count += 1  ❌

# 👉 해결:

# Redis
# DB
# 2) 캐시 문제
# 워커마다 캐시 따로 존재

# 👉 해결:

# Redis 사용
# 3) 세션/상태 문제
# 로그인 상태

# 👉 해결:

# JWT / Redis 세션
# 4) DB 커넥션 수 증가
# 워커 4개 → DB 커넥션 4배

# 👉 반드시:

# connection pool 설정 필요
# 8. 언제 워커를 늘려야 하나?

# 다음 상황이면 늘린다:

# CPU 사용률 높음
# 요청 대기 발생
# 응답 지연
# 9. 언제 줄여야 하나?
# 메모리 부족
# DB 과부하
# 10. 한 줄 정리
# 멀티 워커는 여러 프로세스를 띄워 병렬 요청 처리, CPU 활용, 장애 격리를 가능하게 하는 운영 핵심 전략이다.
# 11. 면접용 1분 답변
# FastAPI는 비동기 기반이지만, Python의 GIL로 인해 단일 프로세스에서는 CPU 활용에 한계가 있습니다. 
# 그래서 운영 환경에서는 Gunicorn을 통해 여러 Uvicorn 워커를 띄워 멀티 프로세스로 구성합니다.

# 이를 통해 동시에 여러 요청을 처리할 수 있고, 특정 워커 장애 시에도 다른 워커가 요청을 처리하여 서비스 안정성을 확보할 수 있습니다.

# 다만 워커 간 메모리 공유가 되지 않기 때문에 Redis나 DB를 활용한 상태 관리가 필요합니다.

# 다음 단계 ㄱㄱ👇