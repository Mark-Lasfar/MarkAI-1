# backend/app/core/memory/context_manager.py
from typing import Dict, List
from datetime import datetime, timedelta
from ..database import SessionLocal

class ContextManager:
    def __init__(self):
        self.conversation_memory: Dict[str, List[Dict]] = {}
        self.user_preferences: Dict[str, Dict] = {}
        
    async def store_conversation(self, user_id: str, message: str, response: str):
        if user_id not in self.conversation_memory:
            self.conversation_memory[user_id] = []
            
        self.conversation_memory[user_id].append({
            'timestamp': datetime.utcnow(),
            'message': message,
            'response': response
        })
        
        # Auto-prune old messages
        self._cleanup_old_messages(user_id)

    async def get_context(self, user_id: str, lookback_hours: int = 24) -> List[Dict]:
        cutoff = datetime.utcnow() - timedelta(hours=lookback_hours)
        return [
            msg for msg in self.conversation_memory.get(user_id, [])
            if msg['timestamp'] > cutoff
        ]

    def _cleanup_old_messages(self, user_id: str, max_age_days: int = 30):
        cutoff = datetime.utcnow() - timedelta(days=max_age_days)
        if user_id in self.conversation_memory:
            self.conversation_memory[user_id] = [
                msg for msg in self.conversation_memory[user_id]
                if msg['timestamp'] > cutoff
            ]