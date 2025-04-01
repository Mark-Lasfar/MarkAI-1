# /backend/api/interactions.py
from fastapi import APIRouter
from ml.collaborative_learning import CollaborativeLearner
from db import users_db

router = APIRouter()
learner = CollaborativeLearner()

@router.post("/log_interaction")
async def log_interaction(user_id: str, interaction: dict):
    # 1. حفظ التفاعل في DB
    users_db.update_one(
        {"_id": user_id},
        {"$push": {"interactions": interaction}},
        upsert=True
    )
    
    # 2. تحديث التوصيات
    similar_users = learner.get_similar_users(user_id)
    recommendations = learner.generate_recommendations(user_id)
    
    return {
        "similar_users": similar_users,
        "recommendations": recommendations
    }