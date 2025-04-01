# backend/app/api/endpoints/collaborative.py
from fastapi import APIRouter, Depends, HTTPException
from app.ai.collaborative_learning import CollaborativeLearner
from app.core.security import get_current_user
from datetime import timedelta

router = APIRouter()
collaborator = CollaborativeLearner()

@router.get("/similar-users")
async def get_similar_users(
    user_id: str = Depends(get_current_user),
    count: int = 5
):
    """الحصول على مستخدمين مشابهين"""
    try:
        return collaborator.get_similar_users(user_id, count)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/share-improvement")
async def share_improvement(
    improvement_data: dict,
    user_id: str = Depends(get_current_user)
):
    """مشاركة تحسين مع المستخدمين المشابهين"""
    try:
        return collaborator.share_improvements(user_id, improvement_data)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/shared-improvements")
async def get_shared_improvements(
    user_id: str = Depends(get_current_user)
):
    """الحصول على التحسينات المشتركة"""
    try:
        return collaborator.get_shared_improvements(user_id)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))