# backend/media/service.py
import os
from pathlib import Path
from typing import Optional, List
from fastapi import UploadFile
from moviepy.editor import *
from .ai_service import ai_service

class MediaService:
    SUPPORTED_TYPES = {
        'image': ['.jpg', '.jpeg', '.png', '.webp'],
        'audio': ['.mp3', '.wav', '.ogg'],
        'video': ['.mp4', '.mov', '.avi']
    }

    def __init__(self):
        # Create necessary directories
        Path("tmp").mkdir(exist_ok=True)
        Path("output").mkdir(exist_ok=True)

    def _get_file_type(self, filename: str) -> Optional[str]:
        """Determine file type based on extension"""
        ext = Path(filename).suffix.lower()
        for file_type, extensions in self.SUPPORTED_TYPES.items():
            if ext in extensions:
                return file_type
        return None

    async def _save_file(self, file: UploadFile, path: str) -> None:
        """Save uploaded file to temporary location"""
        with open(path, "wb") as buffer:
            content = await file.read()
            buffer.write(content)

    def _save_audio(self, audio_data: bytes, path: str) -> None:
        """Save generated audio to file"""
        with open(path, "wb") as audio_file:
            audio_file.write(audio_data)

    async def process_upload(self, file: UploadFile):
        """Process any uploaded media file
        
        Args:
            file: Uploaded file object
            
        Returns:
            Processed result based on file type
            
        Raises:
            ValueError: If file type is not supported
        """
        file_type = self._get_file_type(file.filename)
        if not file_type:
            raise ValueError("Unsupported file type")
            
        temp_path = f"tmp/{file.filename}"
        
        try:
            # Save temporarily
            await self._save_file(file, temp_path)
            
            # Process based on type
            processor = getattr(self, f"_process_{file_type}")
            result = await processor(temp_path)
            return result
        finally:
            # Cleanup
            if os.path.exists(temp_path):
                os.remove(temp_path)

    async def _process_image(self, path: str) -> str:
        """Generate description for an image"""
        return await ai_service.generate(
            modality="image",
            prompt=f"Describe this image in detail: {path}",
            model="captioning"
        )

    async def _process_audio(self, path: str) -> str:
        """Transcribe audio file to text"""
        return await ai_service.generate(
            modality="audio",
            prompt=path,
            model="transcription"
        )

    async def _generate_scenes(self, script: str) -> List[VideoClip]:
        """Generate video scenes from script text"""
        # This would be more sophisticated in production
        scenes = []
        # Placeholder - in reality you would generate actual scenes
        scenes.append(ColorClip((1920, 1080), color=(0, 0, 0), duration=5))
        return scenes

    async def generate_video(self, script: str) -> str:
        """Generate complete video from text script
        
        Args:
            script: Text script to convert to video
            
        Returns:
            Path to generated video file
        """
        try:
            # Step 1: Generate audio
            audio_path = "tmp/audio.mp3"
            tts_result = await ai_service.generate(
                modality="audio",
                prompt=script,
                model="tts"
            )
            self._save_audio(tts_result, audio_path)
            
            # Step 2: Generate scenes
            scenes = await self._generate_scenes(script)
            
            # Step 3: Compile video
            video = concatenate_videoclips(scenes)
            video = video.set_audio(AudioFileClip(audio_path))
            output_path = "output/generated_video.mp4"
            video.write_videofile(output_path, fps=24, codec='libx264')
            
            return output_path
        finally:
            # Cleanup temporary files
            if os.path.exists(audio_path):
                os.remove(audio_path)