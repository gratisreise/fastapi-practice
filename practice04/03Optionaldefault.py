# 3. Optional / default 값
# 개념 한 줄

# 값이 없어도 되는 필드와 기본값을 지정하는 방법

# 1. 기본적으로는 필수값
from pydantic import BaseModel

class UserCreate(BaseModel):
    name: str
    age: int

# 요청 Body:

# {
#   "name": "kim"
# }

# age가 없기 때문에 에러 발생.

# 즉, 기본적으로 타입만 적으면 필수값이야.

# 2. default 값 지정
# class UserCreate(BaseModel):
#     name: str
#     age: int = 20

# 요청 Body:

# {
#   "name": "kim"
# }

# 응답:

# {
#   "name": "kim",
#   "age": 20
# }

# age를 안 보내면 기본값 20이 들어간다.

# 3. Optional 사용
from typing import Optional
from pydantic import BaseModel

class UserCreate(BaseModel):
    name: str
    nickname: Optional[str] = None

# 또는 Python 3.10 이상이면:

class UserCreate(BaseModel):
    name: str
    nickname: str | None = None

# nickname은 없어도 되고, null이어도 된다.

# {
#   "name": "kim"
# }

# 가능.

# {
#   "name": "kim",
#   "nickname": null
# }

# 가능.

# 4. Optional만 쓰면 주의
class UserCreate(BaseModel):
    nickname: Optional[str]

# 이건 의미가 애매해.

# None은 허용하지만, 필드는 여전히 필요할 수 있어.

# 그래서 실무에서는 보통 이렇게 쓴다.

# nickname: str | None = None

# 즉,

# Optional을 쓸 때는 기본값 None까지 같이 주는 게 안전하다.

# 5. Query Parameter에서도 사용 가능
# from fastapi import FastAPI

# app = FastAPI()

# @app.get("/items")
# def read_items(
#     keyword: str | None = None,
#     limit: int = 10
# ):
#     return {
#         "keyword": keyword,
#         "limit": limit
#     }

# 요청:

# GET /items

# 응답:

# {
#   "keyword": null,
#   "limit": 10
# }

# 요청:

# GET /items?keyword=book&limit=5

# 응답:

# {
#   "keyword": "book",
#   "limit": 5
# }
# 실무 감각

# 검색 API를 만들 때 자주 씀.

@app.get("/books")
def search_books(
    keyword: str | None = None,
    category: str | None = None,
    page: int = 1,
    size: int = 20
):
    return {
        "keyword": keyword,
        "category": category,
        "page": page,
        "size": size
    }

# Spring Boot로 치면 이런 느낌이야.

# @RequestParam(required = false) String keyword
# @RequestParam(defaultValue = "1") int page

# FastAPI에서는 타입 힌트와 기본값으로 표현한다.

# 정리
# 형태	의미
# name: str	필수값
# age: int = 20	없으면 기본값 20
# nickname: str | None = None	없어도 됨, null 가능
# limit: int = 10	Query 기본값