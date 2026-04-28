# 1. I/O Bound vs CPU Bound 한 줄 정의
# I/O Bound 👉 “외부 기다림 때문에 느림”
# CPU Bound 👉 “계산 때문에 느림”
# 2. I/O Bound
# ✅ 정의

# 외부 작업이 끝날 때까지 기다리는 시간이 대부분인 작업

# ✅ 예시
# DB 조회
# 외부 API 호출 (Gemini, OpenAI)
# 파일 읽기
# HTTP 요청
# Redis 요청
# ✅ 특징
# CPU는 놀고 있음
# 대부분 "대기 시간"
# async 효과 매우 큼
# ✅ 코드 느낌
# async def get_user():
#     user = await db.fetch()  # DB 기다림
#     return user

# 👉 기다리는 동안 다른 요청 처리 가능

# 🔥 실무 연결 (너 기준)
# Gemini 호출 → I/O Bound
# RAG 검색 → I/O Bound
# 외부 API → I/O Bound

# 👉 그래서 async 쓰는 게 정답

# 3. CPU Bound
# ❌ 정의

# CPU 계산 때문에 시간이 오래 걸리는 작업

# ❌ 예시
# 이미지 처리
# 암호화
# 대량 데이터 연산
# AI 모델 로컬 추론
# 정렬 / 반복문 대량 처리
# ❌ 특징
# CPU를 계속 점유
# async 써도 효과 없음
# 오히려 성능 나빠질 수도 있음
# ❌ 코드 느낌
# def heavy_task():
#     for i in range(100000000):
#         pass

# 👉 CPU가 계속 바쁨

# 4. 핵심 비교
# 구분	I/O Bound	CPU Bound
# 병목	외부 대기	계산
# CPU 상태	놀고 있음	계속 사용
# async 효과	🔥 큼	❌ 없음
# 해결 방법	async/await	multiprocessing / worker
# 5. 왜 async가 CPU Bound에 안 먹히냐

# 핵심:

# 👉 async는 “기다리는 시간”을 활용하는 기술

# 근데 CPU Bound는:

# 계속 계산 중 → 기다림 없음

# 👉 양보할 시간이 없음 → async 의미 없음

# 6. 실무 설계 관점 (중요)
# 👉 I/O Bound
# FastAPI + async/await
# async DB
# async HTTP client
# 👉 CPU Bound
# Celery / Worker 분리
# multiprocessing
# 별도 서비스 (ML 서버)
# 7. 너 프로젝트 기준으로 딱 정리
# 작업	타입	처리 방식
# Gemini API 호출	I/O Bound	async
# RAG 검색	I/O Bound	async
# 임베딩 생성 (외부 API)	I/O Bound	async
# 임베딩 생성 (로컬 모델)	CPU Bound	worker
# Batch 처리	혼합	배치 + 비동기
# 🔥 면접용 1분 답변

# 👉
# “I/O Bound 작업은 외부 시스템 응답을 기다리는 시간이 병목이기 때문에 async/await을 사용하면 성능이 크게 개선됩니다.
# 반면 CPU Bound 작업은 계산 자체가 병목이므로 async로는 해결되지 않고, multiprocessing이나 별도의 worker로 분리해야 합니다.

# 실무에서는 API 호출, DB 조회 같은 작업은 비동기로 처리하고, 이미지 처리나 모델 추론은 별도 처리 구조로 분리하는 방식으로 설계합니다.”