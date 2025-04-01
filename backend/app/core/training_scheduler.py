# backend/app/core/training_scheduler.py
from apscheduler.schedulers.background import BackgroundScheduler
from app.ai.model_finetuner import ModelFinetuner
from app.db import get_interactions_collection
import logging
from datetime import datetime, timedelta

logger = logging.getLogger(__name__)

class TrainingScheduler:
    def __init__(self, model):
        self.scheduler = BackgroundScheduler()
        self.finetuner = ModelFinetuner(model)
        self.interactions = get_interactions_collection()
    
    def start(self):
        """بدء جدولة التدريب الدوري"""
        self.scheduler.add_job(
            self.run_finetuning,
            'cron',
            day_of_week='sun',
            hour=3
        )
        self.scheduler.start()
    
    def run_finetuning(self):
        """تنفيذ عملية ضبط النموذج"""
        try:
            logger.info("Starting periodic model finetuning...")
            self._finetune_on_recent_interactions()
        except Exception as e:
            logger.error(f"Finetuning failed: {str(e)}")
    
    def _finetune_on_recent_interactions(self):
        """ضبط النموذج على التفاعلات الحديثة"""
        last_week = datetime.now() - timedelta(days=7)
        recent_interactions = list(self.interactions.find({
            "timestamp": {"$gte": last_week},
            "rating": {"$exists": True}
        }))
        
        if len(recent_interactions) > 50:  # حد أدنى للتدريب
            self.finetuner.finetune_on_interactions(recent_interactions)
            logger.info(f"Finetuned on {len(recent_interactions)} interactions")
        else:
            logger.info("Not enough interactions for finetuning")