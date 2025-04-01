# backend/app/ai/feedback_processor.py
from collections import defaultdict
from datetime import datetime, timedelta

class FeedbackProcessor:
    def __init__(self):
        self.feedback_store = defaultdict(list)
        
    def process_feedback(self, user_id: str, feedback_data: dict):
        """معالجة التغذية الراجعة وتحديد أولويات التحسين"""
        feedback_data['timestamp'] = datetime.now()
        self.feedback_store[user_id].append(feedback_data)
        
        # تحليل الأنماط الشائعة
        common_issues = self._detect_common_issues()
        
        # تحديد أولويات التحسين
        improvement_areas = self._prioritize_improvements(common_issues)
        
        return improvement_areas
    
    def _detect_common_issues(self) -> dict:
        """كشف المشاكل المتكررة عبر المستخدمين"""
        issues = defaultdict(int)
        for user_feedbacks in self.feedback_store.values():
            for feedback in user_feedbacks:
                if 'issue' in feedback:
                    issues[feedback['issue']] += 1
                    
        return dict(issues)
    
    def _prioritize_improvements(self, issues: dict) -> list:
        """ترتيب أولويات التحسين"""
        recent_threshold = datetime.now() - timedelta(days=7)
        recent_issues = {
            k: v for k, v in issues.items() 
            if any(f['timestamp'] > recent_threshold 
                 for f in self.feedback_store.values())
        }
        
        return sorted(recent_issues.items(), 
                     key=lambda x: x[1], 
                     reverse=True)[:3]