# 14-3. 설정 분리 dev / prod
# 설정 분리는 말 그대로 개발 환경과 운영 환경의 설정값을 다르게 관리하는 것이야.

# 왜 분리해야 하나?
# 개발 환경과 운영 환경은 보통 값이 다르다.
# 개발 dev- DEBUG=true- 로컬 DB 사용- 로그 자세히 출력- CORS 넓게 허용- 테스트용 API Key 사용운영 prod- DEBUG=false- 운영 DB 사용- 로그 최소화- CORS 도메인 제한- 실제 API Key 사용

# 기본 파일 구조
# app/ ├─ main.py ├─ core/ │   └─ config.py ├─ .env.dev ├─ .env.prod └─ .env.example

# .env.dev
# APP_ENV=devAPP_NAME=My FastAPI DevDEBUG=trueDATABASE_URL=postgresql://dev_user:dev_pass@localhost:5432/dev_dbJWT_SECRET_KEY=dev-secretCORS_ORIGINS=http://localhost:3000,http://localhost:5173

# .env.prod
# APP_ENV=prodAPP_NAME=My FastAPIDEBUG=falseDATABASE_URL=postgresql://prod_user:prod_pass@prod-db:5432/prod_dbJWT_SECRET_KEY=real-strong-secretCORS_ORIGINS=https://myservice.com
# 운영 .env.prod도 Git에 올리면 안 된다.

# config.py 예시
# import osfrom pydantic_settings import BaseSettingsclass Settings(BaseSettings):    app_env: str = "dev"    app_name: str    debug: bool = False    database_url: str    jwt_secret_key: str    cors_origins: str = ""    class Config:        env_file = f".env.{os.getenv('APP_ENV', 'dev')}"settings = Settings()

# 동작 방식
# APP_ENV=dev uvicorn app.main:app --reload
# 그러면:
# .env.dev 파일 로딩
# APP_ENV=prod uvicorn app.main:app
# 그러면:
# .env.prod 파일 로딩

# main.py에서 사용
# from fastapi import FastAPIfrom app.core.config import settingsapp = FastAPI(    title=settings.app_name,    debug=settings.debug)@app.get("/")def root():    return {        "env": settings.app_env,        "app_name": settings.app_name,        "debug": settings.debug    }

# CORS 설정에 적용
# from fastapi import FastAPIfrom fastapi.middleware.cors import CORSMiddlewarefrom app.core.config import settingsapp = FastAPI(title=settings.app_name)origins = settings.cors_origins.split(",")app.add_middleware(    CORSMiddleware,    allow_origins=origins,    allow_credentials=True,    allow_methods=["*"],    allow_headers=["*"],)

# 실행 예시
# 개발
# APP_ENV=dev uvicorn app.main:app --reload
# 운영
# APP_ENV=prod uvicorn app.main:app

# 실무에서 더 좋은 구조
# 운영에서는 보통 .env.prod 파일보다 서버 환경 변수를 직접 주입한다.
# 예:
# export APP_ENV=prodexport DATABASE_URL=postgresql://...export JWT_SECRET_KEY=...uvicorn app.main:app
# Docker라면:
# environment:  APP_ENV: prod  DEBUG: false  DATABASE_URL: postgresql://...  JWT_SECRET_KEY: ...

# 주의사항
# .env.dev, .env.prod → Git에 올리지 않기.env.example → Git에 올리기
# .gitignore
# .env.env.dev.env.prod
# .env.example
# APP_ENV=APP_NAME=DEBUG=DATABASE_URL=JWT_SECRET_KEY=CORS_ORIGINS=

# 한 줄 정리

# dev / prod 설정 분리는 환경마다 다른 값을 코드 수정 없이 바꿔 끼우기 위한 구조다.

# 실무에서는 보통:
# local/dev → .env.devprod → OS 환경 변수, Docker, Kubernetes Secret
# 이렇게 가져간다.