# backend/media_tools/generator.py
from gtts import gTTS
from moviepy.editor import *
import numpy as np

class MediaGenerator:
    @staticmethod
    def text_to_audio(text, output_path, lang='ar'):
        tts = gTTS(text=text, lang=lang, slow=False)
        tts.save(output_path)

    @staticmethod
    def create_video_from_images(images, audio_path, output_path):
        clips = [ImageClip(img).set_duration(2) for img in images]
        video = concatenate_videoclips(clips)
        video = video.set_audio(AudioFileClip(audio_path))
        video.write_videofile(output_path, fps=24)