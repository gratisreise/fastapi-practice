# 1. Docker 배포란?
# FastAPI 앱 + 실행 환경 + 의존성 패키지를 하나의 이미지로 묶어서 배포하는 것
# 즉, 내 로컬에서는 되는데 서버에서는 안 되는 문제를 줄이기 위해 사용한다.
# Python 버전패키지 버전실행 명령어환경 변수프로젝트 파일
# 이것들을 Docker 이미지 안에 고정한다.

# 2. 기본 프로젝트 구조
# fastapi-app/├── main.py├── requirements.txt└── Dockerfile

# 3. 예제 FastAPI 코드
# # main.pyfrom fastapi import FastAPIapp = FastAPI()@app.get("/")def health_check():    return {"status": "ok"}

# 4. requirements.txt
# fastapiuvicorn[standard]gunicorn
# 운영 배포까지 고려하면 gunicorn도 같이 넣는다.

# 5. Dockerfile 기본 예시
# FROM python:3.11-slimWORKDIR /appCOPY requirements.txt .RUN pip install --no-cache-dir -r requirements.txtCOPY . .CMD ["gunicorn", "main:app", "-k", "uvicorn.workers.UvicornWorker", "-w", "4", "-b", "0.0.0.0:8000"]

# 6. Dockerfile 설명
# 1) Base Image
# FROM python:3.11-slim
# Python 3.11이 설치된 가벼운 리눅스 이미지를 사용한다.

# 2) 작업 디렉토리 설정
# WORKDIR /app
# 컨테이너 내부에서 /app 디렉토리를 기준으로 작업한다.

# 3) 의존성 파일 복사
# COPY requirements.txt .
# 먼저 requirements.txt만 복사한다.
# 이유는 Docker 캐시 때문이다.
# requirements.txt 변경 없음→ pip install 재실행 안 함→ 빌드 속도 향상

# 4) 패키지 설치
# RUN pip install --no-cache-dir -r requirements.txt
# --no-cache-dir는 불필요한 pip 캐시를 남기지 않아서 이미지 크기를 줄인다.

# 5) 전체 코드 복사
# COPY . .
# 애플리케이션 코드를 컨테이너 안으로 복사한다.

# 6) 실행 명령어
# CMD ["gunicorn", "main:app", "-k", "uvicorn.workers.UvicornWorker", "-w", "4", "-b", "0.0.0.0:8000"]
# 컨테이너가 실행될 때 FastAPI 앱을 실행한다.

# 7. 이미지 빌드
# docker build -t fastapi-app .
# 의미:
# 명령어의미docker build이미지 생성-t fastapi-app이미지 이름 지정.현재 디렉토리의 Dockerfile 사용

# 8. 컨테이너 실행
# docker run -d -p 8000:8000 --name fastapi-server fastapi-app
# 의미:
# 옵션의미-d백그라운드 실행-p 8000:8000호스트 8000 → 컨테이너 8000 연결--name fastapi-server컨테이너 이름 지정fastapi-app실행할 이미지

# 9. 접속 확인
# 브라우저 또는 curl:
# curl http://localhost:8000
# 결과:
# {  "status": "ok"}

# 10. .dockerignore 추가
# 실무에서는 꼭 추가한다.
# __pycache__*.pyc.env.git.venvvenv.idea.vscode
# 이유:
# 불필요한 파일 제외이미지 크기 감소민감 정보 유출 방지빌드 속도 향상
# 특히 .env는 이미지 안에 넣으면 안 된다.

# 11. 환경 변수 주입
# Docker 실행 시 환경 변수를 넣을 수 있다.
# docker run -d \  -p 8000:8000 \  -e APP_ENV=prod \  -e DATABASE_URL=postgresql://user:pass@host:5432/db \  --name fastapi-server \  fastapi-app
# FastAPI에서는:
# import osDATABASE_URL = os.getenv("DATABASE_URL")

# 12. .env 파일로 실행
# docker run -d \  -p 8000:8000 \  --env-file .env \  --name fastapi-server \  fastapi-app
# .env 예시:
# APP_ENV=prodDATABASE_URL=postgresql://user:pass@localhost:5432/mydbSECRET_KEY=my-secret
# 주의:
# .env는 Docker 이미지에 COPY하지 말고컨테이너 실행 시 주입한다.

# 13. Docker Compose 예시
# FastAPI + PostgreSQL 같이 띄울 때는 Docker Compose가 편하다.
# # docker-compose.ymlservices:  app:    build: .    container_name: fastapi-app    ports:      - "8000:8000"    env_file:      - .env    depends_on:      - db  db:    image: postgres:16    container_name: fastapi-db    environment:      POSTGRES_DB: mydb      POSTGRES_USER: user      POSTGRES_PASSWORD: password    ports:      - "5432:5432"
# 실행:
# docker compose up -d --build
# 종료:
# docker compose down

# 14. 운영 배포 시 구조
# Client  ↓Nginx  ↓Docker Container  ↓Gunicorn  ↓Uvicorn Workers  ↓FastAPI
# Docker는 애플리케이션 실행 환경을 고정하고,
# Nginx는 외부 요청을 받아서 컨테이너로 프록시한다.

# 15. 실무 주의사항
# 1) --reload 쓰지 않기
# 운영에서는 절대 이렇게 쓰면 안 된다.
# uvicorn main:app --reload
# --reload는 개발용이다.
# 운영에서는:
# gunicorn main:app -k uvicorn.workers.UvicornWorker -w 4 -b 0.0.0.0:8000

# 2) 0.0.0.0으로 바인딩
# 컨테이너 안에서 이렇게 하면 외부 접속이 안 될 수 있다.
# -b 127.0.0.1:8000
# 컨테이너 배포에서는 보통:
# -b 0.0.0.0:8000

# 3) 워커 수 조정
# -w 4
# 서버 CPU, 메모리, DB 커넥션 수에 따라 조정해야 한다.

# 4) 로그는 stdout으로 남기기
# Docker 환경에서는 로그 파일보다 stdout/stderr로 남기는 게 일반적이다.
# docker logs fastapi-server
# 로 확인할 수 있기 때문이다.

# 16. 한 줄 정리
# FastAPI Docker 배포는 앱 코드, 의존성, 실행 명령을 이미지로 묶고, 운영에서는 Gunicorn + Uvicorn Worker로 실행하며 환경 변수는 이미지에 넣지 않고 컨테이너 실행 시 주입하는 방식이다.

# 17. 면접용 1분 답변
# FastAPI를 Docker로 배포할 때는 Python 기반 이미지를 사용해 애플리케이션 코드와 의존성을 이미지로 패키징합니다.운영 환경에서는 uvicorn --reload가 아니라 Gunicorn과 Uvicorn Worker 조합으로 실행하고, 컨테이너 외부에서 접근 가능하도록 0.0.0.0:8000에 바인딩합니다.또한 .env 같은 민감 정보는 이미지에 포함하지 않고 docker run의 환경 변수나 env_file을 통해 주입합니다. 이를 통해 실행 환경을 일관되게 유지하고 배포 재현성을 높일 수 있습니다.