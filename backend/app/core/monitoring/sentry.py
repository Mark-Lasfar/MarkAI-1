# backend/app/core/monitoring/sentry.py
import sentry_sdk
from ..config import settings

def configure_monitoring():
    sentry_sdk.init(
        dsn=settings.SENTRY_DSN,
        traces_sample_rate=1.0,
        profiles_sample_rate=1.0,
    )