# backend/app/core/file_manager.py
import shutil
from pathlib import Path
from ..config import settings

class FileManager:
    @staticmethod
    async def save_user_file(user_id: str, file_path: str):
        user_dir = Path(settings.USER_FILES_DIR) / str(user_id)
        user_dir.mkdir(exist_ok=True)
        dest = user_dir / Path(file_path).name
        shutil.move(file_path, dest)
        return str(dest)