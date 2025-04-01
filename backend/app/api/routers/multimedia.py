# backend/app/api/routers/multimedia.py
from fastapi import UploadFile, File

@router.post("/generate_video")
async def create_video_from_text(text: str):
    video_path = media_service.text_to_video(text, "output.mp4")
    return FileResponse(video_path)

@router.post("/process_file")
async def process_uploaded_file(file: UploadFile = File(...)):
    file_path = f"uploads/{file.filename}"
    with open(file_path, "wb") as buffer:
        buffer.write(file.file.read())
    
    # معالجة الملف هنا
    return {"status": "processed"}