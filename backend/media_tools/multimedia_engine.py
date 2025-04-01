# backend/media_tools/multimedia_engine.py
import cv2
import numpy as np
from pydub import AudioSegment

class VideoEditor:
    @staticmethod
    def add_subtitles(video_path, text, output_path):
        cap = cv2.VideoCapture(video_path)
        fps = cap.get(cv2.CAP_PROP_FPS)
        width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
        height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
        
        fourcc = cv2.VideoWriter_fourcc(*'mp4v')
        out = cv2.VideoWriter(output_path, fourcc, fps, (width, height))
        
        while cap.isOpened():
            ret, frame = cap.read()
            if not ret:
                break
                
            cv2.putText(frame, text, (50, height-50), 
                        cv2.FONT_HERSHEY_SIMPLEX, 1, (255,255,255), 2)
            out.write(frame)
        
        cap.release()
        out.release()

class AudioProcessor:
    @staticmethod
    def merge_audio_files(file_list, output_path):
        combined = AudioSegment.empty()
        for file in file_list:
            sound = AudioSegment.from_file(file)
            combined += sound
        combined.export(output_path, format="mp3")