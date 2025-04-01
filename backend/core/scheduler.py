# backend/core/scheduler.py
from apscheduler.schedulers.background import BackgroundScheduler
from datetime import datetime

class TaskScheduler:
    def __init__(self):
        self.scheduler = BackgroundScheduler()
        self.scheduler.start()
        
    def schedule_cleanup(self):
        """تنظيف الملفات المؤقتة يومياً"""
        self.scheduler.add_job(
            self._clean_temp_files,
            'cron',
            hour=3,
            minute=0
        )
    
    def _clean_temp_files(self):
        from core.config import Config
        import shutil
        try:
            for item in Config.UPLOAD_FOLDER.glob('*'):
                if item.is_file():
                    item.unlink()
                else:
                    shutil.rmtree(item)
            self.logger.info(f"Temp files cleaned at {datetime.now()}")
        except Exception as e:
            self.logger.error(f"Cleanup failed: {str(e)}")