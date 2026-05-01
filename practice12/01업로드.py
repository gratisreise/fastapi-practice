# 1. 파일 업로드란?

# 클라이언트가 서버로 파일을 보내는 기능이다.

# 예를 들면:

# 사용자 → 이미지 선택 → 서버에 업로드
# 사용자 → PDF 첨부 → 서버 저장
# 사용자 → CSV 파일 업로드 → 서버에서 데이터 분석

# FastAPI에서는 파일 업로드를 처리할 때 주로 UploadFile을 사용한다.

# 2. 기본 코드
# from fastapi import FastAPI, UploadFile, File

# app = FastAPI()

# @app.post("/upload")
# async def upload_file(file: UploadFile = File(...)):
#     return {
#         "filename": file.filename,
#         "content_type": file.content_type
#     }
# 3. 핵심 구조
# file: UploadFile = File(...)

# 의미는 다음과 같다.

# file          → 클라이언트가 보낸 파일
# UploadFile    → FastAPI의 업로드 파일 객체
# File(...)     → 이 값은 파일/form-data에서 받아온다는 의미

# 즉, JSON Body가 아니라 multipart/form-data 방식으로 파일을 받는다.

# 4. UploadFile이 제공하는 값
# file.filename

# 업로드된 원본 파일명

# file.content_type

# 파일 타입

# 예:

# image/png
# image/jpeg
# application/pdf
# text/csv
# await file.read()

# 파일 내용을 바이트로 읽기

# 5. 파일 저장 예제
# from fastapi import FastAPI, UploadFile, File
# import shutil

# app = FastAPI()

# @app.post("/upload")
# async def upload_file(file: UploadFile = File(...)):
#     save_path = f"uploads/{file.filename}"

#     with open(save_path, "wb") as buffer:
#         shutil.copyfileobj(file.file, buffer)

#     return {
#         "message": "파일 업로드 성공",
#         "filename": file.filename,
#         "saved_path": save_path
#     }

# 6. 여기서 중요한 점
# "wb"

# 는 write binary라는 뜻이다.

# 파일은 텍스트가 아니라 이미지, PDF, zip 등 바이너리 데이터일 수 있기 때문에 wb로 저장한다.

# file.file

# 은 실제 파일처럼 다룰 수 있는 객체다.

# shutil.copyfileobj(file.file, buffer)

# 는 업로드된 파일 내용을 서버 파일로 복사한다.

# 7. 실무에서 주의할 점

# 원본 파일명을 그대로 저장하면 위험할 수 있다.

# 예를 들어:

# ../../secret.txt

# 같은 파일명이 들어올 수도 있다.

# 그래서 실무에서는 보통 UUID를 붙인다.

# import uuid
# from fastapi import FastAPI, UploadFile, File
# import os
# import shutil

# app = FastAPI()

# UPLOAD_DIR = "uploads"
# os.makedirs(UPLOAD_DIR, exist_ok=True)

# @app.post("/upload")
# async def upload_file(file: UploadFile = File(...)):
#     extension = file.filename.split(".")[-1]
#     saved_filename = f"{uuid.uuid4()}.{extension}"
#     save_path = os.path.join(UPLOAD_DIR, saved_filename)

#     with open(save_path, "wb") as buffer:
#         shutil.copyfileobj(file.file, buffer)

#     return {
#         "original_filename": file.filename,
#         "saved_filename": saved_filename,
#         "saved_path": save_path
#     }
# 8. 흐름 정리
# 1. 클라이언트가 multipart/form-data로 파일 전송
# 2. FastAPI가 UploadFile 객체로 받음
# 3. filename, content_type 확인 가능
# 4. file.file 또는 await file.read()로 내용 접근
# 5. 서버 로컬 디렉터리에 저장
# 6. DB에는 보통 저장 경로나 URL만 저장