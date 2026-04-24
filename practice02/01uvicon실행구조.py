# 1. uvicorn이란?

# uvicorn = FastAPI 앱을 실제 서버로 실행해주는 프로그램

# FastAPI는 API 로직을 작성하는 프레임워크고,
# uvicorn은 그 FastAPI 앱을 외부 요청을 받을 수 있게 실행해준다.

# 구조는 이렇게 보면 된다.

# 브라우저 / 클라이언트
#         ↓ HTTP 요청
# uvicorn 서버
#         ↓
# FastAPI 앱
#         ↓
# 응답 반환

# 즉,

# FastAPI = API 코드
# uvicorn = API 코드를 실행하는 서버
# 2. 왜 uvicorn이 필요할까?

# 예를 들어 FastAPI 코드를 이렇게 작성했다고 하자.

# from fastapi import FastAPI

# app = FastAPI()

# 이 상태만으로는 서버가 실행되지 않는다.

# 이 코드는 단지:

# FastAPI 애플리케이션 객체를 만든 것

# 일 뿐이다.

# 실제로 요청을 받으려면 서버가 필요하다.

# uvicorn main:app --reload

# 이 명령어가 실행되면 uvicorn이 main.py 안의 app 객체를 찾아서 서버로 띄운다.

# 3. uvicorn 실행 명령어 구조
# uvicorn main:app --reload

# 이걸 나눠보면:

# uvicorn  main:app  --reload
# 부분	의미
# uvicorn	서버 실행 프로그램
# main	실행할 파이썬 파일 이름, main.py
# app	FastAPI 객체 이름
# --reload	코드 변경 시 자동 재시작
# 4. main:app 의미

# 가장 중요하다.

# uvicorn main:app

# 이건 이런 뜻이다.

# main.py 파일 안에 있는 app 변수를 실행해라

# 예시:

# # main.py

# from fastapi import FastAPI

# app = FastAPI()

# 여기서 파일 이름이 main.py이고, FastAPI 객체 이름이 app이니까:

# uvicorn main:app

# 이 된다.

# 만약 파일명이 server.py라면?

# # server.py

# from fastapi import FastAPI

# app = FastAPI()

# 실행은:

# uvicorn server:app

# 만약 객체 이름이 api라면?

# # main.py

# from fastapi import FastAPI

# api = FastAPI()

# 실행은:

# uvicorn main:api
# 5. 백엔드 개발자 관점으로 비유

# Spring Boot에서는 보통:

# SpringApplication.run(Application.class, args);

# 이게 내장 톰캣을 띄우면서 서버가 실행된다.

# FastAPI는 보통 이렇게 분리해서 생각하면 된다.

# Spring Boot 내장 Tomcat 역할 ≈ uvicorn
# Controller 역할 ≈ FastAPI 라우터
# Application 객체 역할 ≈ app = FastAPI()

# 즉, uvicorn은 Spring Boot에서 서버를 띄우는 실행 환경에 가깝다.

# 6. 정리
# uvicorn은 FastAPI 앱을 실행하는 ASGI 서버다.
# FastAPI 코드만 작성하면 서버가 뜨지 않는다.
# uvicorn이 main.py 안의 app 객체를 찾아 HTTP 요청을 처리할 수 있게 실행한다.

# 한 줄로 말하면:

# uvicorn은 FastAPI 앱을 실제 HTTP 서버로 띄워주는 실행기다.