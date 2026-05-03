# 2. pytest
# ✔️ 한 줄 정의

# Python에서 가장 많이 쓰는 테스트 실행 프레임워크 (assert 기반)

# ✔️ 왜 쓰냐 (실무 기준)
# 테스트 자동 실행 (pytest 한 방)
# 코드 간결 (assert 하나로 끝)
# DI 구조 지원 (fixture → 너가 좋아할 스타일)
# FastAPI TestClient랑 궁합 좋음

# ✔️ 기본 구조 (필수 암기)
# def test_add():
#     assert 1 + 1 == 2

# 👉 규칙

# 파일명: test_*.py
# 함수명: test_*
# ✔️ 실행
# pytest

# 특정 파일만:

# pytest test_main.py
# ✔️ assert 핵심
# assert result == expected

# 실패하면 자동으로 로그 출력됨

# 👉 JUnit처럼 assertEquals 필요 없음

# ✔️ 실전 느낌 (FastAPI + TestClient)
# from fastapi.testclient import TestClient
# from main import app

# client = TestClient(app)

# def test_hello():
#     response = client.get("/hello")

#     assert response.status_code == 200
#     assert response.json() == {"msg": "hello"}
# ✔️ 여러 테스트 실행
# def test_1():
#     assert True

# def test_2():
#     assert True

# 👉 pytest가 자동으로 다 실행

# ✔️ 실패 예시
# def test_fail():
#     assert 1 == 2

# 출력:

# E       assert 1 == 2

# 👉 어디서 실패했는지 바로 보여줌

# ✔️ 핵심 포인트 (면접용)
# assert 기반으로 간결한 테스트 작성 가능
# 테스트 자동 수집 및 실행
# FastAPI TestClient와 결합해 API 테스트 수행
# fixture를 통한 의존성 관리 지원
# ✔️ 너 스타일 한 줄 정리

# "pytest는 assert 기반으로 간결하게 테스트를 작성하고 자동으로 실행해주는 Python 테스트 프레임워크입니다."