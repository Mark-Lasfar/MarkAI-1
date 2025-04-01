# backend/analytics/service.py
from datetime import datetime
from typing import Dict
from .models import UserInteraction, Reward

class AnalyticsService:
    REWARD_RATE = 0.15  # 15% of "profits" (engagement metrics)
    
    async def track_interaction(self, user_id: str, action: str, value: float = 1.0):
        """Record user activity and issue rewards"""
        interaction = UserInteraction(
            user_id=user_id,
            action=action,
            value=value,
            timestamp=datetime.utcnow()
        )
        await interaction.save()
        
        # Check reward eligibility
        if await self._check_engagement(user_id):
            reward = value * self.REWARD_RATE
            await self._issue_reward(user_id, reward)

    async def _check_engagement(self, user_id: str) -> bool:
        """Check if user meets reward criteria"""
        last_week = datetime.utcnow() - timedelta(days=7)
        interactions = await UserInteraction.filter(
            user_id=user_id,
            timestamp__gte=last_week
        ).count()
        return interactions >= 10  # Minimum 10 interactions/week

    async def _issue_reward(self, user_id: str, amount: float):
        """Distribute rewards to user"""
        reward = Reward(
            user_id=user_id,
            amount=amount,
            reason="engagement_reward",
            issued_at=datetime.utcnow()
        )
        await reward.save()