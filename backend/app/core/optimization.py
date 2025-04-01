# backend/app/core/optimization.py
import asyncio
from concurrent.futures import ThreadPoolExecutor
from functools import partial, wraps
from typing import Callable, Any

def run_in_threadpool(func: Callable) -> Callable:
    @wraps(func)
    async def wrapper(*args: Any, **kwargs: Any) -> Any:
        loop = asyncio.get_event_loop()
        return await loop.run_in_executor(
            None, partial(func, *args, **kwargs)
        )
    return wrapper

class AIProcessingQueue:
    def __init__(self, max_workers=4):
        self.executor = ThreadPoolExecutor(max_workers=max_workers)
        self.loop = asyncio.get_event_loop()

    async def process(self, func, *args):
        return await self.loop.run_in_executor(
            self.executor, func, *args
        )