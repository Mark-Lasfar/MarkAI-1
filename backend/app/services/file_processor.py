# backend/app/services/file_processor.py
import os
from pathlib import Path
from fastapi import UploadFile
from typing import Union
import magic

class FileProcessor:
    SUPPORTED_TYPES = {
        'audio': ['mp3', 'wav', 'ogg'],
        'image': ['jpg', 'png', 'webp'],
        'video': ['mp4', 'mov', 'avi'],
        'document': ['pdf', 'docx', 'txt']
    }

    async def process_file(self, file: UploadFile) -> dict:
        file_type = await self._identify_file_type(file)
        temp_path = await self._save_temp_file(file)
        
        try:
            processor = self._get_processor(file_type)
            result = await processor(temp_path)
            return {'status': 'success', 'type': file_type, 'data': result}
        finally:
            os.remove(temp_path)

    async def _identify_file_type(self, file: UploadFile) -> str:
        content = await file.read(1024)
        await file.seek(0)
        
        mime = magic.from_buffer(content, mime=True)
        for category, extensions in self.SUPPORTED_TYPES.items():
            if any(f'/{ext}' in mime for ext in extensions):
                return category
        return 'unknown'

    async def _save_temp_file(self, file: UploadFile) -> str:
        temp_dir = Path("temp_uploads")
        temp_dir.mkdir(exist_ok=True)
        temp_path = temp_dir / file.filename
        
        with open(temp_path, "wb") as buffer:
            buffer.write(await file.read())
        
        return str(temp_path)