# backend/ai/multimodal.py
from transformers import pipeline
import speech_recognition as sr

class AIModel:
    def __init__(self):
        self.text_gen = pipeline("text-generation", model="bloom-7b1")
        self.speech_recognizer = sr.Recognizer()

    def generate_code(self, prompt):
        response = self.text_gen(
            f"// Generate {prompt} code\n```python\n",
            max_length=200,
            temperature=0.7
        )
        return response[0]['generated_text']

    def speech_to_text(self, audio_path):
        with sr.AudioFile(audio_path) as source:
            audio = self.speech_recognizer.record(source)
            return self.speech_recognizer.recognize_google(audio, language="ar-AR")