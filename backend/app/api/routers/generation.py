# backend/app/api/routers/generation.py
from fastapi import APIRouter, UploadFile, File, Depends
from ..services import (
    media_generator,
    code_generator,
    content_creator,
    file_processor
)
from ..core.auth import get_current_user

router = APIRouter(prefix="/generate", tags=["Generation"])

@router.post("/video")
async def generate_video(prompt: str, user=Depends(get_current_user)):
    return await media_generator.generate_video(prompt)

@router.post("/code")
async def generate_code(requirements: str, user=Depends(get_current_user)):
    return await code_generator.generate(requirements)

@router.post("/story")
async def generate_story(prompt: str, user=Depends(get_current_user)):
    return await content_creator.generate_story(prompt)

@router.post("/process-file")
async def process_file(file: UploadFile = File(...), user=Depends(get_current_user)):
    return await file_processor.process(file)