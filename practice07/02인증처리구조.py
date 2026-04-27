# 3️⃣ 인증 처리 구조 (FastAPI + Depends)
# ✔ 전체 구조 먼저 잡자 (중요🔥)
# Request
#   ↓
# JWT 추출 (Header)
#   ↓
# 유효성 검증
#   ↓
# 유저 조회
#   ↓
# endpoint에 user 주입

# 👉 이걸 Depends()로 구현하는 게 핵심

# ✔ 1단계: 토큰 추출
from fastapi import Header, HTTPException

def get_token(authorization: str = Header(None)):
    if authorization is None:
        raise HTTPException(status_code=401, detail="No token")

    return authorization.replace("Bearer ", "")

# 👉 역할

# Header에서 JWT 추출
# 없으면 바로 401
# ✔ 2단계: 토큰 검증
def verify_token(token: str = Depends(get_token)):
    if token != "valid-token":
        raise HTTPException(status_code=401, detail="Invalid token")

    return {"user_id": 1}

# 👉 역할

# 토큰 검증
# payload 반환
# ✔ 3단계: 유저 조회
def get_current_user(payload=Depends(verify_token)):
    return {"id": payload["user_id"], "name": "kim"}

# 👉 역할

# DB 조회 자리 (실무에서는 DB 붙음)
# ✔ 4단계: endpoint에서 사용
# @app.get("/me")
# def read_me(user=Depends(get_current_user)):
#     return user

# ✔ 실행 흐름 (진짜 중요🔥)
# get_token
#    ↓
# verify_token
#    ↓
# get_current_user
#    ↓
# endpoint

# 👉 완전 체인 구조

# ✔ 이게 왜 좋냐
# 1. 인증 로직 완전 분리됨

# 👉 endpoint는 오직 비즈니스 로직만

# 2. 재사용 가능
# @app.get("/orders")
# def orders(user=Depends(get_current_user)):

# 👉 모든 API에서 재사용

# 3. 테스트 쉬움

# 👉 dependency mocking 가능

# ✔ Spring이랑 비교
# Spring
# Filter → SecurityContext → Controller
# FastAPI
# Depends 체인 → endpoint

# 👉 역할은 같고
# 👉 구조는 훨씬 단순

# ✔ 실무 확장 패턴 (중요🔥)
# 1. 권한 체크
# def require_admin(user=Depends(get_current_user)):
#     if user["role"] != "admin":
#         raise HTTPException(status_code=403)
#     return user
# @app.get("/admin")
# def admin(user=Depends(require_admin)):
#     return "admin only"
# 2. DB 세션 + 인증 결합
# def get_user(db=Depends(get_db), payload=Depends(verify_token)):
#     return db.query(User).get(payload["user_id"])

# 👉 너가 하던 구조 그대로 가능

# 3. 캐싱 / Redis 붙이기

# 👉 토큰 blacklist 체크
# 👉 rate limit

# ✔ 실무 구조 한 줄 요약

# 👉
# “FastAPI는 Depends 체인을 통해
# 인증 → 검증 → 유저 조회 → 권한 체크를
# 파이프라인처럼 구성한다”

# 🔥 면접용 1분 답변

# 👉
# “FastAPI에서는 Depends를 활용하여 인증 구조를 체인 형태로 구성합니다. 토큰 추출, 검증, 사용자 조회를 각각의 의존성으로 분리하고, 이를 순차적으로 실행하여 최종적으로 엔드포인트에 사용자 정보를 주입합니다. 이를 통해 인증 로직을 재사용 가능하게 만들고, 비즈니스 로직과 명확히 분리할 수 있습니다.”

# 🔥 너 기준으로 중요 포인트 (찐 핵심)

# 너 지금까지 했던 경험이랑 연결하면:

# JWT → verify_token
# Redis blacklist → verify 단계
# DB 조회 → get_current_user
# Gateway 인증 → Depends 체인으로 대체 가능

# 👉 거의 동일 구조