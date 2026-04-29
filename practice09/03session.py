# 3. Session 관리

# 한 줄 정의부터 박자.

# 👉 Session은 DB와의 트랜잭션을 관리하는 작업 단위 객체다.

# Session이 하는 일
# 1. DB 연결 관리 (Connection)
# 2. 트랜잭션 관리 (commit / rollback)
# 3. ORM 객체 상태 관리 (영속성)
# 기본 구조
# db = SessionLocal()

# 이 한 줄이 의미하는 것:

# "DB 작업을 시작할 준비 완료"
# Session lifecycle (중요)
# Session 생성
# → 작업 수행
# → commit or rollback
# → close

# 코드로 보면

# db = SessionLocal()

# try:
#     user = User(name="kim")
#     db.add(user)
#     db.commit()
# except:
#     db.rollback()
# finally:
#     db.close()
# 왜 Session 관리가 중요하냐

# 잘못 쓰면 바로 터진다.

# 문제 1: 커넥션 누수
# db = SessionLocal()
# # close 안함

# 👉 결과
# DB 커넥션 계속 쌓임 → 장애

# 문제 2: 트랜잭션 꼬임
# db.add(user)
# # commit 안함

# 👉 결과
# 데이터 안 들어감 or 중간 상태 유지

# 문제 3: 롤백 누락
# try:
#     db.add(user)
#     db.commit()
# except:
#     pass

# 👉 결과
# 세션 상태 깨짐 → 이후 쿼리 오류

# FastAPI에서 Session 관리 방식 (핵심 패턴)

# FastAPI에서는 직접 만들지 않는다.

# 👉 Dependency Injection (Depends) 사용

# 표준 패턴
# from sqlalchemy.orm import Session
# from fastapi import Depends

# def get_db():
#     db = SessionLocal()
#     try:
#         yield db
#     finally:
#         db.close()
# 사용
# @app.post("/users")
# def create_user(db: Session = Depends(get_db)):
#     user = User(name="kim")
#     db.add(user)
#     db.commit()
#     return user
# 이 구조의 핵심
# 요청마다 Session 생성
# → 요청 끝나면 자동 close

# 👉 즉

# Session per request 패턴
# commit vs flush (면접 포인트)
# flush
# db.flush()

# 👉 DB에 SQL 날림 (하지만 commit 안함)

# commit
# db.commit()

# 👉 실제 저장 + 트랜잭션 종료

# 예시
# user = User(name="kim")
# db.add(user)

# db.flush()
# print(user.id)  # ID 생성됨

# db.commit()
# rollback 언제 쓰냐
# try:
#     db.add(user)
#     db.commit()
# except Exception:
#     db.rollback()

# 👉 실패 시 반드시 rollback

# 객체 상태 관리 (중급 핵심)

# Session은 객체 상태를 관리한다.

# Transient → 아직 DB 없음
# Pending → add() 상태
# Persistent → DB에 존재
# Detached → Session 종료됨
# Detached 문제 예시
# db.close()
# print(user.name)

# 👉 Lazy loading이면 터진다

# 실무 핵심 패턴 3개
# 1. 요청 단위 Session
# 요청 1개 = Session 1개
# 2. 서비스 레이어에서 commit
# Controller에서는 commit 안하는 구조도 많음
# 3. 읽기/쓰기 분리
# 조회 → read-only session
# 쓰기 → write session
# 너 기준 (백엔드 관점 핵심 포인트)

# 이건 꼭 기억해라

# Session = 트랜잭션 경계

# Spring 기준으로 보면

# @Transactional 범위랑 동일한 개념
# 한 줄 정리

# 👉 Session은 DB 트랜잭션과 연결을 관리하는 핵심 객체이며, FastAPI에서는 요청 단위로 생성/종료하는 패턴을 사용한다.