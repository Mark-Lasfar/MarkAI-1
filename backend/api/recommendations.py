# /backend/api/recommendations.py
@router.get("/get_recommendations/{user_id}")
async def get_recommendations(user_id: str):
    return learner.generate_recommendations(user_id)