# backend/ai/multimodal_processor.py
import torch
from transformers import (
    AutoModelForCausalLM,
    AutoModelForSeq2SeqLM,
    AutoTokenizer,
    pipeline
)

class AIMultiModalProcessor:
    def __init__(self):
        self.device = "cuda" if torch.cuda.is_available() else "cpu"
        self.load_models()
        
    def load_models(self):
        """تحميل جميع النماذج بشكل متزامن لتحسين الأداء"""
        self.text_models = {
            'bloom': self._load_model("bigscience/bloom-7b1"),
            'falcon': self._load_model("tiiuae/falcon-7b"),
            'codegen': self._load_model("Salesforce/codegen-16B-mono")
        }
        
        self.multimodal_models = {
            'image_caption': pipeline("image-to-text", model="Salesforce/blip-image-captioning-base"),
            'speech_recognition': pipeline("automatic-speech-recognition", model="openai/whisper-medium")
        }

    def _load_model(self, model_name):
        """تحميل نموذج مع ضبط الذاكرة"""
        tokenizer = AutoTokenizer.from_pretrained(model_name)
        model = AutoModelForCausalLM.from_pretrained(
            model_name,
            torch_dtype=torch.float16 if self.device == "cuda" else torch.float32,
            low_cpu_mem_usage=True
        ).to(self.device)
        return {'model': model, 'tokenizer': tokenizer}

    def process_input(self, input_data, input_type):
        """معالجة متعددة الأنواع مع اكتشاف تلقائي"""
        if input_type == 'text':
            return self._process_text(input_data)
        elif input_type == 'image':
            return self.multimodal_models['image_caption'](input_data)
        elif input_type == 'audio':
            return self.multimodal_models['speech_recognition'](input_data)
        else:
            raise ValueError("نوع الإدخال غير مدعوم")

    def _process_text(self, text):
        """معالجة النص مع اختيار النموذج الأمثل تلقائياً"""
        if "كود" in text or "برمجة" in text:
            model = self.text_models['codegen']
        elif "?" in text or "؟" in text:
            model = self.text_models['falcon']
        else:
            model = self.text_models['bloom']
            
        inputs = model['tokenizer'](text, return_tensors="pt").to(self.device)
        outputs = model['model'].generate(**inputs, max_length=200)
        return model['tokenizer'].decode(outputs[0], skip_special_tokens=True)