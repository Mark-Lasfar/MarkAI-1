# backend/app/core/collaborative_scheduler.py
from apscheduler.schedulers.background import BackgroundScheduler
from datetime import datetime, timedelta
from app.ai.collaborative_learning import CollaborativeLearner
import logging

logger = logging.getLogger(__name__)

class CollaborativeScheduler:
    def __init__(self):
        self.scheduler = BackgroundScheduler()
        self.learner = CollaborativeLearner()
        
    def start(self):
        """بدء جدولة المهام"""
        # تحديث التجميعات كل يوم في 3 صباحاً
        self.scheduler.add_job(
            self.update_clusters,
            'cron',
            hour=3,
            minute=0
        )
        
        # تنظيف البيانات القديمة أسبوعياً
        self.scheduler.add_job(
            self.clean_old_data,
            'cron',
            day_of_week='sun',
            hour=4
        )
        
        self.scheduler.start()
    
    def update_clusters(self):
        """تحديث تجميعات المستخدمين"""
        try:
            logger.info("Starting cluster update...")
            self.learner.update_clusters()
            logger.info("Cluster update completed successfully")
        except Exception as e:
            logger.error(f"Cluster update failed: {str(e)}")
    
    def clean_old_data(self):
        """تنظيف التحسينات القديمة"""
        try:
            logger.info("Cleaning old shared improvements...")
            cutoff = datetime.now() - timedelta(days=30)
            self.learner.users.update_many(
                {},
                {"$pull": {
                    "shared_improvements": {
                        "timestamp": {"$lt": cutoff}
                    }
                }}
            )
            logger.info("Old data cleaning completed")
        except Exception as e:
            logger.error(f"Data cleaning failed: {str(e)}")