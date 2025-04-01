# backend/app/ai/context_memory.py
from datetime import datetime, timedelta
from typing import Dict, List
import hashlib

class ContextMemory:
    def __init__(self, ttl_hours: int = 24):
        self.memories = {}
        self.ttl = timedelta(hours=ttl_hours)
    
    def _generate_memory_key(self, user_id: str, context: str) -> str:
        """إنشاء مفتاح ذاكرة فريد"""
        return hashlib.md5(f"{user_id}_{context}".encode()).hexdigest()
    
    def store_context(self, user_id: str, context: str, data: Dict):
        """تخزين المعلومات السياقية"""
        key = self._generate_memory_key(user_id, context)
        self.memories[key] = {
            "data": data,
            "timestamp": datetime.now()
        }
        self._cleanup()
    
    def retrieve_context(self, user_id: str, context: str) -> Dict:
        """استرجاع المعلومات السياقية"""
        key = self._generate_memory_key(user_id, context)
        memory = self.memories.get(key, None)
        
        if memory and (datetime.now() - memory["timestamp"]) < self.ttl:
            return memory["data"]
        return {}
    
    def _cleanup(self):
        """تنظيف الذكريات المنتهية الصلاحية"""
        now = datetime.now()
        expired_keys = [
            k for k, v in self.memories.items()
            if (now - v["timestamp"]) > self.ttl
        ]
        
        for key in expired_keys:
            del self.memories[key]