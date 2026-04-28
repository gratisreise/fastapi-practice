# 1. 한 줄 정의
# asyncio 병렬 처리는 여러 I/O 작업을 동시에 시작해놓고, 결과를 함께 기다리는 방식이야.
# 정확히는 CPU 병렬이라기보다 비동기 동시 처리에 가깝다.

# 2. 순차 처리
# result1 = await task1() result2 = await task2()
# 흐름은 이렇다.
# task1 끝날 때까지 기다림그 다음 task2 실행
# 각각 2초 걸리면 총 4초 걸린다.

# 3. 동시 처리
# result1, result2 = await asyncio.gather(    task1(),    task2())
# 흐름은 이렇다.
# task1 시작task2 시작둘 다 끝날 때까지 기다림
# 각각 2초 걸리면 총 2초 정도 걸린다.

# 4. 기본 예제
# import asyncioasync def call_api(name: str):    print(f"{name} 시작")    await asyncio.sleep(2)    print(f"{name} 끝")    return nameasync def main():    results = await asyncio.gather(        call_api("A"),        call_api("B"),        call_api("C")    )    print(results)asyncio.run(main())
# 결과 흐름:
# A 시작B 시작C 시작2초 대기A 끝B 끝C 끝['A', 'B', 'C']

# 5. FastAPI에서 활용 예시
# @app.get("/recommend")async def recommend():    user_task = get_user_profile()    search_task = search_vector_db()    history_task = get_user_history()    user, search_result, history = await asyncio.gather(        user_task,        search_task,        history_task    )    return {        "user": user,        "search": search_result,        "history": history    }
# 각 작업이 DB/API 호출이면 동시에 처리할 수 있다.

# 6. LLM/RAG 기준 예시
# async def generate_answer(question: str):    embedding_task = create_embedding(question)    context_task = search_documents(question)    user_task = get_user_context()    embedding, context, user = await asyncio.gather(        embedding_task,        context_task,        user_task    )    answer = await call_llm(question, context, user)    return answer
# 다만 이 예시는 주의가 필요하다.
# 만약 search_documents()가 embedding 결과가 필요하다면 동시에 못 한다.
# 그 경우는 이렇게 해야 한다.
# embedding = await create_embedding(question)context = await search_by_embedding(embedding)answer = await call_llm(question, context)
# 즉, 의존성이 없는 작업만 병렬 처리한다.

# 7. gather의 핵심 주의점
# 1) 하나 실패하면 전체 실패할 수 있음
# results = await asyncio.gather(task1(), task2())
# 기본적으로 하나의 task에서 예외가 나면 gather도 예외를 던진다.
# 필요하면:
# results = await asyncio.gather(    task1(),    task2(),    return_exceptions=True)

# 2) 너무 많이 동시에 실행하면 위험
# await asyncio.gather(*[call_api(i) for i in range(10000)])
# 이러면 외부 API, DB, 서버 자원을 한 번에 압박할 수 있다.
# 그래서 제한을 둔다.
# semaphore = asyncio.Semaphore(10)async def limited_call(i):    async with semaphore:        return await call_api(i)

# 8. Semaphore 예시
# import asynciosemaphore = asyncio.Semaphore(3)async def call_api(i: int):    async with semaphore:        print(f"{i} 시작")        await asyncio.sleep(1)        print(f"{i} 끝")        return iasync def main():    results = await asyncio.gather(        *[call_api(i) for i in range(10)]    )    print(results)asyncio.run(main())
# 이 코드는 한 번에 최대 3개까지만 실행한다.

# 9. 실무 사용 기준
# 상황병렬 처리 가능?사용자 정보 조회 + 상품 조회가능여러 외부 API 동시 호출가능여러 DB 조회가능하나 커넥션풀 주의embedding 생성 후 vector search불가능, 의존성 있음LLM 응답 생성 후 요약 저장보통 순차여러 문서 요약가능, 단 제한 필요

# 10. 면접용 1분 답변
# FastAPI에서 병렬 처리는 asyncio.gather를 사용해 서로 의존성이 없는 I/O 작업을 동시에 실행하는 방식으로 구현할 수 있습니다. 예를 들어 사용자 정보 조회, 외부 API 호출, DB 조회처럼 서로 독립적인 작업은 동시에 실행해 전체 응답 시간을 줄일 수 있습니다. 다만 CPU Bound 작업에는 효과가 없고, 너무 많은 작업을 동시에 실행하면 DB 커넥션 풀이나 외부 API rate limit 문제가 생길 수 있어 Semaphore 등을 사용해 동시 실행 수를 제한해야 합니다.