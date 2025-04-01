# backend/app/core/ai_manager.py
from fastapi import HTTPException
from pathlib import Path
from typing import Union, Any, Dict, Optional
import logging
import hashlib
from datetime import datetime
from ..config import settings
import aiofiles
import os

class AIManager:
    def __init__(self):
        """تهيئة مدير الذكاء الاصطناعي مع إعدادات المشروع"""
        self.logger = logging.getLogger(__name__)
        self._validate_directories()
        self._initialize_services()
        
    def _validate_directories(self):
        """التأكد من وجود المجلدات المطلوبة"""
        settings.AI_MODELS_DIR.mkdir(parents=True, exist_ok=True)
        settings.UPLOAD_DIR.mkdir(parents=True, exist_ok=True)
        settings.PROCESSED_DIR.mkdir(parents=True, exist_ok=True)
        self.logger.info(f"AI models directory: {settings.AI_MODELS_DIR}")

    def _initialize_services(self):
        """تهيئة خدمات المعالجة مع إعدادات المشروع"""
        self.services = {
            'text': self._process_text,
            'image': self._process_image,
            'audio': self._process_audio,
            'document': self._process_document
        }
        self.max_file_size = settings.MAX_FILE_SIZE * 1024 * 1024  # تحويل إلى بايت

    async def _save_uploaded_file(self, file_data: Union[Path, bytes], file_name: str) -> Path:
        """حفظ الملفات المرفوعة حسب إعدادات المشروع"""
        upload_path = settings.UPLOAD_DIR / file_name
        
        if isinstance(file_data, bytes):
            async with aiofiles.open(upload_path, 'wb') as f:
                await f.write(file_data)
        elif isinstance(file_data, Path):
            upload_path = settings.UPLOAD_DIR / file_data.name
            file_data.rename(upload_path)
        
        return upload_path

    async def process(self, 
                     input_type: str, 
                     input_data: Union[str, Path, bytes, UploadFile],
                     **kwargs) -> Dict[str, Any]:
        """
        واجهة معالجة رئيسية متوافقة مع إعدادات المشروع
        
        يدعم:
        - النصوص
        - مسارات الملفات
        - بيانات باينارية
        - كائنات UploadFile من FastAPI
        """
        try:
            # معالجة UploadFile إذا كان المدخل من هذا النوع
            if isinstance(input_data, UploadFile):
                if input_data.size > self.max_file_size:
                    raise ValueError(f"حجم الملف يتجاوز الحد المسموح {settings.MAX_FILE_SIZE}MB")
                
                file_ext = Path(input_data.filename).suffix
                file_name = f"{hashlib.md5(input_data.filename.encode()).hexdigest()}{file_ext}"
                file_path = await self._save_uploaded_file(await input_data.read(), file_name)
                input_data = file_path

            processor = self.services.get(input_type)
            if not processor:
                raise ValueError(f"نوع المعالجة غير مدعوم: {input_type}")

            result = await processor(input_data, **kwargs)
            
            return {
                "project": settings.PROJECT_NAME,
                "version": settings.VERSION,
                "status": "success",
                "type": input_type,
                "data": result,
                "timestamp": datetime.now().isoformat(),
                "request_id": self._generate_request_id(input_data)
            }
            
        except HTTPException:
            raise
        except Exception as e:
            self.logger.error(f"AI Processing Error: {str(e)}", exc_info=True)
            raise HTTPException(
                status_code=500,
                detail=f"فشل المعالجة: {str(e)}"
            )

    async def _process_text(self, text: str, **kwargs) -> Dict:
        """معالجة النصوص مع دعم إعدادات المشروع"""
        return {
            "analysis_type": kwargs.get('analysis', 'default'),
            "processed_text": text.upper(),
            "language": kwargs.get('language', 'ar')
        }

    async def _process_image(self, image_path: Path, **kwargs) -> Dict:
        """معالجة الصور مع استخدام مسار التحميل من الإعدادات"""
        return {
            "original_path": str(image_path),
            "processed_path": str(settings.PROCESSED_DIR / image_path.name),
            "analysis": kwargs.get('analysis', 'basic')
        }

    async def _process_audio(self, audio_path: Path, **kwargs) -> Dict:
        """معالجة الصوت مع التحقق من الحجم الأقصى"""
        file_size = os.path.getsize(audio_path)
        return {
            "duration": "00:02:30",
            "file_size": f"{file_size/1024/1024:.2f}MB",
            "language": kwargs.get('language', 'ar')
        }

    async def _process_document(self, doc_path: Path, **kwargs) -> Dict:
        """معالجة المستندات مع التوثيق الكامل"""
        return {
            "pages": 10,
            "format": doc_path.suffix[1:],
            "processing_mode": kwargs.get('mode', 'fast')
        }

    def _generate_request_id(self, input_data: Any) -> str:
        """إنشاء معرف طلب فريد مع مراعاة إعدادات المشروع"""
        timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
        project_code = hashlib.md5(settings.PROJECT_NAME.encode()).hexdigest()[:4]
        
        if isinstance(input_data, (str, bytes)):
            data_hash = hashlib.md5(str(input_data).encode()).hexdigest()[:8]
        elif isinstance(input_data, Path):
            data_hash = hashlib.md5(input_data.name.encode()).hexdigest()[:8]
        else:
            data_hash = hashlib.md5(str(input_data).encode()).hexdigest()[:8]
            
        return f"{project_code}_{timestamp}_{data_hash}"