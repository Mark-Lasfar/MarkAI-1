# backend/ai_services/multimodal_service.py
import torch
from transformers import (
    pipeline,
    BlipProcessor, 
    BlipForConditionalGeneration,
    SpeechT5Processor,
    SpeechT5ForTextToSpeech,
    AutoModelForCausalLM,
    AutoTokenizer
)
from typing import Dict, Any

class MultimodalAIService:
    def __init__(self):
        """Initialize the multimodal AI service with all models loaded"""
        self.device = "cuda" if torch.cuda.is_available() else "cpu"
        self.models = self._load_models()
    
    def _load_models(self) -> Dict[str, Dict[str, Any]]:
        """Load all AI models into memory
        
        Returns:
            Dictionary containing all loaded models organized by modality
        """
        return {
            'text': {
                'bloom': pipeline("text-generation", model="bigscience/bloom-7b1", device=self.device),
                'falcon': pipeline("text-generation", model="tiiuae/falcon-7b", device=self.device),
                'gpt-j': pipeline("text-generation", model="EleutherAI/gpt-j-6B", device=self.device)
            },
            'image': {
                'captioning': pipeline("image-to-text", model="Salesforce/blip-image-captioning-base", device=self.device),
                'generation': pipeline("text-to-image", model="runwayml/stable-diffusion-v1-5", device=self.device)
            },
            'audio': {
                'tts': pipeline("text-to-speech", model="microsoft/speecht5_tts", device=self.device),
                'transcription': pipeline("automatic-speech-recognition", model="openai/whisper-medium", device=self.device)
            },
            'code': {
                'generation': pipeline("text-generation", model="Salesforce/codegen-6B-mono", device=self.device)
            }
        }

    async def generate(self, modality: str, prompt: str, **kwargs) -> Any:
        """Unified generation endpoint for all modalities
        
        Args:
            modality: Type of content to generate (text, image, audio, code)
            prompt: Input prompt for generation
            **kwargs: Additional model-specific parameters
            
        Returns:
            Generated content based on the modality
        """
        model_name = kwargs.get('model')
        if modality not in self.models:
            raise ValueError(f"Unsupported modality: {modality}")
            
        model = self.models[modality].get(model_name)
        if not model:
            raise ValueError(f"Unsupported model '{model_name}' for {modality}")
        
        result = model(prompt, **kwargs)
        return self._postprocess(result, modality)

    def _postprocess(self, result: Any, modality: str) -> Any:
        """Format output based on modality
        
        Args:
            result: Raw model output
            modality: Type of content
            
        Returns:
            Processed output in appropriate format
        """
        processors = {
            'text': lambda x: x[0]['generated_text'],
            'image': lambda x: x.images[0],
            'audio': lambda x: x['audio'],
            'code': lambda x: x[0]['generated_text']
        }
        return processors.get(modality, lambda x: x)(result)