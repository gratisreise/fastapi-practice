# 1. Hello World API
# 코드
from fastapi import FastAPI

app = FastAPI()

@app.get("/")
def read_root():
    return {"message": "Hello World"}

# 2. 코드 해석 (핵심만)
# 1) FastAPI 객체 생성
app = FastAPI()

# → 이게 서버의 진입점 (Application)

# 2) 라우팅
# @app.get("/")

# → HTTP GET 요청을 / 경로로 받는다

# Spring으로 보면:

# @GetMapping("/")
# 3) 핸들러 함수
# def read_root():

# → 요청 들어오면 실행되는 함수

# 4) 응답
# return {"message": "Hello World"}

# → JSON으로 자동 변환됨

# 응답:

# {
#   "message": "Hello World"
# }
# 3. 실행
# uvicorn main:app --reload

# 실행하면:

# http://127.0.0.1:8000

# 접속 → 결과:

# {"message": "Hello World"}
# 4. 자동 문서 (FastAPI 핵심 장점)

# FastAPI는 Swagger 자동 생성됨

# http://127.0.0.1:8000/docs
# http://127.0.0.1:8000/redoc

# 여기 들어가면 API 테스트 가능

# 5. 백엔드 개발자 관점 비교 (Spring)

# FastAPI:

# @app.get("/")
# def read_root():
#     return {"message": "Hello World"}

# Spring:

# @GetMapping("/")
# public Map<String, String> hello() {
#     return Map.of("message", "Hello World");
# }

# 👉 거의 동일한 역할

# 6. 한 줄 정리
# FastAPI에서 Hello World는 GET / 요청을 받아 JSON을 반환하는 가장 기본 API다.