# 1. 대용량 처리의 핵심
# 대용량 처리는 단순히 “서버를 크게 만든다”가 아니다.
# 핵심은 이거다.
# 요청을 빠르게 끝내고,무거운 작업은 분리하고,DB 부하를 줄이고,응답 데이터를 작게 나누는 것

# 2. 대표 전략 5가지
# 1. Pagination2. Streaming3. Background Task / Queue4. DB Index / Query 최적화5. Cache

# 3. Pagination
# 대용량 조회에서 가장 기본이다.
# 나쁜 예:
# @router.get("/users")def get_users(db: Session = Depends(get_db)):    return db.query(User).all()
# 문제:
# 전체 유저를 한 번에 조회DB 부하 증가메모리 사용량 증가응답 시간 증가
# 좋은 예:
# @router.get("/users")def get_users(    page: int = 1,    size: int = 20,    db: Session = Depends(get_db)):    offset = (page - 1) * size    users = (        db.query(User)        .offset(offset)        .limit(size)        .all()    )    return users

# 4. Cursor Pagination
# 실무에서는 offset보다 cursor 방식이 더 좋을 때가 많다.
# @router.get("/posts")def get_posts(    last_id: int | None = None,    size: int = 20,    db: Session = Depends(get_db)):    query = db.query(Post).order_by(Post.id.desc())    if last_id:        query = query.filter(Post.id < last_id)    posts = query.limit(size).all()    return posts
# 흐름:
# 처음 요청:GET /posts?size=20다음 요청:GET /posts?last_id=85&size=20
# 장점:
# 대용량 테이블에서 성능이 안정적무한 스크롤에 적합데이터가 중간에 추가되어도 중복/누락이 적음

# 5. Streaming Response
# 파일 다운로드, 로그, 대용량 CSV 응답은 한 번에 메모리에 올리면 위험하다.
# 나쁜 예:
# return large_file_content
# 좋은 예:
# from fastapi.responses import StreamingResponsedef iter_file():    with open("large.csv", "rb") as file:        while chunk := file.read(1024 * 1024):            yield chunk@router.get("/download")def download_file():    return StreamingResponse(        iter_file(),        media_type="text/csv"    )
# 장점:
# 파일 전체를 메모리에 올리지 않음조각 단위로 응답 가능대용량 다운로드에 적합

# 6. Background Task
# 사용자 요청 안에서 오래 걸리는 작업을 바로 처리하면 안 된다.
# 예:
# 이메일 발송이미지 리사이징AI 분석 요청알림 생성로그 저장
# from fastapi import BackgroundTasksdef send_email(email: str):    print(f"send email to {email}")@router.post("/signup")def signup(    email: str,    background_tasks: BackgroundTasks):    background_tasks.add_task(send_email, email)    return {"message": "signup success"}
# 응답은 빠르게 반환하고, 이메일 발송은 뒤에서 처리한다.

# 7. Queue 기반 처리
# BackgroundTasks는 간단한 작업에는 괜찮지만, 실무 대용량 작업에는 한계가 있다.
# BackgroundTasks 한계:- 서버 재시작 시 작업 유실 가능- 작업 재시도 어려움- 워커 분리 어려움- 대량 작업 처리에 약함
# 그래서 실무에서는 Queue를 쓴다.
# FastAPI  ↓RabbitMQ / Redis Queue / Kafka  ↓Worker  ↓DB / 외부 API / AI API
# 예:
# 이미지 업로드 요청→ FastAPI는 작업 ID만 반환→ Queue에 이미지 분석 작업 등록→ Worker가 비동기로 처리→ 결과 DB 저장→ 사용자는 상태 조회 API로 확인

# 8. DB Index / Query 최적화
# 대용량에서는 DB가 가장 먼저 병목이 된다.
# 나쁜 예:
# SELECT * FROM users WHERE email = 'a@test.com';
# email에 인덱스가 없으면 전체 테이블을 스캔할 수 있다.
# 좋은 예:
# CREATE INDEX idx_users_email ON users(email);
# 자주 인덱스를 고려하는 컬럼:
# WHERE 조건에 자주 쓰는 컬럼JOIN 조건 컬럼ORDER BY 컬럼검색 기준 컬럼외래키 컬럼

# 9. 필요한 컬럼만 조회
# 나쁜 예:
# users = db.query(User).all()
# 좋은 예:
# users = (    db.query(User.id, User.name, User.email)    .limit(20)    .all())
# 장점:
# 네트워크 전송량 감소메모리 사용량 감소DB I/O 감소

# 10. Cache
# 반복 조회가 많은 데이터는 Redis 캐싱을 고려한다.
# 예:
# 인기 게시글상품 상세사용자 프로필설정 정보랭킹추천 결과
# 흐름:
# 1. Redis에서 먼저 조회2. 없으면 DB 조회3. DB 결과를 Redis에 저장4. 다음 요청부터 Redis 응답
# @router.get("/products/{product_id}")def get_product(product_id: int):    cached = redis.get(f"product:{product_id}")    if cached:        return json.loads(cached)    product = product_service.get_product(product_id)    redis.setex(        f"product:{product_id}",        60,        json.dumps(product)    )    return product

# 11. 대용량 업로드 처리
# 파일 업로드도 전략이 필요하다.
# 나쁜 방식:
# 파일을 서버 메모리에 전부 올림
# 좋은 방식:
# chunk 단위 처리임시 파일 저장S3 같은 Object Storage 직접 업로드업로드 후 비동기 처리
# 예:
# 이미지 업로드→ S3 저장→ Queue에 분석 작업 등록→ Worker가 AI 분석→ 결과 저장

# 12. 실무 판단 기준
# 작업이 1초 이내:- 동기 처리 가능작업이 1~3초:- 비동기 처리 고려작업이 3초 이상:- Queue / Worker 분리 고려외부 API 호출:- timeout, retry, fallback 필수대량 조회:- pagination 필수반복 조회:- cache 고려

# 13. Spring Boot와 비교
# FastAPI                         Spring BootBackgroundTasks                 @AsyncCelery/RQ/Arq Worker             RabbitMQ Consumer / Kafka ConsumerStreamingResponse               StreamingResponseBodyDepends                         DISQLAlchemy query                 JPA / QuerydslRedis cache                     RedisTemplate / CacheManagerUvicorn/Gunicorn worker          Tomcat thread / scale-out

# 14. 한 줄 정리
# FastAPI 대용량 처리는 “한 번에 많이 처리하지 않는 구조”가 핵심이다.
# 즉,
# 조회는 나눠서,파일은 스트리밍으로,무거운 작업은 큐로,반복 데이터는 캐시로,DB는 인덱스와 쿼리 최적화로 처리한다.