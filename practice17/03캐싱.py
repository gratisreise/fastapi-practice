# 좋아. 이번엔 FastAPI 캐싱(Redis) 가자.

# 1. 캐싱이란?

# 캐싱은 자주 쓰는 데이터를 DB 대신 빠른 저장소에 잠깐 저장해두는 것이다.

# DB에서 매번 조회하지 않고
# Redis에서 먼저 꺼내서 응답하는 전략

# 기본 흐름은 이거다.

# Client
#   ↓
# FastAPI
#   ↓
# Redis 먼저 조회
#   ↓
# 있으면 Redis 응답
#   ↓
# 없으면 DB 조회
#   ↓
# DB 결과를 Redis에 저장
#   ↓
# 응답
# 2. 왜 Redis를 쓰는가?

# Redis는 메모리 기반 저장소다.

# DB보다 조회가 빠름
# TTL 설정 가능
# Key-Value 구조라 단순 캐시에 적합
# 랭킹, 세션, 토큰 블랙리스트, Rate Limit에도 사용 가능

# Spring Boot로 치면:

# RedisTemplate
# CacheManager
# StringRedisTemplate

# FastAPI에서는 보통:

# redis-py
# redis.asyncio
# aioredis

# 를 사용한다.

# 요즘은 redis.asyncio를 많이 쓴다.

# 3. 설치
# pip install redis

# 비동기 FastAPI 기준으로는 이렇게 사용한다.

# import redis.asyncio as redis
# 4. Redis 연결 설정
# app/redis_client.py
# import redis.asyncio as redis

# redis_client = redis.Redis(
#     host="localhost",
#     port=6379,
#     db=0,
#     decode_responses=True
# )

# decode_responses=True를 주면 Redis에서 가져온 값이 bytes가 아니라 문자열로 나온다.

# 5. 기본 사용법
# await redis_client.set("name", "kim")
# value = await redis_client.get("name")

# print(value)

# 결과:

# kim

# TTL 설정:

# await redis_client.setex("name", 60, "kim")

# 의미:

# name이라는 key를 60초 동안만 저장
# 6. 상품 상세 캐싱 예제
# 흐름
# GET /products/1 요청
# → Redis에서 product:1 조회
# → 있으면 바로 반환
# → 없으면 DB 조회
# → Redis에 저장
# → 반환
# product_router.py
# from fastapi import APIRouter, Depends
# from sqlalchemy.orm import Session
# from app.database import get_db
# from app.services.product_service import ProductService

# router = APIRouter(prefix="/products", tags=["products"])


# @router.get("/{product_id}")
# async def get_product(
#     product_id: int,
#     db: Session = Depends(get_db)
# ):
#     service = ProductService(db)
#     return await service.get_product(product_id)
# product_service.py
# import json
# from fastapi import HTTPException
# from app.redis_client import redis_client
# from app.repositories.product_repository import ProductRepository


# class ProductService:
#     def __init__(self, db):
#         self.product_repository = ProductRepository(db)

#     async def get_product(self, product_id: int):
#         cache_key = f"product:{product_id}"

#         cached_product = await redis_client.get(cache_key)

#         if cached_product:
#             return json.loads(cached_product)

#         product = self.product_repository.find_by_id(product_id)

#         if product is None:
#             raise HTTPException(
#                 status_code=404,
#                 detail="Product not found"
#             )

#         response = {
#             "id": product.id,
#             "name": product.name,
#             "price": product.price
#         }

#         await redis_client.setex(
#             cache_key,
#             60,
#             json.dumps(response)
#         )

#         return response
# product_repository.py
# from app.models.product import Product


# class ProductRepository:
#     def __init__(self, db):
#         self.db = db

#     def find_by_id(self, product_id: int):
#         return (
#             self.db.query(Product)
#             .filter(Product.id == product_id)
#             .first()
#         )
# 7. Cache Aside 패턴

# 방금 본 방식이 가장 많이 쓰는 Cache Aside 패턴이다.

# 1. 캐시 먼저 조회
# 2. 캐시에 없으면 DB 조회
# 3. DB 결과를 캐시에 저장
# 4. 응답

# 장점:

# 구현이 단순함
# 필요한 데이터만 캐싱 가능
# 장애 시 DB로 fallback 가능

# 단점:

# 첫 요청은 느림
# 데이터 변경 시 캐시 무효화 필요
# 8. 캐시 무효화

# 캐싱에서 제일 중요한 게 이거다.

# DB 데이터가 바뀌었는데 Redis에는 예전 값이 남아있을 수 있음

# 예를 들어 상품 가격이 바뀌었다.

# DB: 12000원
# Redis: 10000원

# 그러면 사용자에게 잘못된 가격을 보여줄 수 있다.

# 그래서 수정/삭제 시 캐시도 같이 삭제한다.

# 상품 수정 예제
# async def update_product(self, product_id: int, request):
#     product = self.product_repository.find_by_id(product_id)

#     if product is None:
#         raise HTTPException(404, "Product not found")

#     product.name = request.name
#     product.price = request.price

#     self.product_repository.save(product)

#     await redis_client.delete(f"product:{product_id}")

#     return {
#         "id": product.id,
#         "name": product.name,
#         "price": product.price
#     }

# 핵심:

# await redis_client.delete(f"product:{product_id}")

# DB가 변경되면 캐시를 지운다.

# 다음 조회 때 다시 DB에서 읽고 Redis에 새로 저장한다.

# 9. TTL을 꼭 설정해야 하는 이유

# 캐시는 영구 저장소가 아니다.

# TTL 없이 저장하면
# 오래된 데이터가 계속 남을 수 있고
# Redis 메모리가 계속 증가한다

# 그래서 보통 캐시는 TTL을 둔다.

# await redis_client.setex(
#     "product:1",
#     60,
#     json.dumps(product)
# )

# TTL 예시:

# 상품 상세: 1~5분
# 인기 게시글: 10~60초
# 사용자 프로필: 1~10분
# 설정 정보: 10분~1시간
# 토큰 블랙리스트: 토큰 만료 시간까지
# 10. 캐싱하면 좋은 데이터
# 자주 조회되는 데이터
# 변경이 자주 일어나지 않는 데이터
# DB 조회 비용이 큰 데이터
# 외부 API 호출 결과
# 랭킹/통계/추천 결과

# 예:

# 상품 상세
# 게시글 상세
# 인기 게시글 목록
# 카테고리 목록
# 사용자 프로필
# AI 추천 결과
# 11. 캐싱하면 위험한 데이터
# 실시간 정확성이 중요한 데이터
# 변경이 매우 잦은 데이터
# 사용자 권한/결제/재고 같은 민감한 데이터

# 예:

# 결제 상태
# 실시간 재고
# 권한 정보
# 계좌 잔액
# 주문 상태

# 이런 데이터는 캐싱하더라도 TTL을 짧게 하거나, 무효화 전략을 강하게 가져가야 한다.

# 12. Redis Key 설계

# 키는 규칙적으로 만들어야 한다.

# 좋은 예:

# product:1
# user:15:profile
# post:100:detail
# ranking:daily:2026-05-04
# recommend:user:10

# 나쁜 예:

# data1
# cache-user
# temp
# abc

# 추천 규칙:

# 도메인:식별자:목적

# 예:

# user:1:profile
# product:3:detail
# meal:10:recommendation
# 13. JSON 직렬화 주의

# Redis에는 객체를 그대로 저장할 수 없다.

# 그래서 보통 JSON 문자열로 바꿔서 저장한다.

# json.dumps(response)

# 꺼낼 때는 다시 dict로 변환한다.

# json.loads(cached_product)

# 주의할 점:

# datetime
# Decimal
# Enum
# ORM 객체

# 이런 값들은 바로 JSON 변환이 안 될 수 있다.

# 그래서 응답용 dict나 Pydantic schema로 변환한 뒤 저장하는 게 좋다.

# 14. FastAPI 실무 구조
# app/
#  ├─ main.py
#  ├─ redis_client.py
#  ├─ api/
#  │   └─ product_router.py
#  ├─ services/
#  │   └─ product_service.py
#  ├─ repositories/
#  │   └─ product_repository.py
#  ├─ schemas/
#  │   └─ product_schema.py
#  └─ models/
#      └─ product.py

# Redis 접근은 보통 Service에서 처리한다.

# Router:
# - 요청/응답

# Service:
# - 캐시 조회
# - DB 조회
# - 캐시 저장
# - 캐시 무효화

# Repository:
# - DB query
# 15. 한 줄 정리
# Redis 캐싱은 DB 조회 전에 Redis를 먼저 확인하고,
# 없을 때만 DB를 조회해서 성능을 높이는 전략이다.

# 실무 핵심은 이거다.

# 캐시 조회 → DB 조회 → 캐시 저장 → 데이터 변경 시 캐시 삭제