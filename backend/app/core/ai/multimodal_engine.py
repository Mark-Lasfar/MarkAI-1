# backend/app/core/ai/multimodal_engine.py
import torch
from transformers import (
    BlipProcessor, 
    BlipForConditionalGeneration,
    SpeechT5Processor,
    SpeechT5ForTextToSpeech,
    AutoModelForCausalLM,
    AutoTokenizer
)
from typing import Union, Optional
from pathlib import Path

class MultimodalAI:
    def __init__(self, models_dir: Path):
        self.device = "cuda" if torch.cuda.is_available() else "cpu"
        self.models = {
            'text': self._load_text_models(models_dir),
            'image': self._load_image_models(),
            'audio': self._load_audio_models()
        }

    def _load_text_models(self, models_dir):
        return {
            'bloom': {
                'model': AutoModelForCausalLM.from_pretrained(
                    models_dir / "bloom-7b1",
                    device_map="auto",
                    torch_dtype=torch.float16
                ),
                'tokenizer': AutoTokenizer.from_pretrained(models_dir / "bloom-7b1")
            },
            'falcon': {
                'model': AutoModelForCausalLM.from_pretrained(
                    models_dir / "falcon-7b",
                    device_map="auto",
                    torch_dtype=torch.float16
                ),
                'tokenizer': AutoTokenizer.from_pretrained(models_dir / "falcon-7b")
            }
        }

    def _load_image_models(self):
        return {
            'captioning': {
                'processor': BlipProcessor.from_pretrained("Salesforce/blip-image-captioning-base"),
                'model': BlipForConditionalGeneration.from_pretrained(
                    "Salesforce/blip-image-captioning-base",
                    torch_dtype=torch.float16
                ).to(self.device)
            }
        }

    def generate_text(self, prompt: str, model: str = "bloom", **kwargs):
        config = self.models['text'].get(model)
        if not config:
            raise ValueError(f"Model {model} not supported")
        
        inputs = config['tokenizer'](prompt, return_tensors="pt").to(self.device)
        outputs = config['model'].generate(
            **inputs,
            max_new_tokens=kwargs.get('max_length', 200),
            do_sample=True,
            temperature=kwargs.get('temperature', 0.7)
        )
        return config['tokenizer'].decode(outputs[0], skip_special_tokens=True)