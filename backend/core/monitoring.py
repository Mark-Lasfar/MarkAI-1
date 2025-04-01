# backend/core/monitoring.py
from prometheus_client import start_http_server, Counter, Gauge

class Monitor:
    def __init__(self):
        self.request_count = Counter(
            'api_requests_total',
            'Total API requests',
            ['endpoint', 'method']
        )
        self.response_time = Gauge(
            'api_response_time_seconds',
            'API response time in seconds',
            ['endpoint']
        )
        self.ai_usage = Counter(
            'ai_usage_total',
            'AI model usage statistics',
            ['model', 'modality']
        )

    def track_request(self, endpoint: str, method: str):
        self.request_count.labels(endpoint, method).inc()

    def track_response_time(self, endpoint: str, duration: float):
        self.response_time.labels(endpoint).set(duration)

    def track_ai_usage(self, model: str, modality: str):
        self.ai_usage.labels(model, modality).inc()

# Initialize global monitor
monitor = Monitor()
start_http_server(8001)  # Metrics endpoint