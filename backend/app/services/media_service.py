# backend/app/services/media_service.py
import os
from pathlib import Path
from typing import Union, Optional
import tempfile
import ffmpeg
from gtts import gTTS
from fastapi import UploadFile, HTTPException
from ..core.ai import MediaGenerator
from ..core.config import settings
from ..utils.file_utils import cleanup_temp_files

class MediaService:
    @staticmethod
    async def text_to_video(
        text: str,
        output_path: Union[str, Path],
        image_path: Optional[Union[str, Path]] = None,
        duration: int = 10,
        lang: str = 'ar'
    ) -> Path:
        """
        إنشاء فيديو من نص مع الصوت والصورة
        
        Args:
            text: النص المراد تحويله
            output_path: مسار ملف الفيديو الناتج
            image_path: مسار الصورة الخلفية (اختياري)
            duration: مدة الفيديو بالثواني
            lang: لغة النص
            
        Returns:
            مسار الفيديو الناتج
            
        Raises:
            HTTPException: إذا فشلت عملية الإنشاء
        """
        if not image_path:
            image_path = settings.DEFAULT_IMAGE_PATH
            
        try:
            with tempfile.NamedTemporaryFile(suffix='.mp3', delete=False) as audio_file:
                # توليد الصوت من النص
                tts = gTTS(text, lang=lang)
                audio_path = audio_file.name
                tts.save(audio_path)
                
                # إنشاء الفيديو
                ffmpeg.input(
                    image_path,
                    loop=1,
                    t=duration
                ).output(
                    str(output_path),
                    vcodec='libx264',
                    acodec='aac',
                    strict='experimental',
                    audio=audio_path
                ).run(overwrite_output=True)
                
            return Path(output_path)
        except Exception as e:
            raise HTTPException(
                status_code=500,
                detail=f"فشل إنشاء الفيديو: {str(e)}"
            )
        finally:
            cleanup_temp_files(audio_path)

    @staticmethod
    async def generate(
        content_type: str,
        prompt: str,
        **kwargs
    ) -> Union[str, bytes, Path]:
        """
        واجهة موحدة لإنشاء المحتوى متعدد الوسائط
        
        يدعم:
        - text: إنشاء نصوص
        - image: إنشاء صور
        - audio: إنشاء صوت
        - video: إنشاء فيديو
        
        Args:
            content_type: نوع المحتوى المراد إنشاؤه
            prompt: النص المحفز للإنشاء
            **kwargs: معاملات إضافية
            
        Returns:
            المحتوى الناتج حسب النوع
        """
        try:
            return await MediaGenerator.generate(content_type, prompt, **kwargs)
        except Exception as e:
            raise HTTPException(
                status_code=500,
                detail=f"فشل إنشاء المحتوى: {str(e)}"
            )

    @staticmethod
    async def process_upload(file: UploadFile) -> Union[str, bytes, Path]:
        """
        معالجة الملفات المرفوعة بأنواعها المختلفة
        
        يدعم:
        - الصور (jpg, png)
        - الصوتيات (mp3, wav)
        - الفيديوهات (mp4)
        
        Args:
            file: الملف المرفوع
            
        Returns:
            نتيجة المعالجة حسب نوع الملف
        """
        try:
            with tempfile.NamedTemporaryFile(delete=False) as temp_file:
                temp_path = temp_file.name
                await file.seek(0)
                content = await file.read()
                temp_file.write(content)
                
            result = await MediaGenerator.process_file(temp_path)
            return result
        except Exception as e:
            raise HTTPException(
                status_code=400,
                detail=f"فشل معالجة الملف: {str(e)}"
            )
        finally:
            if os.path.exists(temp_path):
                os.remove(temp_path)