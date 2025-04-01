// frontend/src/components/ContextAwareChat.jsx
import { useState, useEffect, useRef } from 'react';
import { useUser } from '../context/UserContext';
import { trackInteraction, getRecommendations } from '../lib/api';
import SwaggerUI from 'swagger-ui-react';
import 'swagger-ui-react/swagger-ui.css';

export default function ContextAwareChat() {
  const [messages, setMessages] = useState([]);
  const [input, setInput] = useState('');
  const [context, setContext] = useState({});
  const [showDocs, setShowDocs] = useState(false);
  const { user } = useUser();
  const memoryRef = useRef({});

  const fetchAPIResponse = async (endpoint, data) => {
    const response = await fetch(`/api/${endpoint}`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        'Authorization': `Bearer ${user.token}`
      },
      body: JSON.stringify(data)
    });

    if (!response.ok) {
      throw new Error(`API Error: ${response.status}`);
    }
    return await response.json();
  };

  const handleSend = async () => {
    if (!input.trim()) return;
    
    try {
      // تسجيل التفاعل
      await trackInteraction('chat_message', {
        user_id: user.id,
        message: input,
        context: memoryRef.current
      });

      // إرسال الرسالة
      const data = await fetchAPIResponse('chat', {
        type: 'message',
        content: input,
        context: memoryRef.current
      });

      // تحديث الذاكرة والرسائل
      if (data.context) {
        memoryRef.current = { ...memoryRef.current, ...data.context };
        setContext(memoryRef.current);
      }

      setMessages(prev => [...prev, 
        { text: input, isUser: true },
        { text: data.response, isUser: false }
      ]);
      setInput('');
    } catch (error) {
      console.error('Chat error:', error);
    }
  };

  const handleFileUpload = async (file) => {
    try {
      const formData = new FormData();
      formData.append('file', file);
      
      const response = await fetch('/api/chat', {
        method: 'POST',
        headers: {
          'Authorization': `Bearer ${user.token}`
        },
        body: formData
      });

      const data = await response.json();
      setMessages(prev => [...prev, 
        { text: `File: ${file.name}`, isUser: true },
        { text: data.message, isUser: false }
      ]);
    } catch (error) {
      console.error('Upload error:', error);
    }
  };

  useEffect(() => {
    const loadRecs = async () => {
      try {
        const recs = await getRecommendations(user.id);
        memoryRef.current.recommendations = recs;
      } catch (error) {
        console.error('Failed to load recommendations:', error);
      }
    };
    loadRecs();
  }, [user.id]);

  return (
    <div className="chat-container">
      {showDocs ? (
        <div className="docs-panel">
          <button onClick={() => setShowDocs(false)}>Back to Chat</button>
          <SwaggerUI url={`${process.env.NEXT_PUBLIC_BACKEND_URL}/openapi.json`} />
        </div>
      ) : (
        <>
          <div className="chat-header">
            <h3>MarkAI Chat</h3>
            <button onClick={() => setShowDocs(true)}>View API Docs</button>
          </div>

          <div className="chat-messages">
            {messages.map((msg, i) => (
              <div key={i} className={`message ${msg.isUser ? 'user' : 'ai'}`}>
                {msg.text}
              </div>
            ))}
          </div>

          <div className="chat-controls">
            <input
              value={input}
              onChange={(e) => setInput(e.target.value)}
              placeholder="Type your message..."
              onKeyPress={(e) => e.key === 'Enter' && handleSend()}
            />
            <input
              type="file"
              id="file-upload"
              onChange={(e) => handleFileUpload(e.target.files[0])}
              style={{ display: 'none' }}
            />
            <label htmlFor="file-upload" className="file-button">
              Upload File
            </label>
            <button onClick={handleSend}>Send</button>
          </div>

          <div className="context-panel">
            <h4>Current Context</h4>
            <pre>{JSON.stringify(context, null, 2)}</pre>
          </div>
        </>
      )}
    </div>
  );
}