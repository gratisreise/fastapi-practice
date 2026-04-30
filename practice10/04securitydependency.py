# ✅ 1. 한 줄 정의

# 👉 Depends()를 이용해서 인증 로직을 공통으로 주입하는 구조

# ✅ 2. 왜 필요한가?

# 인증 없이 하면:

# @app.get("/profile")
# def profile():
#     # 매번 토큰 파싱 + 검증 코드 작성 ❌

# 👉 중복 + 유지보수 지옥

# 그래서:

# @app.get("/profile")
# def profile(user = Depends(get_current_user)):

# 👉 인증 로직을 분리

# ✅ 3. 핵심 구조 (🔥 중요)
# 요청 → Depends → JWT 검증 → user 반환 → API 실행
# ✅ 4. OAuth2PasswordBearer

# FastAPI에서 기본 제공

# from fastapi.security import OAuth2PasswordBearer

# oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")

# 👉 역할:

# Authorization Header에서 토큰 추출
# Authorization: Bearer <token>
# ✅ 5. get_current_user (🔥 핵심)
# 구조
# from fastapi import Depends
# from jose import jwt, JWTError

# SECRET_KEY = "secret"
# ALGORITHM = "HS256"

# def get_current_user(token: str = Depends(oauth2_scheme)):
#     try:
#         payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
#         user_id = payload.get("user_id")

#         if user_id is None:
#             raise Exception("Invalid token")

#         return {"user_id": user_id}

#     except JWTError:
#         raise Exception("Token error")
# ✅ 6. 실제 API 적용
# @app.get("/me")
# def read_me(user = Depends(get_current_user)):
#     return user

# 👉 요청 흐름:

# 요청 → Authorization 헤더 → 토큰 추출 → JWT 검증 → user 반환
# ✅ 7. 인증이 필요한 API / 아닌 API
# # 인증 필요
# @app.get("/private")
# def private(user = Depends(get_current_user)):
#     return "인증됨"


# # 인증 불필요
# @app.get("/public")
# def public():
#     return "누구나 접근"
# ✅ 8. 확장 (🔥 실무 핵심)
# 1️⃣ 관리자 권한 체크
# def admin_required(user = Depends(get_current_user)):
#     if user["role"] != "admin":
#         raise Exception("권한 없음")
#     return user

# 사용:

# @app.get("/admin")
# def admin(user = Depends(admin_required)):
#     return "관리자만"
# 2️⃣ DB 조회 포함
# def get_current_user(token: str = Depends(oauth2_scheme)):
#     payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
#     user = db.get_user(payload["user_id"])
#     return user
# ✅ 9. 실무 구조 (🔥 중요)
# dependencies/
#   └── auth.py
#         ├── oauth2_scheme
#         ├── get_current_user
#         ├── admin_required

# 👉 인증 로직 완전 분리

# ✅ 10. 핵심 포인트 (면접용)

# 👉
# "FastAPI에서는 Depends와 OAuth2PasswordBearer를 활용하여 인증 로직을 공통 의존성으로 분리하고, JWT 검증 후 사용자 정보를 주입하는 구조로 구현합니다."