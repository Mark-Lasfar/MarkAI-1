# backend/file_management/smart_organizer.py
import os
import shutil
from pathlib import Path
import filetype

class SmartFileOrganizer:
    def __init__(self):
        self.work_dir = Path("/app/workspace")
        self.create_default_folders()

    def create_default_folders(self):
        """إنشاء هيكل مجلدات ذكي"""
        folders = [
            'uploads',
            'processed',
            'temp',
            'media/videos',
            'media/audios',
            'documents',
            'archives'
        ]
        for folder in folders:
            (self.work_dir / folder).mkdir(parents=True, exist_ok=True)

    def organize_file(self, file_path):
        """تنظيم الملفات تلقائياً حسب النوع"""
        file_type = self.detect_file_type(file_path)
        dest_folder = self.get_destination_folder(file_type)
        
        new_path = self.work_dir / dest_folder / Path(file_path).name
        shutil.move(file_path, new_path)
        return new_path

    def detect_file_type(self, file_path):
        """كشف نوع الملف بدقة عالية"""
        kind = filetype.guess(file_path)
        if kind is None:
            return 'unknown'
        
        return kind.mime.split('/')[0]  # image, video, audio, etc.

    def get_destination_folder(self, file_type):
        """تحديد مجلد الوجهة بناءً على نوع الملف"""
        mapping = {
            'image': 'media/images',
            'video': 'media/videos',
            'audio': 'media/audios',
            'application/pdf': 'documents',
            'application/zip': 'archives',
            'application/x-rar': 'archives'
        }
        return mapping.get(file_type, 'temp')