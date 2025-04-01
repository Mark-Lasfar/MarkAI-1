import { useState, useRef } from 'react';
import styles from '../styles/Chat.module.css';
import { FiSend, FiUpload, FiAlertCircle } from 'react-icons/fi';

export default function ChatUI() {
  const [messages, setMessages] = useState([]);
  const [input, setInput] = useState('');
  const [isLoading, setIsLoading] = useState(false);
  const fileInputRef = useRef();

  const handleSend = () => {
    if (!input.trim()) return;
    
    // إضافة رسالة المستخدم
    const userMessage = { text: input, isUser: true };
    setMessages(prev => [...prev, userMessage]);
    setInput('');
    setIsLoading(true);
    
    // محاكاة استجابة الذكاء الاصطناعي
    setTimeout(() => {
      const aiResponse = { 
        text: "هذا رد تجريبي. سيتم استبداله باتصال فعلي بالخادم.",
        isUser: false 
      };
      setMessages(prev => [...prev, aiResponse]);
      setIsLoading(false);
    }, 1500);
  };

  const handleFileUpload = (e) => {
    const file = e.target.files[0];
    if (!file) return;
    
    setIsLoading(true);
    const fileMessage = { text: `تم رفع الملف: ${file.name}`, isUser: true };
    setMessages(prev => [...prev, fileMessage]);
    
    setTimeout(() => {
      const response = { 
        text: "تم معالجة الملف بنجاح. يحتوي على 3 صفحات.",
        isUser: false 
      };
      setMessages(prev => [...prev, response]);
      setIsLoading(false);
    }, 2000);
  };

  return (
    <div className={styles.container}>
      <div className={styles.header}>
        <h1>MarkAI</h1>
      </div>
      
      <div className={styles.chatArea}>
        {messages.length === 0 ? (
          <div className={styles.welcomeMessage}>
            <h2>كيف يمكنني مساعدتك؟</h2>
            <div className={styles.suggestions}>
              <div className={styles.suggestionCard}>
                <h3>اطلب أي شيء</h3>
                <p>اكتشف إمكانيات الذكاء الاصطناعي</p>
              </div>
              <div className={styles.suggestionCard}>
                <h3>تحليل الملفات</h3>
                <p>رفع المستندات والصور للتحليل</p>
              </div>
            </div>
          </div>
        ) : (
          messages.map((msg, i) => (
            <div key={i} className={`${styles.message} ${msg.isUser ? styles.userMessage : styles.aiMessage}`}>
              {msg.text}
            </div>
          ))
        )}
        
        {isLoading && (
          <div className={styles.loadingIndicator}>
            <div className={styles.dot}></div>
            <div className={styles.dot}></div>
            <div className={styles.dot}></div>
          </div>
        )}
      </div>
      
      <div className={styles.inputContainer}>
        <div className={styles.inputBox}>
          <input
            type="text"
            value={input}
            onChange={(e) => setInput(e.target.value)}
            placeholder="اكتب رسالتك هنا..."
            onKeyPress={(e) => e.key === 'Enter' && handleSend()}
            disabled={isLoading}
          />
          <button 
            onClick={() => fileInputRef.current.click()}
            disabled={isLoading}
          >
            <FiUpload />
          </button>
          <button
            onClick={handleSend}
            disabled={isLoading || !input.trim()}
          >
            <FiSend />
          </button>
        </div>
        <input
          type="file"
          ref={fileInputRef}
          onChange={handleFileUpload}
          className={styles.fileInput}
          disabled={isLoading}
        />
        <div className={styles.disclaimer}>
          <FiAlertCircle />
          <span>MarkAI قد يقدم معلومات غير دقيقة. يرجى التحقق من المعلومات المهمة.</span>
        </div>
      </div>
    </div>
  );
}