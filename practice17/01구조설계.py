# 1. 왜 구조를 나누는가?

# 작은 예제에서는 보통 이렇게 작성해도 된다.

# @app.get("/users/{user_id}")
# def get_user(user_id: int):
#     user = db.query(User).filter(User.id == user_id).first()
#     return user

# 하지만 실무에서는 문제가 생긴다.

# 라우터 안에
# - 요청 처리
# - 검증
# - 비즈니스 로직
# - DB 조회
# - 예외 처리
# 가 전부 섞임

# 그러면 코드가 커질수록 유지보수가 어려워진다.

# 그래서 역할을 나눈다.

# router      → HTTP 요청/응답 담당
# service     → 비즈니스 로직 담당
# repository  → DB 접근 담당
# 2. 기본 구조
# app/
#  ├─ main.py
#  ├─ api/
#  │   └─ user_router.py
#  ├─ services/
#  │   └─ user_service.py
#  ├─ repositories/
#  │   └─ user_repository.py
#  ├─ schemas/
#  │   └─ user_schema.py
#  ├─ models/
#  │   └─ user.py
#  └─ database.py
# 3. 각 계층 역할
# Router

# 클라이언트와 직접 만나는 계층

# 역할:
# - URL 매핑
# - Path / Query / Body 받기
# - Service 호출
# - Response 반환
# @router.get("/users/{user_id}")
# def get_user(user_id: int):
#     return user_service.get_user(user_id)

# Router는 최대한 얇게 유지한다.

# Service

# 비즈니스 로직 계층

# 역할:
# - 유저가 존재하는지 확인
# - 권한 확인
# - 정책 판단
# - 여러 Repository 조합
# - 트랜잭션 흐름 관리
# def get_user(user_id: int):
#     user = user_repository.find_by_id(user_id)

#     if user is None:
#         raise HTTPException(status_code=404, detail="User not found")

#     return user

# 실무에서 가장 중요한 계층이다.

# Repository

# DB 접근 계층

# 역할:
# - select
# - insert
# - update
# - delete
# - query 작성
# def find_by_id(db: Session, user_id: int):
#     return db.query(User).filter(User.id == user_id).first()

# Repository는 “어떤 데이터를 가져올지”에 집중한다.

# 4. 전체 흐름
# Client
#   ↓
# Router
#   ↓
# Service
#   ↓
# Repository
#   ↓
# DB

# 예를 들면:

# GET /users/1

# 요청이 오면:

# 1. Router가 user_id를 받음
# 2. Service에 get_user(user_id) 호출
# 3. Service가 Repository에 DB 조회 요청
# 4. Repository가 DB에서 User 조회
# 5. Service가 존재 여부 판단
# 6. Router가 응답 반환
# 5. 예제 코드
# user_router.py
# from fastapi import APIRouter, Depends
# from sqlalchemy.orm import Session
# from app.database import get_db
# from app.services.user_service import UserService

# router = APIRouter(prefix="/users", tags=["users"])


# @router.get("/{user_id}")
# def get_user(
#     user_id: int,
#     db: Session = Depends(get_db)
# ):
#     service = UserService(db)
#     return service.get_user(user_id)
# user_service.py
# from fastapi import HTTPException
# from app.repositories.user_repository import UserRepository


# class UserService:
#     def __init__(self, db):
#         self.user_repository = UserRepository(db)

#     def get_user(self, user_id: int):
#         user = self.user_repository.find_by_id(user_id)

#         if user is None:
#             raise HTTPException(
#                 status_code=404,
#                 detail="User not found"
#             )

#         return user
# user_repository.py
# from app.models.user import User


# class UserRepository:
#     def __init__(self, db):
#         self.db = db

#     def find_by_id(self, user_id: int):
#         return (
#             self.db.query(User)
#             .filter(User.id == user_id)
#             .first()
#         )
# 6. Spring Boot 기준으로 비교하면

# 너한테 익숙한 구조로 보면 거의 이거랑 같다.

# FastAPI                    Spring Boot

# router                     controller
# service                    service
# repository                 repository
# schema                     DTO
# model                      entity
# Depends(get_db)            @Transactional / EntityManager 주입

# 즉 FastAPI에서도 실무 구조는 Spring과 비슷하게 가져갈 수 있다.

# 7. 실무에서 중요한 규칙
# Router에 비즈니스 로직 넣지 않기

# 나쁜 예:

# @router.get("/{user_id}")
# def get_user(user_id: int, db: Session = Depends(get_db)):
#     user = db.query(User).filter(User.id == user_id).first()

#     if user is None:
#         raise HTTPException(404)

#     return user

# 문제:

# 라우터가 DB도 알고
# 비즈니스 예외도 알고
# 쿼리도 알고 있음

# 좋은 예:

# @router.get("/{user_id}")
# def get_user(user_id: int, db: Session = Depends(get_db)):
#     service = UserService(db)
#     return service.get_user(user_id)

# Router는 요청을 받아 Service에게 넘기기만 한다.

# 8. 한 줄 정리
# Router는 HTTP 담당,
# Service는 비즈니스 로직 담당,
# Repository는 DB 접근 담당이다.

# 실무 FastAPI 구조는 결국 Spring Boot의 Controller-Service-Repository 구조를 Python 방식으로 옮긴 것이라고 보면 된다.