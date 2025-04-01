import os
from typing import Optional
from transformers import (
    AutoModelForCausalLM,
    AutoTokenizer,
    pipeline,
    BitsAndBytesConfig
)
from ..config import settings
import torch

class AIService:
    _instance = None
    _models = {}
    
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(AIService, cls).__new__(cls)
            cls._instance.init_models()
        return cls._instance
    
    def init_models(self):
        """تهيئة النماذج المتاحة"""
        model_paths = {
            "bloom": os.path.join(settings.AI_MODELS_DIR, "bloom-7b1"),
            "falcon": os.path.join(settings.AI_MODELS_DIR, "falcon-7b"),
            "gpt-j": os.path.join(settings.AI_MODELS_DIR, "gpt-j-6B"),
        }
        
        # تكوين التحميل الأمثل للنماذج
        bnb_config = BitsAndBytesConfig(
            load_in_4bit=True,
            bnb_4bit_use_double_quant=True,
            bnb_4bit_quant_type="nf4",
            bnb_4bit_compute_dtype=torch.bfloat16
        )
        
        for name, path in model_paths.items():
            if os.path.exists(path):
                try:
                    tokenizer = AutoTokenizer.from_pretrained(path)
                    model = AutoModelForCausalLM.from_pretrained(
                        path,
                        device_map="auto",
                        quantization_config=bnb_config,
                        torch_dtype=torch.bfloat16
                    )
                    self._models[name] = {
                        "model": model,
                        "tokenizer": tokenizer,
                        "pipe": pipeline(
                            "text-generation",
                            model=model,
                            tokenizer=tokenizer,
                            device_map="auto"
                        )
                    }
                    print(f"✅ تم تحميل النموذج {name} بنجاح")
                except Exception as e:
                    print(f"❌ فشل تحميل النموذج {name}: {str(e)}")
    
    def get_model(self, model_name: str) -> Optional[dict]:
        """استرجاع نموذج معين"""
        return self._models.get(model_name.lower())
    
    def generate_text(self, model_name: str, prompt: str, max_length: int = 200) -> str:
        """توليد نص باستخدام نموذج معين"""
        model_data = self.get_model(model_name)
        if not model_data:
            return f"النموذج {model_name} غير متاح"
        
        try:
            output = model_data["pipe"](
                prompt,
                max_length=max_length,
                do_sample=True,
                top_k=50,
                top_p=0.95,
                temperature=0.7
            )
            return output[0]["generated_text"]
        except Exception as e:
            return f"حدث خطأ أثناء توليد النص: {str(e)}"

# تهيئة الخدمة عند الاستيراد
ai_service = AIService()
