from fastapi import APIRouter, HTTPException
from ..ai.service import ai_service
from pydantic import BaseModel

router = APIRouter(prefix="/ai", tags=["AI"])

class TextGenerationRequest(BaseModel):
    model_name: str
    prompt: str
    max_length: int = 200

@router.post("/generate")
async def generate_text(request: TextGenerationRequest):
    if not ai_service.get_model(request.model_name):
        raise HTTPException(status_code=404, detail=f"Model {request.model_name} not available")
    
    try:
        result = ai_service.generate_text(
            request.model_name,
            request.prompt,
            request.max_length
        )
        return {"result": result}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
