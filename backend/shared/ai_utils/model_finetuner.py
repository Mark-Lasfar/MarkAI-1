# backend/app/ai/model_finetuner.py
from transformers import Trainer, TrainingArguments
from datetime import datetime
import torch
from torch.utils.data import Dataset
import numpy as np

class InteractionDataset(Dataset):
    def __init__(self, interactions):
        self.interactions = interactions
    
    def __len__(self):
        return len(self.interactions)
    
    def __getitem__(self, idx):
        item = self.interactions[idx]
        return {
            "input_text": item["input"],
            "output_text": item["output"],
            "rating": item.get("rating", 0)
        }

class ModelFinetuner:
    def __init__(self, base_model):
        self.base_model = base_model
        self.training_history = []
    
    def finetune_on_interactions(self, interactions, epochs=1):
        """ضبط النموذج على التفاعلات الجديدة"""
        dataset = InteractionDataset(interactions)
        
        training_args = TrainingArguments(
            output_dir="./finetuned",
            num_train_epochs=epochs,
            per_device_train_batch_size=4,
            logging_dir='./logs',
            logging_steps=10,
            save_steps=100
        )
        
        trainer = Trainer(
            model=self.base_model,
            args=training_args,
            train_dataset=dataset,
        )
        
        trainer.train()
        
        self.training_history.append({
            "timestamp": datetime.now(),
            "interactions_count": len(interactions),
            "loss": trainer.state.log_history[-1]["loss"]
        })
        
        return trainer.model