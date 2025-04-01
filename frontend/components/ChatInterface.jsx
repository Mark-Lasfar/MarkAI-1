import { useState, useEffect, useRef } from 'react';
import { useRouter } from 'next/router';
import axios from 'axios';
import { trackInteraction } from '../lib/tracking';
import RecommendationBar from './RecommendationBar';
import styles from '../Chat.module.css';

export default function ChatInterface({ darkMode }) {
  const [messages, setMessages] = useState([
    { text: "مرحباً، أنا MarkAI. كيف يمكنني مساعدتك اليوم؟", isUser: false }
  ]);
  const [input, setInput] = useState('');
  const [isLoading, setIsLoading] = useState(false);
  const [model, setModel] = useState('bloom');
  const messagesEndRef = useRef(null);
  const router = useRouter();

  useEffect(() => {
    trackInteraction('chat_page_loaded', { model });
    scrollToBottom();
  }, []);

  useEffect(() => {
    scrollToBottom();
  }, [messages]);

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: "smooth" });
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    if (!input.trim()) return;

    const userMessage = { text: input, isUser: true };
    setMessages(prev => [...prev, userMessage]);
    setInput('');
    setIsLoading(true);

    try {
      await trackInteraction('message_sent', { 
        text: input, 
        model,
        length: input.length 
      });

      const response = await axios.post('/api/chat', {
        message: input,
        model
      });

      const aiMessage = { text: response.data.response, isUser: false };
      setMessages(prev => [...prev, aiMessage]);

      await trackInteraction('ai_response', {
        input_length: input.length,
        output_length: aiMessage.text.length,
        model,
        response_quality: 1
      });
    } catch (error) {
      console.error('Error:', error);
      setMessages(prev => [...prev, { 
        text: 'حدث خطأ أثناء المعالجة. يرجى المحاولة لاحقاً.', 
        isUser: false 
      }]);
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <div className={styles.chatContainer}>
      <div className={styles.header}>
        <h1>MarkAI</h1>
        <div className={styles.controls}>
          <button>العمرات</button>
          <button>الإعدادات</button>
        </div>
      </div>

      <div className={styles.chatArea}>
        {messages.map((message, index) => (
          <div 
            key={index} 
            className={`${styles.message} ${
              message.isUser ? styles.userMessage : styles.aiMessage
            }`}
          >
            {message.text}
          </div>
        ))}
        {isLoading && (
          <div className={styles.loadingIndicator}>
            <div className={styles.dot}></div>
            <div className={styles.dot}></div>
            <div className={styles.dot}></div>
          </div>
        )}
        <div ref={messagesEndRef} />
      </div>

      <RecommendationBar userId={router.query.userId} />

      <form onSubmit={handleSubmit} className={styles.inputForm}>
        <div className={styles.inputContainer}>
          <select
            value={model}
            onChange={(e) => setModel(e.target.value)}
            className={styles.modelSelector}
          >
            <option value="bloom">BLOOM (العربية)</option>
            <option value="falcon">Falcon (الإنجليزية)</option>
            <option value="gpt-j">GPT-J (متعدد اللغات)</option>
          </select>
          <input
            type="text"
            value={input}
            onChange={(e) => setInput(e.target.value)}
            placeholder="اكتب رسالتك هنا..."
            className={styles.textInput}
            disabled={isLoading}
          />
          <button
            type="submit"
            disabled={isLoading || !input.trim()}
            className={styles.submitButton}
          >
            إرسال
          </button>
        </div>
      </form>
    </div>
  );
}