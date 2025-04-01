# /backend/core/initialization.py
from ml.collaborative_learning import CollaborativeLearner
from ml.collaborative_scheduler import CollaborativeScheduler

def init_system():
    learner = CollaborativeLearner()
    scheduler = CollaborativeScheduler(learner)
    scheduler.start()  # يبدأ بتحليل البيانات كل 24 ساعة