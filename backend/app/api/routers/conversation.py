# backend/app/api/routers/conversation.py
from fastapi import APIRouter, Depends
from ..core.auth import get_current_user
from ..services.conversation import ConversationService

router = APIRouter(prefix="/conversations", tags=["Conversations"])

@router.get("/")
async def get_conversations(user=Depends(get_current_user)):
    return await ConversationService.get_user_conversations(user.id)

@router.get("/{conversation_id}")
async def get_messages(conversation_id: str, user=Depends(get_current_user)):
    return await ConversationService.get_messages(conversation_id, user.id)