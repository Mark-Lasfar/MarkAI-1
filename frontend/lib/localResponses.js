// lib/localResponses.js
export const getLocalResponse = (message) => {
    const responses = {
      "hi": "مرحبًا! كيف يمكنني مساعدتك اليوم؟",
      "hello": "أهلاً وسهلاً! ما الذي تريد معرفته؟",
      "help": "يمكنني المساعدة في:\n- معرفة التاريخ والوقت\n- الإجابة على أسئلة عامة\n- شرح مفاهيم بسيطة",
      "ما اسمك": "أنا مساعدك الذكي، ليس لدي اسم لكن يمكنك مناداتي كما تريد!",
      "default": "لم أفهم السؤال تمامًا. يمكنك إعادة صياغته؟"
    };
  
    const lowerMessage = message.toLowerCase();
    
    // معالجة الأسئلة الديناميكية
    if (lowerMessage.includes("اليوم") || lowerMessage.includes("التاريخ")) {
      return `اليوم هو ${new Date().toLocaleDateString('ar-SA', { 
        weekday: 'long', 
        year: 'numeric', 
        month: 'long', 
        day: 'numeric' 
      })}`;
    }
    
    if (lowerMessage.includes("الوقت")) {
      return `الوقت الآن: ${new Date().toLocaleTimeString('ar-SA')}`;
    }
  
    return responses[lowerMessage] || responses.default;
  };