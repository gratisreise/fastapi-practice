# ✅ 1. JWT 인증 개념
# 한 줄 정의

# 👉 JWT는 서버가 상태를 저장하지 않고 인증을 처리하는 토큰 방식

# ✅ 왜 JWT를 쓰냐?

# 기존 방식 (세션)

# 로그인 → 서버가 세션 저장 → 요청마다 세션 조회

# 문제:

# 서버 메모리 사용
# 서버 늘어나면 세션 공유 필요 (Redis 등)

# JWT 방식

# 로그인 → 토큰 발급 → 클라이언트가 들고 다님

# 👉 서버는 저장 안 함 (Stateless)

# ✅ JWT 구조 (핵심)

# JWT는 3개로 구성됨:

# Header.Payload.Signature

# 예시:

# eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9
# .
# eyJ1c2VyX2lkIjoxLCJleHAiOjE3MDAwMDAwMDB9
# .
# abc123signature
# 1️⃣ Header
# {
#   "alg": "HS256",
#   "typ": "JWT"
# }

# 👉 어떤 방식으로 서명했는지

# 2️⃣ Payload (🔥 중요)
# {
#   "user_id": 1,
#   "exp": 1700000000
# }

# 👉 실제 데이터

# 주요 필드:

# user_id
# exp (만료시간)
# iat (발급시간)
# 3️⃣ Signature (🔥 핵심)
# HMACSHA256(
#   base64(header) + "." + base64(payload),
#   secret_key
# )

# 👉 위조 방지용

# ✅ 핵심 동작 흐름
# 1. 로그인 성공
# 2. 서버가 JWT 생성
# 3. 클라이언트에 전달
# 4. 이후 요청마다 JWT 포함
# 5. 서버는 JWT 검증만 함 (DB 조회 X 가능)
# ✅ 요청 시 사용 방식
# Authorization: Bearer <JWT>
# ✅ 장점 / 단점
# 장점
# 서버 상태 없음 (Stateless)
# 확장성 좋음 (MSA에 유리)
# 속도 빠름
# 단점
# 로그아웃 어려움 ❗
# 토큰 탈취 시 위험
# 토큰 크기 큼
# ✅ 실무 핵심 포인트 (중요)

# 너 같은 백엔드 기준으로 중요한 것만 찝는다:

# Access Token + Refresh Token 구조
# Redis로 블랙리스트 관리 (로그아웃 처리)
# 짧은 만료시간 설정
# HTTPS 필수