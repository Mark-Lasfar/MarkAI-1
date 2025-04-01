# backend/app/services/conversation_engine.py
from datetime import datetime
from typing import List, Dict
from ..core.ai.multimodal_engine import MultimodalAI
from ..models.conversation import Conversation

class ConversationEngine:
    def __init__(self, ai_engine: MultimodalAI):
        self.ai = ai_engine
        self.active_conversations: Dict[str, Conversation] = {}

    async def process_message(self, user_id: str, message: str, context: List[Dict] = None):
        conversation = self.active_conversations.get(user_id, Conversation(user_id))
        
        # بناء السياق من المحادثة السابقة
        context_prompt = self._build_context_prompt(conversation.history, message)
        
        # توليد الرد باستخدام الذكاء الاصطناعي
        response = await self.ai.generate_text(
            model="bloom",
            prompt=context_prompt,
            temperature=0.7
        )
        
        # تحديث تاريخ المحادثة
        conversation.add_message(message, response)
        self.active_conversations[user_id] = conversation
        
        return {
            "response": response,
            "conversation_id": conversation.id,
            "timestamp": datetime.utcnow().isoformat()
        }

    def _build_context_prompt(self, history: List[Dict], new_message: str) -> str:
        prompt = "سياق المحادثة السابقة:\n"
        for msg in history[-5:]:  # أخذ آخر 5 رسائل كسياق
            role = "المستخدم" if msg['is_user'] else "المساعد"
            prompt += f"{role}: {msg['content']}\n"
        
        prompt += f"\nرسالة جديدة من المستخدم: {new_message}\nالرد:"
        return prompt