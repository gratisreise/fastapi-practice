# ✅ 3. JSON Response (자동 vs 직접 제어)
# ✔ 1. 자동 JSON 변환 (기본)
@app.get("/auto")
def auto():
    return {"message": "hello"}
# ✔ 동작
# dict → JSON 자동 변환
# 상태코드 → 기본 200
# 헤더 → 기본값
# ✔ 특징
# 가장 간단
# FastAPI 스타일 (권장 기본 방식)
# Pydantic과 궁합 좋음
# ✔ 2. 직접 JSONResponse 사용
from fastapi.responses import JSONResponse

@app.get("/manual")
def manual():
    return JSONResponse(
        content={"message": "hello"},
        status_code=200
    )
# ✔ 3. 차이 핵심 비교
# 구분	자동 return	JSONResponse
# 코드 간결성	👍 매우 좋음	👎 길어짐
# 상태코드 제어	제한적	👍 자유
# 헤더 제어	Response 필요	👍 가능
# 커스텀 응답	제한적	👍 완전 제어
# 실무 사용	기본	특정 상황
# ✔ 4. 언제 JSONResponse 써야 하냐 (실무 핵심)
# 1) 에러 응답 직접 정의할 때
# return JSONResponse(
#     content={"error": "invalid request"},
#     status_code=400
# )

# 👉 커스텀 에러 포맷 만들 때

# 2) 조건에 따라 상태코드 다를 때
# if not user:
#     return JSONResponse(
#         content={"msg": "not found"},
#         status_code=404
#     )
# 3) 응답 구조 강제 통일
# return JSONResponse(
#     content={
#         "success": True,
#         "data": data,
#         "error": None
#     }
# )

# 👉 실무에서 많이 씀 (표준 응답 포맷)

# 4) 미들웨어/공통 처리

# → 모든 응답 구조를 강제할 때

# ✔ 5. 혼동 포인트 (중요)
# ❌ 이렇게 안 해도 된다
# return JSONResponse(content=data)

# 👉 그냥 이렇게 해도 됨

# return data
# ✔ 6. 베스트 프랙티스 (실무 기준)

# 👉 기본은 무조건 이거

# return {"data": result}

# 👉 특수 상황만 JSONResponse

# 에러 커스터마이징
# 상태코드 동적 처리
# 응답 포맷 강제
# ✔ 7. 너 기준 실무 연결

# Spring 기준으로 보면:

# FastAPI	Spring
# return dict	@ResponseBody
# JSONResponse	ResponseEntity

# 👉 JSONResponse = ResponseEntity 느낌

# 🔥 한 줄 정리

# 👉
# “기본은 return dict, 제어가 필요할 때만 JSONResponse”

# 🔥 면접용 1분 답변

# 👉
# “FastAPI는 기본적으로 dict를 반환하면 자동으로 JSON으로 변환됩니다.
# 하지만 상태 코드나 응답 구조를 직접 제어해야 하는 경우에는 JSONResponse를 사용합니다.
# 실무에서는 일반 응답은 return을 사용하고, 에러 처리나 커스텀 응답이 필요한 경우 JSONResponse를 사용합니다.”