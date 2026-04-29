# 2. SQLAlchemy

# SQLAlchemy는 파이썬에서 가장 대표적인 ORM 라이브러리다.

# 한 줄 정의:

# 👉 DB를 Python 객체로 다루게 해주는 ORM + SQL 제어 라이브러리

# 핵심 구조 (중요)

# SQLAlchemy는 4개만 기억하면 된다.

# Engine → DB 연결
# Base → ORM 모델의 부모
# Model → 테이블 정의
# Session → DB 작업 실행
# 1. Engine (DB 연결)

# DB랑 연결하는 객체

# from sqlalchemy import create_engine

# DATABASE_URL = "sqlite:///./test.db"

# engine = create_engine(DATABASE_URL)

# 👉 의미

# "어떤 DB에 연결할지" 정의

# 예시:

# sqlite:///./test.db
# postgresql://user:pass@localhost/db
# 2. Base (ORM 부모 클래스)

# 모든 ORM 모델이 상속받는 클래스

# from sqlalchemy.orm import declarative_base

# Base = declarative_base()
# 3. Model (테이블 정의)

# 여기서부터 진짜 ORM이다.

# from sqlalchemy import Column, Integer, String

# class User(Base):
#     __tablename__ = "users"

#     id = Column(Integer, primary_key=True)
#     name = Column(String)
#     age = Column(Integer)

# 👉 해석

# User 클래스 = users 테이블
# id = PK 컬럼
# name = 문자열 컬럼
# age = 정수 컬럼
# 4. 테이블 생성
# Base.metadata.create_all(bind=engine)

# 👉 의미

# ORM 모델 → 실제 DB 테이블 생성
# 5. Session (핵심 중 핵심)

# DB 작업을 담당하는 객체

# from sqlalchemy.orm import sessionmaker

# SessionLocal = sessionmaker(bind=engine)

# db = SessionLocal()

# 👉 Session 역할

# INSERT / SELECT / UPDATE / DELETE 수행
# 트랜잭션 관리
# 전체 흐름
# Engine 생성
# → Base 생성
# → Model 정의
# → 테이블 생성
# → Session으로 DB 작업
# FastAPI에서 사용하는 구조

# 보통 이렇게 구성한다.

# database.py
# engine = create_engine(DATABASE_URL)
# SessionLocal = sessionmaker(bind=engine)
# Base = declarative_base()
# models.py
# class User(Base):
#     __tablename__ = "users"
#     id = Column(Integer, primary_key=True)
#     name = Column(String)
# main.py
# @app.post("/users")
# def create_user():
#     db = SessionLocal()
# ORM vs SQLAlchemy Core

# SQLAlchemy는 사실 2가지 방식이 있다.

# 1. ORM (우리가 쓰는 방식)
# db.add(user)
# 2. Core (SQL 직접 제어)
# from sqlalchemy import insert

# stmt = insert(User).values(name="kim")
# engine.execute(stmt)

# 👉 실무 결론

# CRUD → ORM
# 복잡 쿼리 → Core or raw SQL