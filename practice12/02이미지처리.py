# 1. 이미지 처리란?

# 업로드된 이미지를 서버에서 가공하는 것

# 대표적인 처리:

# - 이미지 리사이즈 (썸네일)
# - 포맷 변환 (png → jpg)
# - 압축
# - 크롭
# - 메타데이터 추출
# - AI 분석 (OCR, 객체 인식 등)
# 2. 기본 흐름
# 1. 파일 업로드 (UploadFile)
# 2. 이미지 라이브러리로 열기
# 3. 가공 (resize, crop 등)
# 4. 저장 또는 반환
# 3. 필수 라이브러리

# 이미지 처리는 보통 Python의
# 👉 Pillow 사용

# 설치:

# pip install pillow
# 4. 기본 이미지 열기
from fastapi import FastAPI, UploadFile, File
from PIL import Image
import io

app = FastAPI()

@app.post("/image-info")
async def image_info(file: UploadFile = File(...)):
    contents = await file.read()

    image = Image.open(io.BytesIO(contents))

    return {
        "format": image.format,
        "size": image.size,
        "mode": image.mode
    }
# 설명
# await file.read()

# → 파일을 bytes로 읽음

# io.BytesIO(contents)

# → 메모리에서 파일처럼 다루기

# Image.open(...)

# → 이미지 객체 생성

# 5. 이미지 리사이즈 (핵심)
@app.post("/resize")
async def resize_image(file: UploadFile = File(...)):
    contents = await file.read()
    image = Image.open(io.BytesIO(contents))

    resized_image = image.resize((200, 200))

    output = io.BytesIO()
    resized_image.save(output, format="JPEG")

    return {"message": "리사이즈 완료"}
# 핵심 포인트
# image.resize((width, height))
# (200, 200) → 썸네일 생성
# 6. 이미지 저장까지 포함
# import uuid
# import os

# UPLOAD_DIR = "images"
# os.makedirs(UPLOAD_DIR, exist_ok=True)

# @app.post("/upload-image")
# async def upload_image(file: UploadFile = File(...)):
#     contents = await file.read()
#     image = Image.open(io.BytesIO(contents))

#     image = image.resize((300, 300))

#     filename = f"{uuid.uuid4()}.jpg"
#     path = os.path.join(UPLOAD_DIR, filename)

#     image.save(path, format="JPEG")

#     return {
#         "filename": filename,
#         "path": path
#     }
# 7. 이미지 검증 (실무 필수)

# 이미지인지 확인해야 한다.

# if file.content_type not in ["image/jpeg", "image/png"]:
#     return {"error": "이미지 파일만 업로드 가능"}

# 또는 Pillow로 검증:

# try:
#     image = Image.open(io.BytesIO(contents))
#     image.verify()
# except Exception:
#     return {"error": "유효하지 않은 이미지"}
# 8. 실무 패턴 (중요)
# [업로드 서버]
#         ↓
# [이미지 처리 (resize, 압축)]
#         ↓
# [S3 저장]
#         ↓
# [DB에 URL 저장]
# 9. AI랑 연결하면

# 너가 하고 있는 방향 기준으로 보면:

# 이미지 업로드
# → Pillow로 전처리 (사이즈 줄이기)
# → LLM / Vision API (Gemini 등)
# → 결과 JSON 반환

# 즉:

# 👉 "이미지 처리 = AI 입력 최적화 단계"

# 10. 한 줄 정리

# 이미지 처리는 UploadFile로 받은 파일을 Pillow로 열어서 resize/검증/가공 후 저장하거나 AI 입력으로 넘기는 과정이다.