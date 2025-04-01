# backend/app/services/media_generation.py
import os
from pathlib import Path
from moviepy.editor import *
from gtts import gTTS
from .ai_service import ai_service
from fastapi import UploadFile

class MediaGenerator:
    @staticmethod
    async def generate_video_from_text(text: str, output_path: str = "generated_video.mp4"):
        # Generate audio
        tts = gTTS(text=text, lang='en')
        audio_path = "temp_audio.mp3"
        tts.save(audio_path)
        
        # Generate images (using AI)
        image_paths = await ai_service.generate_images(text)
        
        # Create video
        clips = [ImageClip(img).set_duration(3) for img in image_paths]
        video = concatenate_videoclips(clips)
        video = video.set_audio(AudioFileClip(audio_path))
        video.write_videofile(output_path, fps=24)
        
        # Cleanup
        os.remove(audio_path)
        for img in image_paths:
            os.remove(img)
            
        return output_path

    @staticmethod
    async def process_uploaded_file(file: UploadFile):
        file_path = f"uploads/{file.filename}"
        with open(file_path, "wb") as buffer:
            buffer.write(await file.read())
        
        # Process based on file type
        if file.filename.endswith(('.mp3', '.wav')):
            return await ai_service.process_audio(file_path)
        elif file.filename.endswith(('.jpg', '.png', '.jpeg')):
            return await ai_service.process_image(file_path)
        else:
            return await ai_service.process_text(file_path)