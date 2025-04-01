# backend/app/ai/adaptive_learning.py
from datetime import datetime
import numpy as np
from sklearn.cluster import KMeans
from pymongo import MongoClient
from bson import Binary
import pickle

class AdaptiveLearner:
    def __init__(self, db_uri="mongodb://localhost:27017/"):
        self.client = MongoClient(db_uri)
        self.db = self.client["user_profiles"]
        self.profiles = self.db["learning_profiles"]
        self.model = KMeans(n_clusters=5)
        self.is_trained = False

    def _serialize_model(self, model):
        return Binary(pickle.dumps(model))

    def _deserialize_model(self, data):
        return pickle.loads(data)

    def update_user_profile(self, user_id: str, interaction_data: dict):
        """تحديث ملف المستخدم بناءً على تفاعلاته الأخيرة"""
        profile = self.profiles.find_one({"user_id": user_id}) or {
            "user_id": user_id,
            "created_at": datetime.now(),
            "interactions": [],
            "preferences": {},
            "cluster": -1
        }

        # تحديث سجل التفاعلات
        profile["interactions"].append({
            **interaction_data,
            "timestamp": datetime.now()
        })

        # تحديث التفضيلات التلقائية
        self._update_preferences(profile, interaction_data)

        # حفظ التحديثات
        self.profiles.update_one(
            {"user_id": user_id},
            {"$set": profile},
            upsert=True
        )

        # إعادة تدريب النموذج
        self._retrain_model()

    def _update_preferences(self, profile, interaction):
        """تحديث تفضيلات المستخدم تلقائياً"""
        if "model_used" in interaction:
            profile["preferences"].setdefault("fav_models", {})
            profile["preferences"]["fav_models"][interaction["model_used"]] = \
                profile["preferences"]["fav_models"].get(interaction["model_used"], 0) + 1

        if "task_type" in interaction:
            profile["preferences"].setdefault("common_tasks", {})
            profile["preferences"]["common_tasks"][interaction["task_type"]] = \
                profile["preferences"]["common_tasks"].get(interaction["task_type"], 0) + 1

    def _retrain_model(self):
        """إعادة تدريب نموذج التجميع"""
        user_profiles = list(self.profiles.find())
        if len(user_profiles) < 10:
            return  # تحتاج لعدد كافٍ من المستخدمين

        features = self._extract_features(user_profiles)
        self.model.fit(features)
        self.is_trained = True

    def predict_cluster(self, user_profile):
        """توقع المجموعة المناسبة للمستخدم"""
        if not self.is_trained:
            return -1

        features = self._extract_features([user_profile])
        return self.model.predict(features)[0]

    def _extract_features(self, profiles):
        """استخراج السمات المهمة من تفاعلات المستخدمين"""
        features = []
        for profile in profiles:
            # عدد التفاعلات
            interact_count = len(profile.get("interactions", []))

            # معدل استخدام النماذج
            fav_models = profile.get("preferences", {}).get("fav_models", {})
            model_var = np.var(list(fav_models.values())) if fav_models else 0

            features.append([interact_count, model_var])

        return np.array(features)

    def get_recommendations(self, user_id):
        """الحصول على توصيات مخصصة"""
        user_profile = self.profiles.find_one({"user_id": user_id})
        if user_profile is None:
            return []

        cluster = self.predict_cluster(user_profile)
        return {
            0: ["نموذج BLOOM", "تحويل النص إلى جدول"],
            1: ["تحليل الأكواد", "توليد SQL"],
            2: ["معالجة الصور", "تحويل PDF"],
            3: ["نموذج NLP", "تحليل النص"],
            4: ["نموذج CV", "تحليل الصور"]
        }.get(cluster, [])

class EnhancedUserLearningProfile(AdaptiveLearner):
    def __init__(self):
        super().__init__()
        from .sentiment_analyzer import SentimentAnalyzer
        self.sentiment_analyzer = SentimentAnalyzer()

    def update_user_profile(self, user_id: str, interaction_data: dict):
        """تحديث الملف مع تحليل المشاعر"""
        sentiment = self.sentiment_analyzer.analyze_interaction