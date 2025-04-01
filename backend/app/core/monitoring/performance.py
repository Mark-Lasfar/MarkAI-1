# backend/app/core/monitoring/performance.py
import time
from functools import wraps
from prometheus_client import Summary, Counter

REQUEST_TIME = Summary('request_processing_seconds', 'Time spent processing request')
REQUEST_COUNT = Counter('total_requests', 'Total API requests')

def monitor_performance(func):
    @wraps(func)
    async def wrapper(*args, **kwargs):
        start_time = time.time()
        REQUEST_COUNT.inc()
        
        try:
            result = await func(*args, **kwargs)
            return result
        finally:
            duration = time.time() - start_time
            REQUEST_TIME.observe(duration)
    return wrapper