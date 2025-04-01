# backend/app/services/file_manager.py
import os
import hashlib
from pathlib import Path
from fastapi import UploadFile
from typing import Optional
from ..core.config import settings

class FileManager:
    CHUNK_SIZE = 1024 * 1024 * 10  # 10MB

    def __init__(self):
        self.storage_path = Path(settings.STORAGE_PATH)
        self.storage_path.mkdir(exist_ok=True)

    async def save_file(self, file: UploadFile) -> str:
        file_hash = await self._calculate_hash(file)
        file_path = self.storage_path / file_hash[:2] / file_hash[2:4] / file_hash
        
        if file_path.exists():
            return file_hash

        file_path.parent.mkdir(parents=True, exist_ok=True)
        
        with open(file_path, "wb") as buffer:
            while chunk := await file.read(self.CHUNK_SIZE):
                buffer.write(chunk)
        
        return file_hash

    async def _calculate_hash(self, file: UploadFile) -> str:
        hash_obj = hashlib.sha256()
        await file.seek(0)
        
        while chunk := await file.read(self.CHUNK_SIZE):
            hash_obj.update(chunk)
        
        await file.seek(0)
        return hash_obj.hexdigest()

    def get_file_path(self, file_hash: str) -> Optional[Path]:
        file_path = self.storage_path / file_hash[:2] / file_hash[2:4] / file_hash
        return file_path if file_path.exists() else None