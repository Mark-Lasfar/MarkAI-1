# backend/app/routers/multimedia_router.py
from fastapi import APIRouter, UploadFile, File
from media_tools.multimedia_engine import VideoEditor, AudioProcessor
from file_processor.advanced_tools import AdvancedFileProcessor

router = APIRouter()

@router.post("/video/add_subtitles")
async def add_subtitles_to_video(
    video: UploadFile = File(...),
    subtitle_text: str
):
    video_path = f"/tmp/{video.filename}"
    with open(video_path, "wb") as buffer:
        buffer.write(await video.read())
    
    output_path = f"/tmp/subtitled_{video.filename}"
    VideoEditor.add_subtitles(video_path, subtitle_text, output_path)
    
    return FileResponse(output_path)

@router.post("/convert_image")
async def convert_image_format(
    image: UploadFile = File(...),
    target_format: str = "webp"
):
    image_path = f"/tmp/{image.filename}"
    with open(image_path, "wb") as buffer:
        buffer.write(await image.read())
    
    output_path = AdvancedFileProcessor.convert_image_format(image_path, target_format)
    return FileResponse(output_path)