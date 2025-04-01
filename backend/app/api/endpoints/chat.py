# backend/app/api/endpoints/chat.py
from fastapi import APIRouter, UploadFile, File, HTTPException
from typing import Optional
from ..services.chat_service import ChatService
from ..core.ai_manager import AIManager

router = APIRouter(
    prefix="/chat",
    tags=["Chat"],
    responses={
        404: {"description": "Not found"},
        500: {"description": "Internal server error"}
    },
)

chat_service = ChatService()
ai_manager = AIManager()

@router.post(
    "",
    summary="Process chat message",
    response_description="AI-generated response",
    operation_id="processChatMessage"
)
@router.post(
    "/",
    include_in_schema=False
)
async def chat(message: str):
    """
    Process text message and return AI response
    
    - **message**: Text input to process
    - **returns**: JSON with AI response
    """
    try:
        response = await ai_manager.process(message, 'text')
        return {
            "status": "success",
            "response": response,
            "type": "text"
        }
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Message processing failed: {str(e)}"
        )

@router.post(
    "/send-message",
    summary="Alternative message endpoint",
    response_description="Processed result",
    operation_id="sendChatMessage"
)
async def send_message(message: str):
    """
    Alternative endpoint for text processing
    
    - **message**: Text input to process
    - **returns**: JSON with processed result
    """
    try:
        return await chat_service.process_message(message)
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Message processing failed: {str(e)}"
        )

@router.post(
    "/send-file",
    summary="Process uploaded file",
    response_description="File processing result",
    operation_id="processChatFile"
)
async def send_file(
    file: UploadFile = File(...),
    process_type: Optional[str] = "auto"
):
    """
    Process uploaded files (images/audio/documents)
    
    - **file**: File to upload (max 10MB)
    - **process_type**: Processing type (auto/image/audio/document)
    - **returns**: JSON with processing results
    """
    try:
        return await chat_service.process_file(file, process_type)
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"File processing failed: {str(e)}"
        )