from fastapi import FastAPI, UploadFile, File, HTTPException, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import JSONResponse
from pathlib import Path
import shutil
import uuid
import logging
from typing import Dict, List, Optional
from pydantic import BaseModel
import torch
from transformers import (
    AutoModelForCausalLM,
    AutoTokenizer,
    pipeline
)
import numpy as np
from concurrent.futures import ThreadPoolExecutor
from datetime import datetime

app = FastAPI(title="MarkAI Fusion", version="3.0")

# CORS Configuration
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# Model Configuration
MODEL_PATHS = {
    "bloom": "/home/mark/hager/bloom-7b1",
    "falcon": "/home/mark/hager/falcon-7b",
    "gpt-j": "/home/mark/hager/gpt-j-6B"
}

MODELS = {}
DEVICE = "cuda" if torch.cuda.is_available() else "cpu"
EXECUTOR = ThreadPoolExecutor(max_workers=4)

class ChatRequest(BaseModel):
    message: str
    file: Optional[str] = None

class HybridResponse(BaseModel):
    response: str
    components: Dict[str, str]
    confidence: float
    request_id: str
    timestamp: str

def load_model(model_name: str):
    """تحميل النموذج مع إدارة الذاكرة الذكية"""
    try:
        tokenizer = AutoTokenizer.from_pretrained(MODEL_PATHS[model_name])
        model = AutoModelForCausalLM.from_pretrained(
            MODEL_PATHS[model_name],
            torch_dtype=torch.float16 if DEVICE == "cuda" else torch.float32,
            device_map="auto",
            low_cpu_mem_usage=True
        )
        return {"tokenizer": tokenizer, "model": model}
    except Exception as e:
        logging.error(f"Error loading {model_name}: {str(e)}")
        return None

@app.on_event("startup")
async def startup_event():
    """تحميل النماذج بشكل غير متزامن مع إدارة الذاكرة"""
    global MODELS
    try:
        futures = {model: EXECUTOR.submit(load_model, model) for model in MODEL_PATHS}
        MODELS = {model: future.result() for model, future in futures.items()}
        logging.info("All models loaded with optimized memory management")
    except Exception as e:
        logging.error(f"Model loading failed: {str(e)}")
        raise

def intelligent_router(prompt: str) -> List[str]:
    """توجيه ذكي للاستعلامات بناءً على نوع المحتوى"""
    prompt_lower = prompt.lower()
    
    # كود برمجي
    if any(kw in prompt_lower for kw in ['كود', 'برمجة', 'خطأ', 'bug', 'code', 'function', 'دالة']):
        return ['gpt-j', 'bloom']
    
    # إبداعي
    elif any(kw in prompt_lower for kw in ['قصة', 'رواية', 'تخيل', 'story', 'create', 'اكتب', 'تأليف']):
        return ['falcon', 'bloom']
    
    # تقني
    elif any(kw in prompt_lower for kw in ['شرح', 'كيف', 'how', 'why', 'مبدأ', 'explain']):
        return ['gpt-j', 'bloom']
    
    # صور/وسائط
    elif any(kw in prompt_lower for kw in ['صورة', 'رسم', 'image', 'picture', 'فيديو', 'video']):
        return ['bloom', 'falcon']
    
    # عام
    else:
        return ['bloom', 'falcon', 'gpt-j']

async def generate_response(model_name: str, prompt: str, **kwargs):
    """توليد رد مع إدارة الموارد الذكية"""
    try:
        model_data = MODELS.get(model_name)
        if not model_data:
            return None
            
        inputs = model_data['tokenizer'](
            prompt, 
            return_tensors="pt",
            max_length=512,
            truncation=True
        ).to(DEVICE)
        
        outputs = model_data['model'].generate(
            **inputs,
            max_new_tokens=kwargs.get('max_length', 150),
            temperature=kwargs.get('temperature', 0.7),
            num_return_sequences=1,
            pad_token_id=model_data['tokenizer'].eos_token_id
        )
        
        return model_data['tokenizer'].decode(outputs[0], skip_special_tokens=True)
    except Exception as e:
        logging.error(f"Generation error in {model_name}: {str(e)}")
        return None

async def ensemble_responses(prompt: str) -> dict:
    """دمج ردود النماذج باستخدام خوارزمية متقدمة"""
    # تحديد النماذج المناسبة
    selected_models = intelligent_router(prompt)
    
    # توليد الردود بشكل متوازي
    futures = [EXECUTOR.submit(generate_response, model, prompt) for model in selected_models]
    results = {}
    
    for model, future in zip(selected_models, futures):
        try:
            results[model] = future.result()
        except Exception as e:
            logging.error(f"Error in {model}: {str(e)}")
    
    # تحليل وتجميع النتائج
    responses = [resp for resp in results.values() if resp]
    
    if not responses:
        raise ValueError("All models failed to generate response")
    
    # خوارزمية دمج ذكية
    combined_response = max(set(responses), key=responses.count)
    
    # حساب الثقة
    confidence = sum(1 for r in responses if r == combined_response) / len(responses)
    
    return {
        "final_response": combined_response,
        "components": results,
        "confidence": confidence
    }

@app.post("/api/chat", response_model=HybridResponse)
async def handle_chat(request: ChatRequest):
    """نقطة النهاية الذكية للمحادثة"""
    try:
        prompt = request.message
        if not prompt:
            raise HTTPException(status_code=400, detail="Empty input")
        
        # معالجة الملفات المرفقة إن وجدت
        if request.file:
            file_analysis = await process_attached_file(request.file)
            prompt += f"\n[ملف مرفق: {file_analysis}]"
        
        # توليد الرد المدعم
        ensemble_result = await ensemble_responses(prompt)
        
        return {
            "response": ensemble_result['final_response'],
            "components": ensemble_result['components'],
            "confidence": ensemble_result['confidence'],
            "request_id": str(uuid.uuid4()),
            "timestamp": datetime.now().isoformat()
        }
        
    except Exception as e:
        logging.error(f"Chat error: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

async def process_attached_file(file_data: str):
    """معالجة الملفات المرفقة بشكل متقدم"""
    try:
        # هنا يمكنك إضافة معالجة الملفات الفعلية
        # حالياً نكتفي بإرجاع نوع الملف فقط
        return f"تم تحليل الملف المرفق ({file_data[:20]}...)"
    except Exception as e:
        logging.error(f"File processing error: {str(e)}")
        return "خطأ في تحليل الملف"

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)