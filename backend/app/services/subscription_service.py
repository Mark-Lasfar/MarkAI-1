# backend/app/services/subscription_service.py
from datetime import datetime, timedelta
from ..models import User, Transaction

class SubscriptionService:
    FREE_TIER_LIMITS = {
        'daily_messages': 50,
        'monthly_media': 30,
        'storage_gb': 5
    }

    REWARD_RATE = 0.15  # 15% reward
    
    async def check_usage(self, user: User, feature: str) -> bool:
        if user.subscription.tier == 'premium':
            return True
            
        usage = await self.get_usage(user.id, feature)
        limit = self.FREE_TIER_LIMITS.get(feature, 0)
        return usage < limit
    
    async def issue_reward(self, user_id: str, activity_value: float):
        reward = activity_value * self.REWARD_RATE
        await Transaction.create(
            user_id=user_id,
            amount=reward,
            type='reward',
            description='Activity reward'
        )