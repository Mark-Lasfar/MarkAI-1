# backend/subscription/service.py
from datetime import datetime, timedelta
from .models import Subscription

class SubscriptionService:
    FREE_TIER = {
        "name": "free",
        "limits": {
            "daily_requests": 100,
            "media_generations": 20,
            "file_processing": 50
        },
        "features": [
            "basic_ai",
            "community_support",
            "5_free_messages"
        ]
    }

    async def create_free_subscription(self, user_id: str):
        """Initialize free subscription for new users"""
        return await Subscription.create(
            user_id=user_id,
            tier=self.FREE_TIER["name"],
            limits=self.FREE_TIER["limits"],
            features=self.FREE_TIER["features"],
            expires_at=datetime.utcnow() + timedelta(days=365)  # 1 year free
        )

    async def check_limit(self, user_id: str, feature: str) -> bool:
        """Verify user hasn't exceeded usage limits"""
        subscription = await Subscription.get(user_id=user_id)
        usage = await self._get_usage(user_id, feature)
        return usage < subscription.limits.get(feature, 0)

    async def _get_usage(self, user_id: str, feature: str) -> int:
        """Get current usage for a specific feature"""
        today = datetime.utcnow().date()
        return await UsageLog.filter(
            user_id=user_id,
            feature=feature,
            date=today
        ).count()