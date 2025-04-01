# backend/app/ai/auto_evaluator.py
from transformers import pipeline
from typing import Dict

class AutoEvaluator:
    def __init__(self):
        self.quality_scorer = pipeline(
            "text-classification", 
            model="distilbert-base-uncased-finetuned-sst-2-english"
        )
        self.fact_checker = pipeline(
            "text2text-generation", 
            model="google/t5-small-finetuned-wikiSQL"
        )
    
    def evaluate_response(self, input_text: str, output_text: str) -> Dict:
        """تقييم جودة الرد تلقائياً"""
        quality = self.quality_scorer(output_text)
        fact_check = self.fact_checker(
            f"verify the fact: {output_text} based on: {input_text}"
        )
        
        return {
            "quality_score": quality[0]['score'],
            "quality_label": quality[0]['label'],
            "fact_check": fact_check[0]['generated_text'],
            "needs_human_review": self._needs_review(output_text)
        }
    
    def _needs_review(self, text: str) -> bool:
        """تحديد إذا كان الرد يحتاج مراجعة بشرية"""
        red_flags = [
            "لا أعرف", "غير متأكد", "ليس لدي معلومات", 
            "I don't know", "unsure", "no information"
        ]
        
        return any(flag in text for flag in red_flags)