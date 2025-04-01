# backend/app/api/endpoints/learning.py
from fastapi import APIRouter, Depends
from app.ai.adaptive_learning import UserLearningProfile, AdaptiveClusterer
from app.core.security import get_current_user

router = APIRouter()
user_learner = UserLearningProfile()
clusterer = AdaptiveClusterer()

@router.post("/log_interaction")
async def log_interaction(
    interaction_data: dict,
    user_id: str = Depends(get_current_user)
):
    """تسجيل تفاعل المستخدم لتحسين التجربة"""
    user_learner.update_user_profile(user_id, interaction_data)
    return {"status": "success"}

@router.get("/get_recommendations")
async def get_recommendations(
    user_id: str = Depends(get_current_user)
):
    """الحصول على توصيات مخصصة للمستخدم"""
    profile = user_learner.profiles.find_one({"user_id": user_id})
    if not profile:
        return {"recommendations": []}
    
    cluster = clusterer.predict_cluster(profile)
    recommendations = {
        0: ["نموذج BLOOM", "تحويل النص إلى جدول"],
        1: ["تحليل الأكواد", "توليد SQL"],
        2: ["معالجة الصور", "تحويل PDF"],
        3: ["الترجمة الآلية", "تلخيص النصوص"],
        4: ["الذكاء الاصطناعي الإبداعي", "كتابة القصص"]
    }.get(cluster, [])
    
    return {"recommendations": recommendations}