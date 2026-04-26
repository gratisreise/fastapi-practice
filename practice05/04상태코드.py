# ✅ 4. Status Code 설정
# ✔ 1. 개념 (한 줄)

# 👉 HTTP 요청 결과를 숫자로 표현하는 규칙

# ✔ 2. 기본 사용 (FastAPI 스타일)
# ✔ 방법 1 (가장 많이 씀)
# @app.post("/users", status_code=201)
# def create_user():
#     return {"msg": "created"}

# 👉 선언적으로 설정 (깔끔, 추천)

# ✔ 방법 2 (Response 객체)
# from fastapi import Response

# @app.get("/custom")
# def custom(response: Response):
#     response.status_code = 202
#     return {"msg": "accepted"}
# ✔ 방법 3 (JSONResponse)
# from fastapi.responses import JSONResponse

# return JSONResponse(
#     content={"msg": "error"},
#     status_code=400
# )
# ✔ 3. 상태코드 분류 (무조건 암기)
# 🔵 2xx (성공)
# 코드	의미
# 200	성공
# 201	생성 성공
# 204	성공 (응답 없음)
# 🟡 4xx (클라이언트 오류)
# 코드	의미
# 400	잘못된 요청
# 401	인증 실패
# 403	권한 없음
# 404	리소스 없음
# 🔴 5xx (서버 오류)
# 코드	의미
# 500	서버 내부 오류
# ✔ 4. 실무 기준 (이게 진짜 중요)
# ✔ CREATE (POST)
# POST /users → 201
# ✔ READ (GET)
# GET /users → 200
# GET /users/{id} → 404 (없으면)
# ✔ UPDATE (PUT / PATCH)
# PUT → 200 or 204
# ✔ DELETE
# DELETE → 204 (성공, body 없음)
# ✔ 5. 잘못 쓰는 케이스 (면접 단골 함정)
# ❌ 무조건 200 쓰는 경우

# 👉 REST 설계 능력 낮다고 평가됨

# ❌ 에러인데 200 반환
# {
#   "success": false
# }

# 👉 ❌ 절대 금지

# ✔ 6. 실무 패턴 (너 스타일 연결)

# 너처럼 백엔드 설계 기준이면 이렇게 간다:

# {
#   "success": true,
#   "data": {...},
#   "error": null
# }
# 상태코드도 같이 맞춤
# ✔ 7. FastAPI에서 예외 처리 (중요)
# from fastapi import HTTPException

# @app.get("/user/{id}")
# def get_user(id: int):
#     if id != 1:
#         raise HTTPException(status_code=404, detail="User not found")
#     return {"id": id}

# 👉 이게 실무 표준 방식

# ✔ 8. Spring이랑 비교
# FastAPI	Spring
# status_code	@ResponseStatus
# JSONResponse	ResponseEntity
# HTTPException	throw Exception
# 🔥 한 줄 정리

# 👉
# “상태코드는 API의 결과를 표현하는 규칙이며, REST 설계의 핵심이다”

# 🔥 면접용 1분 답변

# 👉
# “HTTP 상태 코드는 요청 결과를 표현하는 규칙이며 REST API 설계에서 매우 중요합니다.
# 예를 들어 생성은 201, 조회는 200, 삭제는 204를 사용하고, 에러 상황에서는 4xx, 서버 오류는 5xx를 사용합니다.
# 실무에서는 상태 코드와 응답 바디를 함께 설계하여 API의 의도를 명확히 전달하는 것이 중요합니다.”