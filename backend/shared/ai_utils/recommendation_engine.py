# backend/app/ai/recommendation_engine.py
from typing import List, Dict
import numpy as np
from sklearn.neighbors import NearestNeighbors
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

class RecommendationEngine:
    def __init__(self):
        self.content_model = NearestNeighbors(n_neighbors=5)
        self.collab_model = NearestNeighbors(n_neighbors=5)
        self.vectorizer = TfidfVectorizer(ngram_range=(1, 2))
        self.user_profiles = {}
        self.feature_weights = {
            'content': 0.6,
            'collaborative': 0.4
        }
    
    def train_models(self, content_features, collab_features):
        """تدريب نماذج التوصية"""
        self.content_model.fit(content_features)
        self.collab_model.fit(collab_features)
    
    def update_user_profile(self, user_id: str, interaction: Dict):
        """تحديث ملف المستخدم مع التفاعلات الجديدة"""
        if user_id not in self.user_profiles:
            self.user_profiles[user_id] = {
                "interactions": [],
                "feature_vector": None
            }
        
        self.user_profiles[user_id]["interactions"].append(interaction)
        self._update_feature_vector(user_id)
    
    def _update_feature_vector(self, user_id: str):
        """تحديث متجهات السمات للمستخدم"""
        interactions = self.user_profiles[user_id]["interactions"]
        texts = [f"{i['input']} {i['output']}" for i in interactions[-50:]]  # آخر 50 تفاعل
        
        if len(texts) > 5:  # حد أدنى للتفاعلات
            tfidf_matrix = self.vectorizer.fit_transform(texts)
            self.user_profiles[user_id]["feature_vector"] = np.mean(tfidf_matrix, axis=0)
    
    def get_similar_users(self, user_id: str, n: int = 5) -> List[str]:
        """إيجاد مستخدمين متشابهين"""
        if user_id not in self.user_profiles or not self.user_profiles[user_id]["feature_vector"]:
            return []
        
        user_vec = self.user_profiles[user_id]["feature_vector"]
        similarities = []
        
        for other_id, profile in self.user_profiles.items():
            if other_id != user_id and profile["feature_vector"] is not None:
                sim = cosine_similarity(user_vec, profile["feature_vector"])[0][0]
                similarities.append((other_id, sim))
        
        similarities.sort(key=lambda x: x[1], reverse=True)
        return [user_id for user_id, _ in similarities[:n]]
    
    def generate_recommendations(self, user_profile: Dict) -> List[str]:
        """توليد توصيات هجينة"""
        # تحضير بيانات المستخدم
        content_features = self._extract_content_features(user_profile)
        collab_features = self._extract_collab_features(user_profile)
        
        # البحث عن الأقرب في كل نموذج
        content_recs = self.content_model.kneighbors([content_features], return_distance=False)
        collab_recs = self.collab_model.kneighbors([collab_features], return_distance=False)
        
        # دمج النتائج مع الأوزان
        combined_recs = self._combine_recommendations(content_recs, collab_recs)
        
        return combined_recs
    
    def _extract_content_features(self, profile: Dict) -> np.array:
        """استخراج سمات المحتوى"""
        return np.array([
            len(profile.get('interactions', [])),
            profile.get('preferences', {}).get('model_usage', {}).get('bloom', 0),
            profile.get('preferences', {}).get('task_types', {}).get('coding', 0)
        ])
    
    def _combine_recommendations(self, content_recs, collab_recs) -> List[str]:
        """دمج التوصيات بذكاء"""
        # تطبيق خوارزمية Borda Count للدمج
        recommendations = []
        
        for i, rec in enumerate(content_recs[0]):
            recommendations.append({
                'item': rec,
                'score': (len(content_recs[0]) - i) * self.feature_weights['content']
            })
            
        for i, rec in enumerate(collab_recs[0]):
            found = next((r for r in recommendations if r['item'] == rec), None)
            if found:
                found['score'] += (len(collab_recs[0]) - i) * self.feature_weights['collaborative']
            else:
                recommendations