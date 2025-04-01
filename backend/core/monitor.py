# backend/core/monitor.py
import psutil
import logging
from threading import Timer

class SystemMonitor:
    def __init__(self):
        self.logger = logging.getLogger('system_monitor')
        self.check_interval = 60  # ثانية
        
    def start(self):
        self._schedule_next_check()
        
    def _check_system(self):
        cpu = psutil.cpu_percent()
        mem = psutil.virtual_memory().percent
        disk = psutil.disk_usage('/').percent
        
        if cpu > 80 or mem > 80 or disk > 90:
            self.logger.warning(f"High system usage - CPU: {cpu}%, Memory: {mem}%, Disk: {disk}%")
        
        self._schedule_next_check()
    
    def _schedule_next_check(self):
        Timer(self.check_interval, self._check_system).start()