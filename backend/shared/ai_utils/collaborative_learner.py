# backend/app/ai/collaborative_learner.py
from collections import defaultdict
import numpy as np
from sklearn.cluster import DBSCAN

class CollaborativeLearner:
    def __init__(self):
        self.user_vectors = {}
        self.clusters = {}
        self.cluster_model = DBSCAN(eps=0.5, min_samples=2)
    
    def add_user_vector(self, user_id: str, vector: np.ndarray):
        """إضافة متجه مستخدم للتعلم التعاوني"""
        self.user_vectors[user_id] = vector
        self._update_clusters()
    
    def _update_clusters(self):
        """تحديث تجمعات المستخدمين"""
        if len(self.user_vectors) < 3:
            return
        
        vectors = np.array(list(self.user_vectors.values()))
        clusters = self.cluster_model.fit_predict(vectors)
        
        self.clusters = defaultdict(list)
        for user_id, cluster in zip(self.user_vectors.keys(), clusters):
            if cluster != -1:  # تجاهل القيم الشاذة
                self.clusters[cluster].append(user_id)
    
    def get_cluster_knowledge(self, user_id: str) -> Dict:
        """الحصول على المعرفة من المستخدمين المتشابهين"""
        user_cluster = None
        for cluster, users in self.clusters.items():
            if user_id in users:
                user_cluster = cluster
                break
        
        if user_cluster is None:
            return {}
        
        # جمع المعرفة من المستخدمين في نفس التجمع
        cluster_knowledge = {
            "common_phrases": [],
            "preferred_models": defaultdict(int),
            "frequent_tasks": defaultdict(int)
        }
        
        for member_id in self.clusters[user_cluster]:
            if member_id != user_id:
                # هنا يمكن جلب بيانات الأعضاء الآخرين من قاعدة البيانات
                pass
                
        return cluster_knowledge