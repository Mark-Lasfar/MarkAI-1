# backend/app/api/smart_routes.py
from fastapi import APIRouter, UploadFile, File, HTTPException
from ai.multimodal_processor import AIMultiModalProcessor
from file_management.smart_organizer import SmartFileOrganizer
from typing import Optional

router = APIRouter()
ai_processor = AIMultiModalProcessor()
file_organizer = SmartFileOrganizer()

@router.post("/smart-process")
async def smart_process(
    file: Optional[UploadFile] = File(None),
    text: Optional[str] = None,
    process_type: Optional[str] = None
):
    try:
        if file:
            # معالجة الملفات
            file_path = f"/tmp/{file.filename}"
            with open(file_path, "wb") as buffer:
                buffer.write(await file.read())
            
            organized_path = file_organizer.organize_file(file_path)
            file_type = file_organizer.detect_file_type(organized_path)
            
            result = ai_processor.process_input(organized_path, file_type)
        elif text:
            # معالجة النصوص
            result = ai_processor.process_input(text, 'text')
        else:
            raise HTTPException(status_code=400, detail="لا يوجد إدخال للمعالجة")
        
        return {
            "success": True,
            "result": result,
            "processed_at": datetime.now().isoformat()
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))