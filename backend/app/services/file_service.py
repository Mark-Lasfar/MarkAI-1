# backend/app/services/file_service.py
import hashlib
import aiofiles
from pathlib import Path
from fastapi import UploadFile
from typing import Optional
from ..core.config import settings

class FileService:
    CHUNK_SIZE = 1024 * 1024  # 1MB

    def __init__(self):
        self.storage_path = Path(settings.STORAGE_PATH)
        self.storage_path.mkdir(exist_ok=True)

    async def save_file(self, file: UploadFile) -> str:
        file_hash = await self._calculate_hash(file)
        file_dir = self.storage_path / file_hash[:2] / file_hash[2:4]
        file_dir.mkdir(parents=True, exist_ok=True)
        file_path = file_dir / file_hash

        if file_path.exists():
            return file_hash

        async with aiofiles.open(file_path, 'wb') as f:
            while chunk := await file.read(self.CHUNK_SIZE):
                await f.write(chunk)

        return file_hash

    async def _calculate_hash(self, file: UploadFile) -> str:
        hash_obj = hashlib.sha256()
        await file.seek(0)
        
        while chunk := await file.read(self.CUNK_SIZE):
            hash_obj.update(chunk)
        
        await file.seek(0)
        return hash_obj.hexdigest()