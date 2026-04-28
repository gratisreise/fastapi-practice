# 1. 한 줄 정의

# 비동기 DB 처리는 DB 응답을 기다리는 동안 서버가 다른 요청을 처리할 수 있게 하는 방식이야.

# DB 조회는 대표적인 I/O Bound 작업이라 async 효과가 크다.

# 2. 왜 필요한가?

# 동기 DB를 쓰면 이런 흐름이야.

# 요청 A → DB 조회 기다림 → 응답
# 요청 B는 그동안 대기

# 비동기 DB는 이런 흐름이야.

# 요청 A → DB 조회 요청 후 대기 양보
# 요청 B 처리
# DB 응답 오면 요청 A 재개

# 즉, DB가 느릴 때 서버 처리량을 더 잘 유지할 수 있다.

# 3. FastAPI에서 주의할 점
# ❌ 안 좋은 예
# @app.get("/users")
# async def get_users():
#     users = sync_db.query(User).all()
#     return users

# 문제는 이거야.

# async 함수 안에서 동기 DB 호출

# 이러면 async def를 써도 DB 호출이 이벤트 루프를 막아버린다.

# 4. 올바른 방식 1: Async SQLAlchemy 사용

# FastAPI에서 자주 쓰는 조합:

# FastAPI
# SQLAlchemy AsyncSession
# asyncpg
# PostgreSQL

# 예시:

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

async def get_user(user_id: int, db: AsyncSession):
    result = await db.execute(
        select(User).where(User.id == user_id)
    )
    return result.scalar_one_or_none()

# 핵심은 이거야.

# await db.execute(...)

# DB 조회 자체를 비동기로 기다린다.

# 5. DB 세션 의존성 예시
# from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker

# DATABASE_URL = "postgresql+asyncpg://user:password@localhost:5432/app"

# engine = create_async_engine(DATABASE_URL)

# AsyncSessionLocal = async_sessionmaker(
#     bind=engine,
#     expire_on_commit=False
# )
# async def get_db():
#     async with AsyncSessionLocal() as session:
#         yield session

# FastAPI 라우터에서는 이렇게 쓴다.

# from fastapi import Depends

# @app.get("/users/{user_id}")
# async def read_user(
#     user_id: int,
#     db: AsyncSession = Depends(get_db)
# ):
#     user = await get_user(user_id, db)
#     return user
# 6. 올바른 방식 2: 동기 ORM을 ThreadPool로 감싸기

# 기존 동기 DB 코드를 바로 못 바꿀 수도 있어.

# 그럴 때는:

from fastapi.concurrency import run_in_threadpool

@app.get("/users/{user_id}")
async def read_user(user_id: int):
    user = await run_in_threadpool(sync_find_user, user_id)
    return user

# 이 방식은 동기 DB 작업을 이벤트 루프 밖의 스레드에서 실행하게 한다.

# 즉:

# 이벤트 루프는 안 막음
# 대신 스레드풀 자원을 사용함
# 7. 실무 선택 기준
# 상황	추천
# 새 프로젝트	AsyncSession + asyncpg
# 기존 동기 ORM 코드 많음	run_in_threadpool
# 트래픽 많고 DB I/O 많음	Async DB 고려
# CPU 계산 많음	DB 비동기보다 worker 분리
# 8. 중요한 함정
# 함정 1. async def만 붙인다고 비동기가 아니다
# @app.get("/")
# async def api():
#     time.sleep(3)  # ❌ blocking

# 이건 이벤트 루프를 막는다.

# 비동기로 하려면:

# await asyncio.sleep(3)
# 함정 2. DB 드라이버도 비동기여야 한다

# PostgreSQL 기준:

# postgresql://...

# 이건 보통 동기 드라이버.

# postgresql+asyncpg://...

# 이건 asyncpg 기반 비동기 드라이버.

# 함정 3. ORM 내부 lazy loading 조심

# 비동기 ORM에서 lazy loading이 예상치 못한 추가 DB 호출을 만들 수 있다.

# 그래서 실무에서는:

# selectinload
# joinedload
# 명시적 쿼리

# 같은 방식으로 필요한 데이터를 미리 조회하는 게 좋다.

# 9. 면접용 1분 답변

# 비동기 DB 처리는 DB 응답 대기 시간 동안 이벤트 루프가 다른 요청을 처리할 수 있도록 하는 방식입니다. FastAPI에서는 AsyncSession과 asyncpg 같은 비동기 드라이버를 사용해 구현할 수 있습니다. 단순히 라우터에 async def를 붙이는 것만으로는 부족하고, DB 드라이버와 ORM 호출까지 비동기여야 합니다. 기존 동기 ORM을 사용해야 한다면 run_in_threadpool로 이벤트 루프 블로킹을 피할 수 있습니다.