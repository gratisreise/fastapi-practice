# 4. CRUD 구현

# 예제는 User로 간다.

# 전체 흐름
# FastAPI 요청
# → Pydantic으로 데이터 검증
# → SQLAlchemy ORM 객체 생성/조회
# → Session으로 DB 작업
# → 응답 반환
# 1. database.py
# from sqlalchemy import create_engine
# from sqlalchemy.orm import sessionmaker, declarative_base

# DATABASE_URL = "sqlite:///./test.db"

# engine = create_engine(
#     DATABASE_URL,
#     connect_args={"check_same_thread": False}
# )

# SessionLocal = sessionmaker(
#     autocommit=False,
#     autoflush=False,
#     bind=engine
# )

# Base = declarative_base()
# 2. models.py
# from sqlalchemy import Column, Integer, String
# from database import Base

# class User(Base):
#     __tablename__ = "users"

#     id = Column(Integer, primary_key=True, index=True)
#     name = Column(String, nullable=False)
#     age = Column(Integer, nullable=False)
# 3. schemas.py
# from pydantic import BaseModel

# class UserCreate(BaseModel):
#     name: str
#     age: int

# class UserUpdate(BaseModel):
#     name: str
#     age: int

# class UserResponse(BaseModel):
#     id: int
#     name: str
#     age: int

#     class Config:
#         from_attributes = True
# 4. main.py
# from fastapi import FastAPI, Depends, HTTPException
# from sqlalchemy.orm import Session

# from database import Base, engine, SessionLocal
# from models import User
# from schemas import UserCreate, UserUpdate, UserResponse

# app = FastAPI()

# Base.metadata.create_all(bind=engine)
# 5. DB Session Dependency
# def get_db():
#     db = SessionLocal()
#     try:
#         yield db
#     finally:
#         db.close()
# 6. Create
# @app.post("/users", response_model=UserResponse)
# def create_user(
#     request: UserCreate,
#     db: Session = Depends(get_db)
# ):
#     user = User(
#         name=request.name,
#         age=request.age
#     )

#     db.add(user)
#     db.commit()
#     db.refresh(user)

#     return user

# 흐름:

# 요청 데이터 받음
# → User ORM 객체 생성
# → db.add()
# → db.commit()
# → db.refresh()
# → 응답 반환

# refresh()는 DB에 저장된 최신 값을 다시 가져오는 역할이야.
# 예를 들어 자동 생성된 id 값을 객체에 반영할 때 사용한다.

# 7. Read - 단건 조회
# @app.get("/users/{user_id}", response_model=UserResponse)
# def get_user(
#     user_id: int,
#     db: Session = Depends(get_db)
# ):
#     user = db.query(User).filter(User.id == user_id).first()

#     if user is None:
#         raise HTTPException(status_code=404, detail="User not found")

#     return user
# 8. Read - 전체 조회
# @app.get("/users", response_model=list[UserResponse])
# def get_users(db: Session = Depends(get_db)):
#     users = db.query(User).all()
#     return users
# 9. Update
# @app.put("/users/{user_id}", response_model=UserResponse)
# def update_user(
#     user_id: int,
#     request: UserUpdate,
#     db: Session = Depends(get_db)
# ):
#     user = db.query(User).filter(User.id == user_id).first()

#     if user is None:
#         raise HTTPException(status_code=404, detail="User not found")

#     user.name = request.name
#     user.age = request.age

#     db.commit()
#     db.refresh(user)

#     return user

# 핵심:

# ORM 객체를 조회한 뒤
# 필드 값을 바꾸고
# commit 하면 UPDATE SQL 실행

# JPA의 dirty checking이랑 비슷하게 보면 된다.

# 10. Delete
# @app.delete("/users/{user_id}")
# def delete_user(
#     user_id: int,
#     db: Session = Depends(get_db)
# ):
#     user = db.query(User).filter(User.id == user_id).first()

#     if user is None:
#         raise HTTPException(status_code=404, detail="User not found")

#     db.delete(user)
#     db.commit()

#     return {"message": "User deleted"}
# CRUD 요약
# 기능	SQLAlchemy 코드
# 생성	db.add(user)
# 저장 확정	db.commit()
# 최신값 반영	db.refresh(user)
# 조회	db.query(User).filter(...).first()
# 전체 조회	db.query(User).all()
# 수정	객체 필드 변경 후 db.commit()
# 삭제	db.delete(user)