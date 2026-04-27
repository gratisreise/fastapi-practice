# 1️⃣ Depends() — 개념부터 정확히 잡자
# ✔ 한 줄 정의

# 👉 Depends() =
# “이 함수 실행 전에 필요한 로직을 먼저 실행해줘”

# ✔ 기본 구조
# from fastapi import Depends

# def dependency():
#     return "hello"

# @app.get("/")
# def read_root(data=Depends(dependency)):
#     return {"data": data}
# 실행 흐름
# dependency() 먼저 실행됨
# 반환값 "hello" 획득
# read_root() 실행 시 data로 주입

# 👉 즉

# dependency() → 결과 → endpoint에 주입
# ✔ 핵심 포인트 3개
# 1. 함수 실행을 “자동으로 끼워넣는다”
# data=Depends(dependency)

# 👉 이건 단순 파라미터가 아니라
# 👉 실행 트리거

# 2. 결과를 자동으로 전달
# return "hello"

# 👉 이 값이 그대로 data에 들어감

# 3. 여러 개도 가능
# def dep1():
#     return 1

# def dep2():
#     return 2

# @app.get("/")
# def test(a=Depends(dep1), b=Depends(dep2)):
#     return a + b
# ✔ 왜 쓰냐 (중요)

# FastAPI에서 Depends는 단순 편의 기능이 아니라

# 👉 관심사 분리 (Separation of Concerns)
# 👉 재사용 가능한 요청 파이프라인 구성

# 을 위해 존재한다

# ✔ 실무 느낌으로 보면

# Spring에서

# @Autowired
# private UserService userService;

# 👉 이거랑 비슷해 보이지만

# FastAPI는 이렇게 생각해야 맞다:

# 👉 “이 요청 처리 전에 이 로직을 반드시 실행해라”

# ✔ 요청 흐름 기준으로 보면
# Request 들어옴
#    ↓
# Dependency 실행
#    ↓
# Endpoint 실행
#    ↓
# Response 반환
# ✔ 체인도 가능 (중요🔥)
# def dep1():
#     return 10

# def dep2(x=Depends(dep1)):
#     return x * 2

# @app.get("/")
# def test(result=Depends(dep2)):
#     return result

# 👉 실행 순서

# dep1 → dep2 → endpoint

# 👉 이게 진짜 FastAPI DI의 핵심

# ✔ 이걸 어디에 쓰냐

# 앞으로 나올 것들 전부 Depends 기반이다:

# DB 세션 주입
# 인증 처리 (JWT)
# 공통 로깅
# 권한 체크
# 트랜잭션 관리 느낌
# 🔥 정리 (면접용 1분 답변)

# 👉
# “FastAPI의 Depends는 의존성 주입 도구이면서 동시에 요청 처리 파이프라인을 구성하는 메커니즘입니다. 특정 로직을 엔드포인트 실행 전에 자동으로 수행하고, 그 결과를 주입함으로써 인증, DB 세션, 공통 로직 등을 재사용 가능하게 분리할 수 있습니다.”