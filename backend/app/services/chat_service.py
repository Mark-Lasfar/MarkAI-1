# backend/app/services/chat_service.py
from fastapi import UploadFile, HTTPException
from pathlib import Path
import shutil
import uuid
from typing import Optional, Dict, Any
from datetime import datetime
from ..core.ai_manager import AIManager
from ..models.chat import Message
from ..config import settings

class ChatService:
    def __init__(self):
        self.ai_manager = AIManager()
        self.upload_dir = settings.UPLOAD_DIR / "chat"
        self.upload_dir.mkdir(parents=True, exist_ok=True)

    async def process_message(self, message: str) -> Message:
        """
        معالجة الرسائل النصية وإرجاع كائن Message
        
        Args:
            message: النص المدخل من المستخدم
            
        Returns:
            Message: كائن الرسالة المحتوي على الرد
            
        Raises:
            HTTPException: عند فشل المعالجة
        """
        try:
            # معالجة النص باستخدام الذكاء الاصطناعي
            ai_response = await self.ai_manager.process("text", message)
            
            return Message(
                content=ai_response.get("data", {}).get("processed_text", "No response"),
                is_user=False,
                timestamp=datetime.now(),
                meta={
                    "status": "success",
                    "request_id": ai_response.get("request_id")
                }
            )
            
        except HTTPException:
            raise
        except Exception as e:
            raise HTTPException(
                status_code=500,
                detail=f"فشل معالجة الرسالة: {str(e)}"
            )

    async def process_file(
        self,
        file: UploadFile,
        process_type: Optional[str] = "auto"
    ) -> Dict[str, Any]:
        """
        معالجة الملفات المرفوعة بأنواعها المختلفة
        
        Args:
            file: الملف المرفوع
            process_type: نوع المعالجة (auto/image/audio/document)
            
        Returns:
            dict: نتائج المعالجة مع البيانات الوصفية
            
        Raises:
            HTTPException: عند فشل المعالجة
        """
        file_path = None
        try:
            # حفظ الملف مؤقتاً
            file_path = self.upload_dir / f"{uuid.uuid4()}_{file.filename}"
            with file_path.open("wb") as buffer:
                shutil.copyfileobj(file.file, buffer)

            # تحديد نوع المحتوى تلقائياً
            if process_type == "auto":
                content_type = file.content_type.split("/")[0] if file.content_type else ""
                process_type = content_type if content_type in ["image", "audio"] else "document"

            # المعالجة باستخدام AIManager
            result = await self.ai_manager.process(process_type, file_path)
            
            return {
                "status": "success",
                "filename": file.filename,
                "type": process_type,
                "result": result.get("data", {}),
                "request_id": result.get("request_id"),
                "timestamp": datetime.now().isoformat()
            }

        except HTTPException:
            raise
        except Exception as e:
            raise HTTPException(
                status_code=500,
                detail=f"فشل معالجة الملف: {str(e)}"
            )
        finally:
            # تنظيف الملف المؤقت
            if file_path and file_path.exists():
                file_path.unlink()

    async def process_file_simple(self, file: UploadFile) -> Dict[str, Any]:
        """
        واجهة مبسطة لمعالجة الملفات (للتكامل مع الأنظمة القديمة)
        
        Args:
            file: الملف المرفوع
            
        Returns:
            dict: المعلومات الأساسية عن الملف
        """
        return {
            "filename": file.filename,
            "content_type": file.content_type,
            "message": "File received successfully",
            "timestamp": datetime.now().isoformat()
        }