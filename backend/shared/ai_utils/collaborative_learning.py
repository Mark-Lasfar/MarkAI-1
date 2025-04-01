# backend/app/ai/collaborative_learning.py
from datetime import datetime, timedelta
from pymongo import MongoClient
import numpy as np
from sklearn.cluster import KMeans
from typing import Dict, List, Optional
import hashlib

class CollaborativeLearner:
    def __init__(self, db_uri: str = "mongodb://localhost:27017/"):
        self.client = MongoClient(db_uri)
        self.db = self.client["ai_learning"]
        self.users = self.db["user_profiles"]
        self.clusters = self.db["user_clusters"]
        self.model = KMeans(n_clusters=5)
        self.cluster_centers = {}
        
    def _get_user_vector(self, user_data: Dict) -> np.ndarray:
        """تحويل بيانات المستخدم لمتجهات عددية"""
        features = [
            len(user_data.get("interactions", [])),
            user_data.get("preferences", {}).get("model_usage", {}).get("bloom", 0),
            user_data.get("preferences", {}).get("model_usage", {}).get("falcon", 0),
            user_data.get("preferences", {}).get("task_types", {}).get("code", 0),
            user_data.get("preferences", {}).get("task_types", {}).get("text", 0),
        ]
        return np.array(features)
    
    def update_clusters(self):
        """تحديث تجميعات المستخدمين"""
        all_users = list(self.users.find({}))
        
        if len(all_users) < 10:
            return  # تحتاج عدد كافٍ من المستخدمين
            
        # تحضير البيانات للتدريب
        user_vectors = np.array([self._get_user_vector(u) for u in all_users])
        user_ids = [str(u["_id"]) for u in all_users]
        
        # تدريب نموذج التجميع
        self.model.fit(user_vectors)
        
        # حفظ التجميعات الجديدة
        clusters = {}
        for user_id, cluster_id in zip(user_ids, self.model.labels_):
            clusters.setdefault(str(cluster_id), []).append(user_id)
        
        # تحديث قاعدة البيانات
        self.clusters.delete_many({})
        for cluster_id, members in clusters.items():
            self.clusters.insert_one({
                "cluster_id": cluster_id,
                "members": members,
                "updated_at": datetime.now()
            })
        
        # حفظ مراكز التجميع
        self.cluster_centers = {
            str(i): center for i, center in enumerate(self.model.cluster_centers_)
        }
    
    def get_similar_users(self, user_id: str, max_users: int = 5) -> List[Dict]:
        """الحصول على مستخدمين مشابهين"""
        user_data = self.users.find_one({"_id": user_id})
        if not user_data:
            return []
            
        user_cluster = self.clusters.find_one({"members": user_id})
        if not user_cluster:
            return []
            
        similar_users = []
        for member_id in user_cluster["members"]:
            if member_id != user_id:
                member_data = self.users.find_one({"_id": member_id})
                if member_data:
                    similarity = self._calculate_similarity(
                        self._get_user_vector(user_data),
                        self._get_user_vector(member_data)
                    )
                    similar_users.append({
                        "user_id": member_id,
                        "similarity": similarity,
                        "preferences": member_data.get("preferences", {})
                    })
        
        # ترتيب حسب التشابه
        similar_users.sort(key=lambda x: x["similarity"], reverse=True)
        return similar_users[:max_users]
    
    def _calculate_similarity(self, vec1: np.ndarray, vec2: np.ndarray) -> float:
        """حساب درجة التشابه بين متجهين"""
        return np.dot(vec1, vec2) / (np.linalg.norm(vec1) * np.linalg.norm(vec2))
    
    def share_improvements(self, user_id: str, improvement_data: Dict):
        """مشاركة التحسينات مع المستخدمين المشابهين"""
        similar_users = self.get_similar_users(user_id)
        improvement_id = hashlib.md5(
            str(improvement_data).encode()
        ).hexdigest()
        
        for user in similar_users:
            self.users.update_one(
                {"_id": user["user_id"]},
                {"$push": {
                    "shared_improvements": {
                        "id": improvement_id,
                        "data": improvement_data,
                        "shared_by": user_id,
                        "timestamp": datetime.now()
                    }
                }}
            )
        
        return {"status": "shared", "count": len(similar_users)}
    
    def get_shared_improvements(self, user_id: str) -> List[Dict]:
        """الحصول على التحسينات المشتركة من المستخدمين المشابهين"""
        user_data = self.users.find_one({"_id": user_id})
        if not user_data:
            return []
            
        return user_data.get("shared_improvements", [])