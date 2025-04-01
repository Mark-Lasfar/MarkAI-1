# backend/app/ai/feedback_analyzer.py
from transformers import pipeline
from typing import List, Dict
import numpy as np

class FeedbackAnalyzer:
    def __init__(self):
        self.sentiment = pipeline("text-classification", model="arabert-sentiment")
        self.keyword_extractor = pipeline("token-classification", model="bert-keyword-extractor")
    
    def analyze_feedback(self, text: str) -> Dict:
        """تحليل نصي للتغذية الراجعة باستخدام الذكاء الاصطناعي"""
        sentiment = self.sentiment(text)
        keywords = self.keyword_extractor(text)
        
        return {
            "sentiment": sentiment[0]['label'],
            "confidence": sentiment[0]['score'],
            "keywords": [kw['word'] for kw in keywords],
            "improvement_areas": self._detect_improvement_areas(text)
        }
    
    def _detect_improvement_areas(self, text: str) -> List[str]:
        """كشف مجالات التحسين من التعليقات"""
        improvement_keywords = {
            "ar": ["بطيء", "خطأ", "غير دقيق", "مشكلة", "لا يعمل"],
            "en": ["slow", "wrong", "inaccurate", "issue", "not working"]
        }
        
        detected_areas = []
        for lang, keywords in improvement_keywords.items():
            if any(keyword in text for keyword in keywords):
                detected_areas.extend(keywords)
        
        return list(set(detected_areas))