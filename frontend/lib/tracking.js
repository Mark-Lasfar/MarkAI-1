// frontend/lib/tracking.js
/**
 * دالة لتسجيل التفاعلات مع التطبيق
 * @param {string} action نوع التفاعل (مثال: page_view, chat_message)
 * @param {object} metadata بيانات إضافية عن التفاعل (مثال: page_name, model_used)
 * @returns {Promise<object>} وعد بالبيانات التي تم تسجيلها
 */
export const track = async (action, metadata = {}) => {
  try {
    // إعداد رأس الطلب
    const headers = {
      'Content-Type': 'application/json',
      'Authorization': `Bearer ${localStorage.getItem('token')}`
    };

    // إعداد جسم الطلب
    const body = JSON.stringify({
      action,
      ...metadata,
      timestamp: new Date().toISOString()
    });

    // إرسال الطلب
    const response = await fetch('/api/tracking', {
      method: 'POST',
      headers,
      body
    });

    // إرجاع البيانات التي تم تسجيلها
    return await response.json();
  } catch (error) {
    console.error('Failed to track interaction:', error);
  }
};

// مثال للاستخدام في مكون React
useEffect(() => {
  track('page_view', {
    page: 'Chat Interface',
    model_used: 'bloom'
  });
}, []);

// مثال للاستخدام في دالة أخرى
const logChatMessage = async () => {
  await track('chat_message', {
    model_used: 'bloom'
  });
};