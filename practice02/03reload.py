# 3. 핫 리로드 (--reload)
# 1. 정의
# uvicorn main:app --reload

# → 코드가 변경되면 서버를 자동으로 재시작 해주는 기능

# 2. 왜 필요하냐

# 보통 서버는 이렇게 동작한다:

# 코드 수정 → 서버 재시작 → 다시 테스트

# 근데 이거 계속 반복하면 개빡셈

# 그래서:

# 코드 수정 → 자동 재시작 → 바로 반영

# 👉 이걸 --reload가 해준다

# 3. 동작 방식 (중요)

# 핫 리로드는 내부적으로:

# 파일 변경 감지 → 서버 프로세스 재시작

# 즉, “실시간 반영”이 아니라:

# 👉 재시작을 자동으로 해주는 것

# 4. 실습
# 1) 서버 실행
# uvicorn main:app --reload
# 2) 코드 수정
# @app.get("/")
# def read_root():
#     return {"message": "Hello FastAPI"}
# 3) 결과

# 브라우저 새로고침하면:

# {
#   "message": "Hello FastAPI"
# }

# 👉 서버 껐다 켤 필요 없음

# 5. 로그 보면 이해됨

# 실행하면 이런 로그 나옴:

# INFO: Started reloader process
# INFO: Started server process

# 코드 수정하면:

# INFO: Detected file change
# INFO: Reloading...

# 👉 실제로 프로세스 다시 뜸

# 6. 주의 (실무 중요)
# ❌ 운영 환경에서 쓰면 안됨
# --reload = 개발용

# 이유:

# 성능 떨어짐
# 파일 감시 비용 있음
# 안정성 낮음
# ✔ 운영 환경
# uvicorn main:app

# 또는:

# gunicorn + uvicorn worker 조합
# 7. 백엔드 개발자 관점 비교

# Spring Boot:

# spring-boot-devtools

# → 자동 재시작 기능

# FastAPI:

# uvicorn --reload

# 👉 완전히 같은 역할

# 8. 한 줄 정리
# --reload는 코드 변경 시 서버를 자동 재시작해주는 개발용 옵션이다.