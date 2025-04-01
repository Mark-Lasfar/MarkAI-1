# backend/app/core/performance.py
from fastapi import Request, Response
from fastapi.middleware.gzip import GZipMiddleware
import time
import zlib

class AdvancedGZipMiddleware(GZipMiddleware):
    async def dispatch(self, request: Request, call_next):
        if "gzip" not in request.headers.get("accept-encoding", ""):
            return await call_next(request)

        response = await call_next(request)

        if response.status_code >= 400 or len(response.body) < 500:
            return response

        response.body = zlib.compress(response.body, level=6)
        response.headers["Content-Encoding"] = "gzip"
        response.headers["Content-Length"] = str(len(response.body))
        return response

class CacheControlMiddleware:
    def __init__(self, max_age=3600):
        self.max_age = max_age

    async def __call__(self, request: Request, call_next):
        start_time = time.time()
        response = await call_next(request)
        process_time = time.time() - start_time
        response.headers["X-Process-Time"] = str(process_time)
        
        if request.method == "GET" and response.status_code < 400:
            response.headers["Cache-Control"] = f"public, max-age={self.max_age}"
        
        return response