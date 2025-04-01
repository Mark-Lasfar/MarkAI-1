# دليل البدء السريع

## إعداد البيئة

1. تثبيت المتطلبات:
   ```bash
   # Backend
   cd backend && pip install -r requirements.txt
   
   # Frontend
   cd ../frontend && npm install
   
   # Mobile
   cd ../mobile && flutter pub get
   ```

2. تشغيل الخدمات:
   ```bash
   docker-compose -f infrastructure/docker-compose.yml up -d
   ```

## الوصول إلى التطبيق

- الواجهة الأمامية: http://localhost
- واجهة API: http://localhost/api/v1/docs
- نماذج الذكاء الاصطناعي المتاحة: bloom-7b1 falcon-7b gpt-j-6B
