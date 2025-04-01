# backend/app/ai/multimodal_manager.py
import torch
from transformers import (
    AutoModelForCausalLM,
    AutoModelForSeq2SeqLM,
    AutoTokenizer,
    pipeline
)
from typing import Union, BinaryIO
import numpy as np

class MultimodalManager:
    def __init__(self):
        self.device = "cuda" if torch.cuda.is_available() else "cpu"
        self.load_models()
        
    def load_models(self):
        """تحميل جميع النماذج بذكاء مع إدارة الذاكرة"""
        self.models = {
            'text': {
                'ar': self._load_text_model("aubmindlab/aragpt2-base"),
                'en': self._load_text_model("gpt2")
            },
            'image': pipeline("image-to-text", model="Salesforce/blip-image-captioning-base"),
            'audio': pipeline("automatic-speech-recognition", model="openai/whisper-medium")
        }
    
    def _load_text_model(self, model_name):
        """تحميل نموذج نصي مع تحسين الذاكرة"""
        tokenizer = AutoTokenizer.from_pretrained(model_name)
        model = AutoModelForCausalLM.from_pretrained(
            model_name,
            torch_dtype=torch.float16,
            low_cpu_mem_usage=True
        ).to(self.device)
        return {'model': model, 'tokenizer': tokenizer}

    async def process(self, input_data: Union[str, BinaryIO], input_type: str, lang: str = 'ar'):
        """معالجة ذكية حسب نوع المدخلات"""
        try:
            if input_type == 'text':
                return await self._process_text(input_data, lang)
            elif input_type == 'image':
                return await self._process_image(input_data)
            elif input_type == 'audio':
                return await self._process_audio(input_data)
            else:
                raise ValueError("نوع المدخلات غير مدعوم")
        except Exception as e:
            raise RuntimeError(f"خطأ في المعالجة: {str(e)}")

    async def _process_text(self, text: str, lang: str):
        """معالجة النص مع الترجمة التلقائية"""
        inputs = self.models['text'][lang]['tokenizer'](text, return_tensors="pt").to(self.device)
        outputs = self.models['text'][lang]['model'].generate(**inputs, max_length=200)
        return self.models['text'][lang]['tokenizer'].decode(outputs[0], skip_special_tokens=True)

    async def _process_image(self, image: BinaryIO):
        """معالجة الصورة مع وصفها"""
        return self.models['image'](image)

    async def _process_audio(self, audio: BinaryIO):
        """معالجة الصوت مع ترجمته"""
        return self.models['audio'](audio)