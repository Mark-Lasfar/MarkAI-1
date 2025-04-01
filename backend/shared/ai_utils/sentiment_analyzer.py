# backend/app/ai/sentiment_analyzer.py
from transformers import pipeline
from typing import Dict, Any
import numpy as np

class SentimentAnalyzer:
    def __init__(self):
        self.model = pipeline("text-classification", 
                            model="finiteautomata/bertweet-ar-sentiment")
        
    def analyze_interaction(self, interaction: Dict[str, Any]) -> Dict[str, float]:
        """تحليل مشاعر المستخدم من التفاعلات"""
        text = interaction.get('user_input', '') + " " + interaction.get('user_feedback', '')
        
        if not text.strip():
            return {'neutral': 1.0}
            
        result = self.model(text)
        
        # تحويل النتائج لصيغة موحدة
        sentiment_scores = {
            'positive': 0.0,
            'negative': 0.0,
            'neutral': 0.0
        }
        
        for res in result:
            label = res['label'].lower()
            score = res['score']
            sentiment_scores[label] = score
            
        return sentiment_scores