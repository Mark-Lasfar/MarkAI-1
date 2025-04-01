# backend/app/services/generation_service.py
from typing import Union
from ..core.ai.multimodal import MultimodalGenerator

class GenerationService:
    def __init__(self):
        self.generator = MultimodalGenerator()
    
    async def generate(
        self,
        content_type: str,
        prompt: str,
        **kwargs
    ) -> Union[str, bytes, dict]:
        if content_type == 'text':
            return await self._generate_text(prompt, **kwargs)
        elif content_type == 'image':
            return await self._generate_image(prompt, **kwargs)
        elif content_type == 'audio':
            return await self._generate_audio(prompt, **kwargs)
        elif content_type == 'video':
            return await self._generate_video(prompt, **kwargs)
        else:
            raise ValueError(f"Unsupported content type: {content_type}")

    async def _generate_text(self, prompt: str, model: str = 'bloom', **kwargs):
        return await self.generator.text_generate(prompt, model=model, **kwargs)
    
    async def _generate_image(self, prompt: str, style: str = 'realistic', **kwargs):
        return await self.generator.image_generate(prompt, style=style, **kwargs)
    
    async def _generate_audio(self, text: str, voice: str = 'male', **kwargs):
        return await self.generator.audio_generate(text, voice=voice, **kwargs)
    
    async def _generate_video(self, script: str, **kwargs):
        return await self.generator.video_generate(script, **kwargs)