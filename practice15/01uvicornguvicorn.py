# 1. Uvicorn이란?

# Uvicorn은 FastAPI 앱을 직접 실행하는 ASGI 서버입니다.

# uvicorn main:app --reload

# FastAPI에서 자주 쓰던 이 명령어가 바로 Uvicorn 실행입니다.

# # main.py
# from fastapi import FastAPI

# app = FastAPI()

# @app.get("/")
# def hello():
#     return {"message": "hello"}
# uvicorn main:app

# 의미는 다음과 같습니다.

# main:app
# 구분	의미
# main	main.py 파일
# app	FastAPI 객체 이름

# 즉, main.py 안에 있는 app 객체를 Uvicorn으로 실행한다는 뜻입니다.

# 2. Gunicorn이란?

# Gunicorn은 Python 웹 서버 관리자 역할을 하는 WSGI 서버입니다.

# 정확히 말하면 Gunicorn 자체는 원래 WSGI 서버입니다.

# 하지만 FastAPI는 ASGI 기반이므로 Gunicorn만으로 직접 실행하기보다는 보통 이렇게 사용합니다.

# gunicorn main:app -k uvicorn.workers.UvicornWorker

# 여기서 핵심은 -k uvicorn.workers.UvicornWorker입니다.

# 즉,

# Gunicorn이 프로세스들을 관리하고
# 각 프로세스 내부에서는 Uvicorn Worker가 FastAPI를 실행한다

# 는 구조입니다.

# 3. 둘의 역할 차이
# 구분	Uvicorn	Gunicorn
# 역할	FastAPI 앱 실행	워커 프로세스 관리
# 서버 타입	ASGI 서버	WSGI 서버 / 프로세스 매니저
# 개발 환경	자주 사용	거의 안 씀
# 운영 환경	단독 사용 가능	Uvicorn Worker와 함께 자주 사용
# 멀티 프로세스 관리	가능하지만 제한적	강함
# 장애 대응	단순	워커 재시작, 프로세스 관리에 강함
# 4. 쉽게 비유하면
# Uvicorn 단독 실행
# FastAPI 앱을 실행하는 엔진
# uvicorn main:app

# 구조:

# Client
#   ↓
# Uvicorn
#   ↓
# FastAPI
# Gunicorn + Uvicorn Worker
# Gunicorn = 매니저
# Uvicorn Worker = 실제 일하는 서버
# FastAPI = 애플리케이션
# gunicorn main:app -k uvicorn.workers.UvicornWorker -w 4

# 구조:

# Client
#   ↓
# Gunicorn
#   ↓
# Uvicorn Worker 1
# Uvicorn Worker 2
# Uvicorn Worker 3
# Uvicorn Worker 4
#   ↓
# FastAPI
# 5. 왜 Gunicorn을 같이 쓰는가?

# 운영 환경에서는 하나의 서버 프로세스만 띄우면 위험합니다.

# 예를 들어 Uvicorn 하나만 실행 중인데 장애가 나면:

# Uvicorn 프로세스 종료
# → FastAPI 서비스 중단

# 하지만 Gunicorn을 사용하면:

# Worker 하나 죽음
# → Gunicorn이 감지
# → Worker 재시작
# → 서비스 지속

# 그래서 운영에서는 Gunicorn이 다음 역할을 합니다.

# 기능	설명
# 멀티 워커 실행	여러 프로세스로 요청 처리
# 워커 재시작	죽은 프로세스 자동 복구
# 타임아웃 관리	오래 걸리는 요청 제한
# graceful restart	배포 시 부드럽게 재시작
# 프로세스 관리	운영 안정성 향상
# 6. 개발 환경에서는?

# 개발할 때는 보통 Uvicorn만 씁니다.

# uvicorn main:app --reload

# --reload는 코드 변경 시 자동 재시작입니다.

# 코드 수정
# → Uvicorn 감지
# → 서버 자동 재시작

# 개발 환경에서는 빠른 피드백이 중요하므로 Gunicorn까지 쓸 필요가 거의 없습니다.

# 7. 운영 환경에서는?

# 운영에서는 보통 아래처럼 사용합니다.

# gunicorn main:app \
#   -k uvicorn.workers.UvicornWorker \
#   -w 4 \
#   -b 0.0.0.0:8000

# 옵션 의미:

# 옵션	의미
# main:app	main.py의 app 객체 실행
# -k uvicorn.workers.UvicornWorker	Uvicorn Worker 사용
# -w 4	워커 프로세스 4개 실행
# -b 0.0.0.0:8000	8000번 포트로 외부 요청 수신
# 8. 실무 기준 정리
# 개발 환경
# uvicorn main:app --reload

# 사용 이유:

# 빠른 실행
# 자동 리로드
# 디버깅 편함
# 운영 환경
# gunicorn main:app -k uvicorn.workers.UvicornWorker -w 4

# 사용 이유:

# 멀티 워커
# 장애 복구
# 프로세스 관리
# 안정적인 운영
# 9. 주의할 점

# FastAPI는 ASGI 기반입니다.

# 그래서 Gunicorn만 이렇게 실행하면 안 됩니다.

# gunicorn main:app

# 이 방식은 FastAPI에 적합하지 않습니다.

# 반드시 Uvicorn Worker를 지정해야 합니다.

# gunicorn main:app -k uvicorn.workers.UvicornWorker
# 10. 한 줄 정리
# Uvicorn은 FastAPI를 직접 실행하는 ASGI 서버이고,
# Gunicorn은 운영 환경에서 여러 Uvicorn Worker를 관리하는 프로세스 매니저 역할을 한다.

# 면접식으로 말하면:

# 개발 환경에서는 Uvicorn을 단독으로 사용하고,
# 운영 환경에서는 Gunicorn이 여러 Uvicorn Worker를 관리하도록 구성해
# 멀티 프로세스 처리와 장애 복구 측면의 안정성을 확보합니다.