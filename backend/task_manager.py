# backend/task_manager.py
import threading
from queue import Queue
from datetime import datetime

class TaskManager:
    def __init__(self):
        self.task_queue = Queue()
        self.results = {}
        self.worker = threading.Thread(target=self._process_tasks, daemon=True)
        self.worker.start()

    def _process_tasks(self):
        while True:
            task_id, func, args, kwargs = self.task_queue.get()
            try:
                result = func(*args, **kwargs)
                self.results[task_id] = {
                    'status': 'completed',
                    'result': result,
                    'finished_at': datetime.now()
                }
            except Exception as e:
                self.results[task_id] = {
                    'status': 'failed',
                    'error': str(e)
                }

    def submit_task(self, func, *args, **kwargs):
        task_id = str(datetime.now().timestamp())
        self.task_queue.put((task_id, func, args, kwargs))
        return task_id

    def get_task_result(self, task_id):
        return self.results.get(task_id)