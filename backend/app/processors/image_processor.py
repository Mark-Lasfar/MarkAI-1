# backend/app/processors/image_processor.py
from PIL import Image
import pytesseract

class ImageProcessor:
    async def process(self, image_path: str):
        # تحليل النص من الصورة
        text = pytesseract.image_to_string(Image.open(image_path), lang='ara')
        
        # معالجة الصورة (مثال: تحويل إلى رمادي)
        img = Image.open(image_path).convert('L')
        processed_path = f"processed/{uuid.uuid4()}.jpg"
        img.save(processed_path)
        
        return {
            "type": "text",
            "data": text,
            "processed_image": processed_path
        }