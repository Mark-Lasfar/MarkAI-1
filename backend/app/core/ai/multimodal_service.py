# backend/app/core/ai/multimodal_service.py
import os
from typing import Optional
from transformers import (
    AutoModelForCausalLM,
    AutoTokenizer,
    pipeline,
    BlipProcessor, 
    BlipForConditionalGeneration,
    SpeechT5Processor,
    SpeechT5ForTextToSpeech
)

class MultimodalAIService:
    def __init__(self):
        self.models = {
            'text': self._load_text_models(),
            'image': self._load_image_models(),
            'audio': self._load_audio_models()
        }
    
    def _load_text_models(self):
        return {
            'bloom': pipeline("text-generation", model="bigscience/bloom-7b1"),
            'falcon': pipeline("text-generation", model="tiiuae/falcon-7b"),
            'gpt-j': pipeline("text-generation", model="EleutherAI/gpt-j-6B")
        }
    
    def _load_image_models(self):
        return {
            'captioning': {
                'processor': BlipProcessor.from_pretrained("Salesforce/blip-image-captioning-base"),
                'model': BlipForConditionalGeneration.from_pretrained("Salesforce/blip-image-captioning-base")
            }
        }
    
    def _load_audio_models(self):
        return {
            'tts': {
                'processor': SpeechT5Processor.from_pretrained("microsoft/speecht5_tts"),
                'model': SpeechT5ForTextToSpeech.from_pretrained("microsoft/speecht5_tts")
            }
        }