# 1. ORM 개념

# ORM(Object Relational Mapping)은
# 객체 지향 코드의 객체와 관계형 데이터베이스의 테이블을 연결해주는 기술이야.

# 쉽게 말하면,

# user = User(name="kim", age=30)

# 이런 파이썬 객체를

# INSERT INTO users (name, age) VALUES ('kim', 30);

# 이런 SQL로 직접 바꿔주는 역할을 한다고 보면 돼.

# ORM이 없으면

# 직접 SQL을 작성해야 해.

# cursor.execute(
#     "INSERT INTO users (name, age) VALUES (?, ?)",
#     ("kim", 30)
# )

# 조회도 직접 SQL로 해야 한다.

# cursor.execute("SELECT * FROM users WHERE id = ?", (1,))
# row = cursor.fetchone()

# 이 방식은 SQL을 명확히 제어할 수 있지만, 코드가 길어지고 객체 중심으로 다루기 어렵다.

# ORM을 쓰면

# 테이블을 클래스로 표현한다.

# class User:
#     id: int
#     name: str
#     age: int

# 그리고 데이터를 객체처럼 다룬다.

# user = User(name="kim", age=30)
# db.add(user)
# db.commit()

# 즉, 개발자는 SQL을 매번 직접 작성하지 않고 객체를 저장하고 조회하는 방식으로 DB를 다룰 수 있다.

# 핵심 매핑 구조
# DB 개념	Python ORM 개념
# Table	Class
# Row	Object
# Column	Attribute
# INSERT	객체 저장
# SELECT	객체 조회
# UPDATE	객체 수정
# DELETE	객체 삭제

# 예를 들면 DB에 users 테이블이 있으면 ORM에서는 보통 이렇게 표현한다.

# class User(Base):
#     __tablename__ = "users"

#     id = Column(Integer, primary_key=True)
#     name = Column(String)
#     age = Column(Integer)

# 여기서 의미는 이거야.

# User 클래스  → users 테이블
# id           → id 컬럼
# name         → name 컬럼
# age          → age 컬럼
# User 객체    → users 테이블의 한 행
# FastAPI에서 ORM을 쓰는 이유

# FastAPI는 API 서버이고, 대부분의 서비스는 데이터를 저장해야 한다.

# 예를 들어 게시글 작성 API가 있다면

# POST /posts

# 요청이 들어오고,

# {
#   "title": "첫 글",
#   "content": "내용입니다"
# }

# 이 데이터를 DB에 저장해야 한다.

# ORM을 쓰면 흐름이 이렇게 된다.

# 요청 JSON
# → Pydantic 모델로 검증
# → ORM 객체로 변환
# → DB 저장
# → 응답 반환

# 즉 FastAPI에서는 보통

# Pydantic = 요청/응답 데이터 검증용
# SQLAlchemy ORM = DB 테이블 매핑 및 저장용

# 이렇게 역할이 나뉜다.

# Pydantic 모델과 ORM 모델 차이

# 이거 중요해.

# Pydantic 모델

# API 요청/응답 검증용이다.

# class UserCreate(BaseModel):
#     name: str
#     age: int
# ORM 모델

# DB 테이블 매핑용이다.

# class User(Base):
#     __tablename__ = "users"

#     id = Column(Integer, primary_key=True)
#     name = Column(String)
#     age = Column(Integer)

# 둘 다 User처럼 생겼지만 역할이 다르다.

# Pydantic → API 데이터 검증
# ORM → DB 테이블 매핑
# ORM의 장점

# 첫째, SQL을 직접 많이 작성하지 않아도 된다.

# db.query(User).filter(User.id == 1).first()

# 둘째, 객체 중심으로 데이터를 다룰 수 있다.

# user.name = "lee"

# 셋째, DB 종류가 바뀌어도 코드 변경이 줄어든다.

# 예를 들어 SQLite에서 PostgreSQL로 바꿔도 ORM 코드 대부분은 유지할 수 있다.

# ORM의 단점

# ORM이 SQL을 대신 만들어주기 때문에, 실제 어떤 SQL이 나가는지 모르면 성능 문제가 생길 수 있다.

# 대표적으로 이런 문제가 있다.

# N+1 문제
# 불필요한 조회
# 과도한 join
# 트랜잭션 범위 관리 실패

# 그래서 ORM을 쓸 때도 SQL, 인덱스, 트랜잭션 개념은 반드시 알아야 한다.

# 한 줄 정리

# ORM은 DB 테이블을 파이썬 클래스로 매핑해서, SQL 대신 객체 중심으로 데이터를 저장·조회하게 해주는 기술이다.