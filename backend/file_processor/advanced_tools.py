# backend/file_processor/advanced_tools.py
import os
import patoolib
from PIL import Image, ImageOps

class AdvancedFileProcessor:
    @staticmethod
    def convert_image_format(input_path, output_format='WEBP'):
        """تحويل بين 30 صيغة صورة مختلفة"""
        with Image.open(input_path) as img:
            output_path = f"{os.path.splitext(input_path)[0]}.{output_format.lower()}"
            img.save(output_path, format=output_format)
            return output_path

    @staticmethod
    def handle_rar_files(rar_path, output_dir):
        """دعم فك ضغط RAR بدون تكاليف"""
        patoolib.extract_archive(rar_path, outdir=output_dir)
        return [os.path.join(output_dir, f) for f in os.listdir(output_dir)]

    @staticmethod
    def pdf_to_images(pdf_path):
        """تحويل PDF إلى سلسلة صور (باستخدام pdf2image)"""
        from pdf2image import convert_from_path
        images = convert_from_path(pdf_path)
        return images