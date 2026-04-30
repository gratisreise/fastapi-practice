# ✅ 1. 한 줄 정의

# 👉 비밀번호를 암호화해서 저장하는 것 (복호화 불가능)

# ❌ 왜 평문 저장하면 안 되냐
# DB 유출 → 사용자 비밀번호 그대로 노출 → 다른 서비스까지 털림

# 👉 실제 사고 대부분 이거 때문

# ✅ 2. 해싱 vs 암호화
# 구분	해싱	암호화
# 복호화	❌ 불가능	✅ 가능
# 목적	비밀번호 저장	데이터 보호
# 예시	bcrypt	AES

# 👉 비밀번호는 무조건 해싱

# ✅ 3. bcrypt (🔥 표준)

# 👉 FastAPI에서 가장 많이 쓰는 방식

# 특징:

# Salt 자동 포함
# 느림 (브루트포스 방지)
# 동일 비밀번호 → 매번 다른 해시
# ✅ 4. FastAPI에서 사용 라이브러리
# pip install passlib[bcrypt]
# ✅ 5. 기본 코드
# 1️⃣ 해싱 (회원가입)
# from passlib.context import CryptContext

# pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# def hash_password(password: str) -> str:
#     return pwd_context.hash(password)
# 2️⃣ 검증 (로그인)
# def verify_password(plain_password: str, hashed_password: str) -> bool:
#     return pwd_context.verify(plain_password, hashed_password)
# ✅ 6. 사용 흐름
# 회원가입:
# password → hash → DB 저장

# 로그인:
# 입력 password → hash 비교 → 일치 여부 확인
# ✅ 7. 실제 사용 예시
# # 회원가입
# user.password = hash_password("1234")

# # 로그인
# if not verify_password("1234", user.password):
#     raise Exception("비밀번호 틀림")
# ✅ 8. 실무 핵심 포인트 (🔥 중요)
# 1️⃣ 절대 금지
# ❌ 평문 저장
# ❌ SHA256 단독 사용 (빠름 → 위험)
# 2️⃣ 반드시
# ✅ bcrypt 사용
# ✅ salt 포함 (bcrypt가 자동 처리)
# ✅ 비교는 verify 함수로
# 3️⃣ 추가 보안
# rate limit (로그인 시도 제한)
# 실패 횟수 제한
# 2FA (선택)
# ✅ 9. 자주 하는 실수
# # ❌ 잘못된 방식
# if hash(input_pw) == stored_hash:
#     pass

# 👉 bcrypt는 매번 값 다름 → 이렇게 비교하면 안 됨

# ✅ 10. 한 줄 정리 (면접용)

# 👉
# "비밀번호는 bcrypt로 해싱하여 저장하고, 로그인 시 verify로 비교합니다. 해시는 salt를 포함하며 복호화가 불가능합니다."