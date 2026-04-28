# 1. async / await 한 줄 정의

# async / await은 오래 기다리는 작업 중에 다른 작업을 처리할 수 있게 해주는 비동기 문법이야.

# 특히 이런 작업에서 의미가 크다.

# DB 조회
# 외부 API 호출
# 파일 읽기/쓰기
# Redis 요청
# HTTP 요청
# LLM API 호출
# 2. 핵심 비유

# 동기 코드는 이런 느낌이야.

# 손님 A 주문 받음
# 커피 나올 때까지 멍하니 기다림
# 손님 B 주문 못 받음

# 비동기 코드는 이런 느낌이야.

# 손님 A 주문 받음
# 커피 머신에 맡김
# 기다리는 동안 손님 B 주문 받음

# 즉, 기다리는 시간에 서버가 놀지 않게 하는 것이 async / await의 목적이야.

# 3. 기본 문법
# async def get_data():
#     result = await fetch_from_api()
#     return result
# async def
# async def get_data():

# 비동기 함수를 만든다는 뜻.

# await
# result = await fetch_from_api()

# 이 작업이 끝날 때까지 기다리되,
# 그동안 실행 흐름을 이벤트 루프에 양보한다는 뜻.

# 4. 중요한 오해

# await은 “그냥 기다린다”가 아니다.

# 정확히는:

# 이 작업은 시간이 걸리니까,
# 끝날 때까지 다른 작업 먼저 처리해도 돼

# 라는 의미다.

# 5. 가장 단순한 예시
# import asyncio

# async def hello():
#     print("시작")
#     await asyncio.sleep(2)
#     print("끝")

# asyncio.run(hello())

# 여기서:

# await asyncio.sleep(2)

# 은 2초 동안 멈추는 게 아니라,
# 2초 동안 다른 비동기 작업이 실행될 수 있게 양보한다.

# 6. 동기 sleep과 차이
# 동기
import time

def hello():
    print("시작")
    time.sleep(2)
    print("끝")

# time.sleep(2)는 진짜로 현재 실행 흐름을 막는다.

# 비동기
import asyncio

async def hello():
    print("시작")
    await asyncio.sleep(2)
    print("끝")

# await asyncio.sleep(2)는 기다리는 동안 다른 작업을 처리할 수 있다.

# 7. 오늘 핵심 정리
# async def

# 비동기 함수 선언

# await

# 오래 걸리는 I/O 작업을 기다리면서 실행 흐름 양보

# asyncio.run()

# 비동기 함수를 실행하는 진입점