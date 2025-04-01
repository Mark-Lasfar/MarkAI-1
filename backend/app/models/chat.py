# backend/app/models/chat.py
from pydantic import BaseModel, Field
from datetime import datetime
from typing import Optional, Dict, Any, List
from enum import Enum
from ..config import settings

class MessageType(str, Enum):
    """أنواع الرسائل المدعومة"""
    TEXT = "text"
    IMAGE = "image"
    AUDIO = "audio"
    DOCUMENT = "document"
    SYSTEM = "system"

class Message(BaseModel):
    """
    نموذج رسالة المحادثة الأساسي
    
    Attributes:
        content: محتوى الرسالة (نص أو رابط ملف)
        message_type: نوع الرسالة (text/image/audio/document)
        is_user: هل الرسالة من المستخدم أم من النظام؟
        timestamp: وقت إرسال الرسالة
        meta: بيانات وصفية إضافية
    """
    content: str
    message_type: MessageType = MessageType.TEXT
    is_user: bool = True
    timestamp: datetime = Field(default_factory=datetime.now)
    meta: Dict[str, Any] = Field(default_factory=dict)

    class Config:
        json_encoders = {
            datetime: lambda v: v.isoformat()
        }
        schema_extra = {
            "example": {
                "content": "مرحباً كيف حالك؟",
                "message_type": "text",
                "is_user": True,
                "timestamp": "2023-01-01T12:00:00Z",
                "meta": {}
            }
        }

class ChatSession(BaseModel):
    """
    نموذج جلسة المحادثة
    
    Attributes:
        session_id: معرف الجلسة الفريد
        created_at: وقت إنشاء الجلسة
        last_activity: آخر نشاط في الجلسة
        messages: قائمة الرسائل في الجلسة
        user_id: معرف المستخدم (اختياري)
    """
    session_id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    created_at: datetime = Field(default_factory=datetime.now)
    last_activity: datetime = Field(default_factory=datetime.now)
    messages: List[Message] = Field(default_factory=list)
    user_id: Optional[str] = None

    class Config:
        json_encoders = {
            datetime: lambda v: v.isoformat()
        }

class FileUploadResponse(BaseModel):
    """
    نموذج رد رفع الملف
    
    Attributes:
        filename: اسم الملف
        content_type: نوع الملف
        file_size: حجم الملف بالبايت
        message: رسالة حالة
        file_url: رابط الوصول للملف (اختياري)
    """
    filename: str
    content_type: str
    file_size: int
    message: str = "تم استلام الملف بنجاح"
    file_url: Optional[str] = None

    class Config:
        schema_extra = {
            "example": {
                "filename": "example.pdf",
                "content_type": "application/pdf",
                "file_size": 1024,
                "message": "File uploaded successfully",
                "file_url": "https://example.com/files/example.pdf"
            }
        }

class AIResponse(BaseModel):
    """
    نموذج رد الذكاء الاصطناعي
    
    Attributes:
        text: النص الأساسي للرد
        attachments: مرفقات إضافية
        is_final: هل هذا الرد نهائي؟
        request_id: معرف الطلب
    """
    text: str
    attachments: List[Dict[str, Any]] = Field(default_factory=list)
    is_final: bool = True
    request_id: str

    class Config:
        schema_extra = {
            "example": {
                "text": "هذا رد الذكاء الاصطناعي",
                "attachments": [],
                "is_final": True,
                "request_id": "123e4567-e89b-12d3-a456-426614174000"
            }
        }