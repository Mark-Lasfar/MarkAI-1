# backend/ai_services/chat.py
from typing import List, Dict
from .memory import ConversationMemory

class AIChatService:
    def __init__(self):
        self.memory = ConversationMemory()
        self.personality = "professional"  # Can be customized

    async def generate_response(self, messages: List[Dict], context: Dict = None):
        """Generate context-aware responses"""
        # Augment with conversation history
        augmented = await self.memory.augment_prompt(messages)
        
        # Add personality traits
        prompt = self._apply_personality(augmented)
        
        # Generate response
        response = await self._call_llm(prompt)
        
        # Store interaction
        await self.memory.store_interaction(
            input=messages[-1]["content"],
            output=response
        )
        
        return response

    def _apply_personality(self, prompt: str) -> str:
        """Modify prompt based on selected personality"""
        personalities = {
            "professional": "Respond in a professional, business-appropriate manner.",
            "friendly": "Respond in a warm, friendly tone.",
            "technical": "Respond with detailed technical explanations."
        }
        return f"{personalities[self.personality]}\n\n{prompt}"

    async def _call_llm(self, prompt: str) -> str:
        """Call the appropriate LLM based on context"""
        # Implementation depends on your model setup
        return await ai_service.generate("text", prompt)