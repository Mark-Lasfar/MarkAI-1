# backend/app/monitoring/monitor.py
from prometheus_client import start_http_server, Summary, Counter
import time

# مقاييس الأداء
REQUEST_TIME = Summary('request_processing_seconds', 'Time spent processing request')
REQUEST_COUNT = Counter('total_requests', 'Total API requests count')

class PerformanceMonitor:
    def __init__(self, port=8001):
        self.port = port
        
    def start(self):
        start_http_server(self.port)
        
    @REQUEST_TIME.time()
    def track_request(self):
        REQUEST_COUNT.inc()
        
    def track_error(self, error_type):
        ERROR_COUNTER.labels(error_type).inc()