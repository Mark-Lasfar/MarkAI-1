# backend/app/services/subscription.py
from datetime import datetime, timedelta
from ..models import User, Subscription

class SubscriptionService:
    FREE_TIER_LIMITS = {
        'messages': 1000,
        'media_generations': 50,
        'file_processing': 100
    }

    @staticmethod
    async def create_free_subscription(user_id: str):
        # 1 year free subscription
        expiry = datetime.utcnow() + timedelta(days=365)
        return await Subscription.create(
            user_id=user_id,
            tier="free",
            limits=SubscriptionService.FREE_TIER_LIMITS,
            expires_at=expiry
        )

    @staticmethod
    async def check_usage(user_id: str, feature: str):
        user = await User.get(user_id)
        if user.subscription.tier == "free":
            return user.usage[feature] < user.subscription.limits[feature]
        return True