# 1. 왜 Nginx를 쓰는가?

# FastAPI(Gunicorn)는 직접 외부에 노출해도 동작은 한다.

# 하지만 실무에서는 반드시 앞단에
# 👉 Nginx 를 둔다.

# 이유 4가지 (핵심🔥)
# 1) Reverse Proxy
# Client → Nginx → FastAPI

# 👉 서버 구조 숨김 + 라우팅 제어

# 2) 정적 파일 처리
# 이미지 / CSS / JS

# 👉 FastAPI 대신 Nginx가 처리 (성능 ↑)

# 3) 로드 밸런싱
# Nginx → 여러 FastAPI 서버

# 👉 트래픽 분산

# 4) HTTPS 처리
# SSL 인증서
# TLS 종료

# 👉 보안 처리 담당

# 2. 전체 구조
# Client
#   ↓
# Nginx (80 / 443)
#   ↓
# FastAPI (Docker)
#   ↓
# Gunicorn
#   ↓
# Uvicorn Workers
# 3. Nginx 기본 설정
# nginx.conf (핵심 예제)
# server {
#     listen 80;

#     server_name localhost;

#     location / {
#         proxy_pass http://app:8000;

#         proxy_set_header Host $host;
#         proxy_set_header X-Real-IP $remote_addr;

#         proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
#         proxy_set_header X-Forwarded-Proto $scheme;
#     }
# }
# 4. 설정 설명
# proxy_pass
# proxy_pass http://app:8000;

# 👉 FastAPI 서버로 요청 전달

# 헤더 설정 (중요🔥)
# proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;

# 👉 실제 클라이언트 IP 전달

# proxy_set_header X-Forwarded-Proto $scheme;

# 👉 http / https 구분 전달

# 5. Docker + Nginx 구성
# docker-compose.yml
# services:
#   app:
#     build: .
#     container_name: fastapi-app
#     expose:
#       - "8000"

#   nginx:
#     image: nginx:latest
#     container_name: nginx
#     ports:
#       - "80:80"
#     volumes:
#       - ./nginx.conf:/etc/nginx/conf.d/default.conf
#     depends_on:
#       - app
# 핵심 포인트
# proxy_pass http://app:8000;

# 👉 여기서 app은 Docker 서비스 이름

# 6. 실행
# docker compose up -d --build
# 접속
# http://localhost

# 👉 Nginx → FastAPI로 전달됨

# 7. 정적 파일 처리
# location /static/ {
#     alias /static/;
# }

# 👉 이미지, CSS 등은 Nginx가 직접 처리

# 8. HTTPS 적용 (개념)
# server {
#     listen 443 ssl;

#     ssl_certificate /etc/ssl/cert.pem;
#     ssl_certificate_key /etc/ssl/key.pem;
# }

# 👉 HTTPS는 Nginx에서 처리하고
# FastAPI는 내부 HTTP로 통신

# 9. 로드 밸런싱
# upstream fastapi {
#     server app1:8000;
#     server app2:8000;
# }

# server {
#     location / {
#         proxy_pass http://fastapi;
#     }
# }

# 👉 여러 서버로 분산

# 10. 실무 핵심 포인트 (진짜 중요🔥)
# 1) FastAPI 직접 노출 ❌
# 보안 취약
# 성능 한계

# 👉 항상 Nginx 앞단 배치

# 2) timeout 설정
# proxy_read_timeout 60;

# 👉 긴 요청 대비

# 3) body size 제한
# client_max_body_size 10M;

# 👉 파일 업로드 대응

# 4) keep-alive
# keepalive_timeout 65;

# 👉 성능 개선

# 11. 최종 구조 (완성🔥)
# Client
#   ↓
# Nginx (Reverse Proxy + HTTPS + Static)
#   ↓
# Docker Container
#   ↓
# Gunicorn
#   ↓
# Uvicorn Workers
#   ↓
# FastAPI
# 12. 한 줄 정리
# Nginx는 FastAPI 앞단에서 Reverse Proxy, HTTPS, 정적 파일 처리, 로드 밸런싱을 담당하는 핵심 웹 서버이다.
# 13. 면접용 1분 답변
# FastAPI는 운영 환경에서 직접 외부에 노출하지 않고, 앞단에 Nginx를 두는 구조로 구성합니다.

# Nginx는 Reverse Proxy 역할을 하여 클라이언트 요청을 FastAPI 서버로 전달하고, HTTPS 처리와 정적 파일 서빙을 담당합니다. 또한 필요 시 여러 FastAPI 인스턴스로 로드 밸런싱을 수행할 수 있어 확장성과 안정성을 확보할 수 있습니다.

# 이러한 구조를 통해 애플리케이션 서버의 부담을 줄이고, 보안과 성능을 동시에 개선할 수 있습니다.