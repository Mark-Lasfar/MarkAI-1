# backend/app/services/ai_service.py
from transformers import pipeline
from ..core.config import settings
import torch

class AIService:
    def __init__(self):
        self.text_generators = {
            'bloom': pipeline("text-generation", model=str(settings.AI_MODELS_DIR/"bloom-7b1")),
            'falcon': pipeline("text-generation", model=str(settings.AI_MODELS_DIR/"falcon-7b1")),
            'gpt-j': pipeline("text-generation", model=str(settings.AI_MODELS_DIR/"gpt-j-6b"))
        }
    
    async def generate_text(self, prompt: str, model: str = "bloom"):
        generator = self.text_generators.get(model)
        if not generator:
            raise ValueError(f"Model {model} not supported")
        
        return generator(prompt, max_length=200)[0]['generated_text']