# backend/file_processor/core.py
import zipfile
import tarfile
import magic
from pathlib import Path

class FileProcessor:
    @staticmethod
    def detect_file_type(file_path):
        return magic.from_file(file_path, mime=True)

    @staticmethod
    def compress_to_zip(input_paths, output_path):
        with zipfile.ZipFile(output_path, 'w') as zipf:
            for path in input_paths:
                zipf.write(path)

    @staticmethod
    def extract_archive(archive_path, output_dir):
        if archive_path.endswith('.zip'):
            with zipfile.ZipFile(archive_path, 'r') as zipf:
                zipf.extractall(output_dir)
        elif archive_path.endswith('.tar.gz'):
            with tarfile.open(archive_path, 'r:gz') as tar:
                tar.extractall(output_dir)