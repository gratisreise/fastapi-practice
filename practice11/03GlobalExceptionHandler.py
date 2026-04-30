# 11-3. Global Exception Handler (전역 예외 처리)

# Middleware, Logging까지 왔으면 이제 실무 핵심 3번째 축이야.

# Middleware → Logging → Exception Handling
# 1. 왜 필요한가?

# 예외를 그대로 두면 이런 응답이 나감:

# {
#   "detail": "Internal Server Error"
# }

# 문제:

# 에러 구조가 제각각
# 클라이언트에서 처리 어려움
# 디버깅 힘듦

# 👉 그래서 에러 응답을 표준화해야 함

# 2. 기본 구조

# FastAPI에서는 @app.exception_handler로 처리함.

# from fastapi import FastAPI, Request
# from fastapi.responses import JSONResponse

# app = FastAPI()

# @app.exception_handler(Exception)
# async def global_exception_handler(request: Request, exc: Exception):
#     return JSONResponse(
#         status_code=500,
#         content={
#             "message": "서버 내부 오류",
#             "detail": str(exc)
#         }
#     )
# 3. 동작 흐름
# 요청 → 라우터 실행 → 예외 발생
# → Global Exception Handler 잡음
# → JSON 형태로 응답 반환
# 4. HTTPException 따로 처리 (중요)

# FastAPI 기본 예외인 **HTTPException**은 따로 처리하는 게 좋다.

# from fastapi import HTTPException

# @app.exception_handler(HTTPException)
# async def http_exception_handler(request: Request, exc: HTTPException):
#     return JSONResponse(
#         status_code=exc.status_code,
#         content={
#             "message": "요청 오류",
#             "detail": exc.detail
#         }
#     )
# 5. 커스텀 예외 만들기 (실무 핵심)
# class CustomException(Exception):
#     def __init__(self, message: str):
#         self.message = message
# @app.exception_handler(CustomException)
# async def custom_exception_handler(request: Request, exc: CustomException):
#     return JSONResponse(
#         status_code=400,
#         content={
#             "message": exc.message
#         }
#     )

# 사용:

# @app.get("/test")
# def test():
#     raise CustomException("잘못된 요청입니다")
# 6. 실무형 에러 구조 (추천)

# 너처럼 백엔드 설계 기준이면 이렇게 간다:

# {
#   "success": false,
#   "code": "USER_NOT_FOUND",
#   "message": "사용자를 찾을 수 없습니다"
# }

# 구현 예시:

# class AppException(Exception):
#     def __init__(self, code: str, message: str, status_code: int = 400):
#         self.code = code
#         self.message = message
#         self.status_code = status_code
# @app.exception_handler(AppException)
# async def app_exception_handler(request: Request, exc: AppException):
#     return JSONResponse(
#         status_code=exc.status_code,
#         content={
#             "success": False,
#             "code": exc.code,
#             "message": exc.message
#         }
#     )
# 7. Spring이랑 비교
# FastAPI Global Exception Handler ≒ Spring @ControllerAdvice

# Spring:

# @RestControllerAdvice
# @ExceptionHandler(Exception.class)

# FastAPI:

# @app.exception_handler(Exception)
# 8. Middleware vs Exception Handler 차이

# 이거 면접 포인트다.

# Middleware
# → 요청/응답 흐름 제어
# → 성능, 로그, 인증

# Exception Handler
# → 예외 발생 시 처리
# → 에러 응답 통일
# 핵심 요약
# Global Exception Handler = 모든 예외를 한 곳에서 처리하는 구조
# 핵심 포인트:
# - Exception / HTTPException 분리
# - 커스텀 예외 정의
# - 응답 포맷 표준화
# 실무 기준:
# → 에러 코드 + 메시지 구조 통일
# → 클라이언트/프론트 협업 필수 요소

# 원하면 다음 단계로