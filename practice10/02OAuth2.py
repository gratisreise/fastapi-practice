# ✅ 1. OAuth2 한 줄 정의

# 👉 사용자 비밀번호를 직접 받지 않고, 외부 서비스로 인증을 위임하는 방식

# ✅ 2. 왜 OAuth2를 쓰냐?

# 일반 로그인:

# 우리 서비스가 아이디/비밀번호 직접 관리

# OAuth2:

# Google / Kakao가 인증 → 우리는 결과만 받음

# 👉 보안 + UX 둘 다 해결

# ✅ 3. 핵심 개념 (🔥 중요 3개만 기억)
# 1️⃣ Resource Owner

# 👉 사용자

# 2️⃣ Authorization Server

# 👉 Google, Kakao 같은 인증 서버

# 3️⃣ Client

# 👉 우리 서비스 (FastAPI 서버)

# ✅ 4. 전체 흐름 (🔥 무조건 암기)
# 1. 사용자 → "구글 로그인" 클릭
# 2. 구글 로그인 페이지 이동
# 3. 로그인 성공
# 4. Authorization Code 받음
# 5. 서버가 Code로 Access Token 요청
# 6. Access Token 받음
# 7. 사용자 정보 요청
# 8. 우리 서비스 JWT 발급

# 👉 핵심:
# "Code → Token → User Info → 우리 JWT"

# ✅ 5. Authorization Code Flow (핵심 플로우)
# Client → Google → Client(Server) → Google → Client

# 조금 더 풀면:

# [1] 프론트 → Google 로그인 요청
# [2] Google → redirect (code 포함)
# [3] FastAPI 서버 → code로 access_token 요청
# [4] Google → access_token 반환
# [5] FastAPI → user info 요청
# [6] FastAPI → 자체 JWT 발급
# ✅ 6. FastAPI에서의 구조
# 핵심은 3개 API
# 1️⃣ 로그인 요청
# @app.get("/login/google")
# def login():
#     return RedirectResponse("구글 인증 URL")
# 2️⃣ 콜백 (🔥 핵심)
# @app.get("/auth/google/callback")
# def callback(code: str):
#     # 1. code → access_token
#     # 2. access_token → user info
#     # 3. DB 조회 or 회원가입
#     # 4. JWT 발급
# 3️⃣ JWT 사용 (기존과 동일)

# 👉 이후는 그냥 JWT 인증

# ✅ 7. FastAPI에서 사용하는 라이브러리

# 대표:

# httpx → 외부 API 호출
# python-jose → JWT
# fastapi.security
# ✅ 8. 코드 흐름 (간단 버전)
# 1️⃣ code → access_token
# import httpx

# async def get_access_token(code: str):
#     async with httpx.AsyncClient() as client:
#         response = await client.post(
#             "https://oauth2.googleapis.com/token",
#             data={
#                 "client_id": "CLIENT_ID",
#                 "client_secret": "SECRET",
#                 "code": code,
#                 "grant_type": "authorization_code",
#                 "redirect_uri": "URL"
#             }
#         )
#     return response.json()
# 2️⃣ 사용자 정보 조회
# async def get_user_info(access_token: str):
#     async with httpx.AsyncClient() as client:
#         response = await client.get(
#             "https://www.googleapis.com/oauth2/v2/userinfo",
#             headers={"Authorization": f"Bearer {access_token}"}
#         )
#     return response.json()
# 3️⃣ JWT 발급

# 👉 여기서 기존 JWT 로직 그대로 사용

# ✅ 9. 실무 구조 (🔥 중요)

# 너 프로젝트 스타일로 보면 이렇게 가야 맞다:

# OAuthService
#   ├── GoogleStrategy
#   ├── KakaoStrategy
#   ├── NaverStrategy

# 👉 Strategy Pattern

# ✅ 10. 핵심 포인트 (면접용)

# 👉 이거 말하면 바로 합격권이다

# OAuth2는 인증 위임 프로토콜
# Authorization Code Flow 사용
# 서버에서 access_token 교환
# user info 받아서 내부 JWT 발급
# provider별 전략 패턴으로 확장