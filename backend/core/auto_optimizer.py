# backend/core/auto_optimizer.py
import psutil
import time
from threading import Thread
from transformers import logging as transformers_logging

class AutoOptimizer:
    OPTIMIZATION_PROFILES = {
        'low': {'max_workers': 2, 'model_quality': 'medium'},
        'medium': {'max_workers': 4, 'model_quality': 'high'},
        'high': {'max_workers': 8, 'model_quality': 'best'}
    }

    def __init__(self):
        self.running = True
        self.optimization_level = 1  # 1-3 (من الأقل إلى الأكثر عدوانية)
        self.profile = self.OPTIMIZATION_PROFILES['medium']  # الprofil الافتراضي
        transformers_logging.set_verbosity_error()

    def start(self):
        Thread(target=self._monitor_loop, daemon=True).start()

    def _monitor_loop(self):
        while self.running:
            cpu_usage = psutil.cpu_percent()
            mem_usage = psutil.virtual_memory().percent

            self._adjust_optimization(cpu_usage, mem_usage)
            time.sleep(30)

    def _adjust_optimization(self, cpu, mem):
        if cpu > 80 or mem > 80:
            self.optimization_level = 3
            self.profile = self.OPTIMIZATION_PROFILES['low']
            self._free_unused_resources()
        elif cpu > 60 or mem > 60:
            self.optimization_level = 2
            self.profile = self.OPTIMIZATION_PROFILES['medium']
        else:
            self.optimization_level = 1
            self.profile = self.OPTIMIZATION_PROFILES['high']

    def _free_unused_resources(self):
        import torch
        if torch.cuda.is_available():
            torch.cuda.empty_cache()

        import gc
        gc.collect()