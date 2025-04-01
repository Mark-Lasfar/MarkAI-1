# backend/main.py
from fastapi import FastAPI, UploadFile, File, HTTPException, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import JSONResponse, HTMLResponse
from fastapi.openapi.docs import get_swagger_ui_html
from pathlib import Path
import shutil
import uuid
from typing import List, Optional, Union
from .core.config import settings
from .core.database import engine, Base
from .core.api.routers import api_router
from .media_tools.generator import MediaGenerator
from .file_processor.core import FileProcessor
from .core.task_manager import UnifiedTaskManager
from .services import (
    AIService,
    MediaService,
    TextProcessor,
    ImageProcessor,
    AudioProcessor
)
from .routers import (
    ai,
    auth,
    media,
    files,
    subscription,
    rewards,
    chat
)
from fastapi import APIRouter

router = APIRouter()

# Initialize FastAPI application
app = FastAPI(
    title=settings.PROJECT_NAME,
    version=settings.VERSION,
    docs_url=None,  # Disable default docs to use custom
    redoc_url=None, # Disable default redoc
    openapi_url="/openapi.json"
)

# Custom Swagger UI
@app.get("/docs", include_in_schema=False)
async def custom_swagger_ui_html():
    return get_swagger_ui_html(
        openapi_url="/openapi.json",
        title=f"{settings.PROJECT_NAME} - Swagger UI",
        swagger_js_url="/static/swagger-ui/swagger-ui-bundle.js",
        swagger_css_url="/static/swagger-ui/swagger-ui.css",
        swagger_favicon_url="/static/swagger-ui/favicon-32x32.png"
    )

# Middleware configuration
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.ALLOWED_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize task manager
task_manager = UnifiedTaskManager()
app.state.task_manager = task_manager

# Mount routers
app.include_router(api_router, prefix="/api/v1")
app.include_router(ai.router, prefix="/api/ai")
app.include_router(auth.router, prefix="/api/auth")
app.include_router(media.router, prefix="/api/media")
app.include_router(files.router, prefix="/api/files")
app.include_router(subscription.router, prefix="/api/subscription")
app.include_router(rewards.router, prefix="/api/rewards")
app.include_router(chat.router, prefix="/api/chat")

# Create storage directories
UPLOAD_DIR = Path(settings.UPLOAD_DIR)
PROCESSED_DIR = Path(settings.PROCESSED_DIR)
UPLOAD_DIR.mkdir(parents=True, exist_ok=True)
PROCESSED_DIR.mkdir(parents=True, exist_ok=True)

# Static files
app.mount("/static", StaticFiles(directory="static"), name="static")

@app.on_event("startup")
async def startup():
    """Initialize application services"""
    # Create database tables
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    
    # Initialize AI services
    from .core.initialization import initialize_services
    await initialize_services()

@app.on_event("shutdown")
async def shutdown():
    """Cleanup resources on shutdown"""
    await engine.dispose()
    await task_manager.shutdown()

@app.get("/openapi.json", include_in_schema=False)
async def get_openapi():
    return JSONResponse(app.openapi())

# API Endpoints
@app.post("/api/process")
async def process_content(
    file: Optional[UploadFile] = File(None),
    text: Optional[str] = None,
    content_type: str = "auto"
):
    """
    Unified content processing endpoint
    
    Supports:
    - File uploads (images, audio, documents)
    - Direct text processing
    """
    try:
        ai_service = AIService()

        if file:
            # Save uploaded file
            file_path = UPLOAD_DIR / f"{uuid.uuid4()}_{file.filename}"
            with file_path.open("wb") as buffer:
                shutil.copyfileobj(file.file, buffer)

            # Auto-detect content type if not specified
            if content_type == "auto":
                content_type = file.content_type.split("/")[0]

            result = await ai_service.process(content_type, file_path)
            
            # Move to processed directory
            processed_path = PROCESSED_DIR / file_path.name
            file_path.rename(processed_path)

        elif text:
            result = await ai_service.process("text", text)
        else:
            raise HTTPException(status_code=400, detail="No input provided for processing")

        return {"success": True, "result": result}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/chat", 
    summary="معالجة رسالة محادثة",
    description="يتلقى نص الرسالة ويعيد رد الذكاء الاصطناعي",
    response_description="كائن الرسالة مع الرد"
)
async def chat_handler():
    pass

@app.post("/api/tasks")
async def create_processing_task(
    request_type: str,
    input_data: Union[str, dict, UploadFile] = None,
    params: dict = {}
):
    """
    Create asynchronous processing task
    
    Supported request types:
    - text_to_video
    - document_analysis
    - image_processing
    - audio_transcription
    """
    try:
        if request_type == "text_to_video":
            task_id = task_manager.submit_task(
                MediaService.text_to_video,
                input_data,
                params.get('style', 'default')
            )
        elif request_type == "document_analysis":
            task_id = task_manager.submit_task(
                AIService.analyze_document,
                input_data,
                params.get('analysis_type', 'summary')
            )
        elif request_type == "image_processing":
            task_id = task_manager.submit_task(
                ImageProcessor.process_image,
                input_data,
                params
            )
        elif request_type == "audio_transcription":
            task_id = task_manager.submit_task(
                AudioProcessor.transcribe,
                input_data,
                params
            )
        else:
            raise HTTPException(status_code=400, detail="Unsupported request type")

        return {"task_id": task_id, "status": "queued"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/tasks/{task_id}")
async def get_task_status(task_id: str):
    """Check status of a processing task"""
    task = task_manager.get_task_status(task_id)
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    return task

@app.post("/api/chat/files", include_in_schema=True)
async def handle_chat_file_upload(file: UploadFile = File(...)):
    """
    معالجة ملفات المحادثة المرفوعة
    """
    try:
        file_path = UPLOAD_DIR / f"chat_{uuid.uuid4()}{Path(file.filename).suffix}"
        with file_path.open("wb") as buffer:
            shutil.copyfileobj(file.file, buffer)
        
        return {
            "status": "success",
            "filename": file.filename,
            "message": "تم استلام الملف بنجاح"
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/api/files/process")
async def process_uploaded_file(file: UploadFile = File(...)):
    """
    Process uploaded files (zip, audio, documents)
    """
    try:
        temp_path = UPLOAD_DIR / file.filename
        
        # Save uploaded file
        with temp_path.open("wb") as buffer:
            shutil.copyfileobj(file.file, buffer)

        if file.filename.endswith('.zip'):
            # Process archive files
            extract_path = UPLOAD_DIR / "extracted"
            extract_path.mkdir(exist_ok=True)
            FileProcessor.extract_archive(temp_path, extract_path)
            return {"status": "extracted", "path": str(extract_path)}
        
        elif file.filename.endswith(('.mp3', '.wav', '.ogg')):
            # Process audio files
            text = await AudioProcessor().speech_to_text(temp_path)
            return {"text": text}
        
        elif file.filename.endswith(('.pdf', '.docx', '.txt')):
            # Process documents
            content = FileProcessor.extract_text(temp_path)
            return {"content": content}
        
        else:
            raise HTTPException(status_code=400, detail="Unsupported file type")
    finally:
        if temp_path.exists():
            temp_path.unlink()