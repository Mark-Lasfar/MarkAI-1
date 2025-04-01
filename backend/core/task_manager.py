# backend/core/task_manager.py
from concurrent.futures import ThreadPoolExecutor
from enum import Enum
import uuid
import time

class TaskStatus(Enum):
    PENDING = 1
    PROCESSING = 2
    COMPLETED = 3
    FAILED = 4

class UnifiedTaskManager:
    def __init__(self):
        self.executor = ThreadPoolExecutor(max_workers=4)
        self.tasks = {}
        
    def submit_task(self, task_func, *args, **kwargs):
        task_id = str(uuid.uuid4())
        self.tasks[task_id] = {
            'status': TaskStatus.PENDING,
            'start_time': time.time(),
            'result': None
        }
        
        def task_wrapper():
            self.tasks[task_id]['status'] = TaskStatus.PROCESSING
            try:
                result = task_func(*args, **kwargs)
                self.tasks[task_id].update({
                    'status': TaskStatus.COMPLETED,
                    'result': result,
                    'end_time': time.time()
                })
            except Exception as e:
                self.tasks[task_id].update({
                    'status': TaskStatus.FAILED,
                    'error': str(e),
                    'end_time': time.time()
                })
        
        self.executor.submit(task_wrapper)
        return task_id

    def get_task_status(self, task_id):
        return self.tasks.get(task_id)