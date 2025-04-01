import { useState, useRef, useEffect } from 'react';
import { FiSend, FiUpload, FiCheck, FiMic } from 'react-icons/fi';
import Head from 'next/head';
import { motion } from 'framer-motion';

export default function ChatPage() {
  const [messages, setMessages] = useState([]);
  const [input, setInput] = useState('');
  const [isProcessing, setIsProcessing] = useState(false);
  const [file, setFile] = useState(null);
  const messagesEndRef = useRef(null);

  const handleSend = async () => {
    if (!input.trim() || isProcessing) return;
    
    setIsProcessing(true);
    const userMessage = {
      text: input,
      isUser: true,
      timestamp: new Date().toLocaleTimeString(),
      file: file ? file.name : null
    };
    
    setMessages(prev => [...prev, userMessage]);
    setInput('');
    setFile(null);

    try {
      const response = await fetch('/api/chat', {
        method: 'POST',
        headers: {'Content-Type': 'application/json'},
        body: JSON.stringify({
          message: input,
          file: file ? file.name : null
        })
      });

      const data = await response.json();
      
      const aiResponse = {
        text: data.response,
        isUser: false,
        timestamp: new Date(data.timestamp).toLocaleTimeString(),
        confidence: data.confidence,
        components: data.components
      };
      
      setMessages(prev => [...prev, aiResponse]);
    } catch (error) {
      console.error('Error:', error);
      setMessages(prev => [...prev, { 
        text: "Error: Failed to get response", 
        isUser: false 
      }]);
    } finally {
      setIsProcessing(false);
    }
  };

  const handleFileChange = (e) => {
    const selectedFile = e.target.files[0];
    if (selectedFile) {
      setFile(selectedFile);
    }
  };

  useEffect(() => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  }, [messages]);

  return (
    <div className="min-h-screen bg-gray-50">
      <Head>
        <title>MarkAI Fusion Chat</title>
      </Head>

      <div className="max-w-2xl mx-auto p-4">
        {/* Chat Area */}
        <div className="h-[600px] overflow-y-auto bg-white rounded-lg p-4 shadow mb-4">
          {messages.map((msg, i) => (
            <motion.div
              key={i}
              initial={{ opacity: 0, y: 20 }}
              animate={{ opacity: 1, y: 0 }}
              className={`mb-4 p-4 rounded-lg ${
                msg.isUser ? 'bg-blue-100 ml-auto' : 'bg-gray-100'
              }`}
              style={{ maxWidth: '80%' }}
            >
              <div className="flex justify-between items-start mb-1">
                <p className="text-sm text-gray-600">
                  {msg.isUser ? 'You' : 'MarkAI Fusion'}
                </p>
                {!msg.isUser && (
                  <span className="text-xs bg-blue-500 text-white px-2 py-1 rounded">
                    Confidence: {(msg.confidence * 100).toFixed(0)}%
                  </span>
                )}
              </div>
              
              {msg.file && (
                <div className="bg-blue-50 p-2 rounded mb-2">
                  <p className="text-xs text-blue-600">File: {msg.file}</p>
                </div>
              )}
              
              <p className="text-gray-800">{msg.text}</p>
              
              <p className="text-xs text-gray-500 mt-2 text-right">
                {msg.timestamp}
              </p>
              
              {!msg.isUser && msg.components && (
                <details className="mt-2 text-xs text-gray-600">
                  <summary>Model Responses</summary>
                  <ul className="mt-1 space-y-1">
                    {Object.entries(msg.components).map(([model, response]) => (
                      <li key={model} className="border-t pt-1">
                        <strong>{model}:</strong> {response}
                      </li>
                    ))}
                  </ul>
                </details>
              )}
            </motion.div>
          ))}
          <div ref={messagesEndRef} />
        </div>

        {/* Input Area */}
        <div className="flex flex-col gap-2">
          <div className="flex gap-2">
            <label className="flex items-center justify-center p-2 bg-gray-200 rounded-lg cursor-pointer hover:bg-gray-300">
              <input 
                type="file" 
                className="hidden" 
                onChange={handleFileChange}
              />
              <FiUpload size={20} />
              {file && <FiCheck className="ml-1 text-green-500" size={16} />}
            </label>
            
            <input
              value={input}
              onChange={(e) => setInput(e.target.value)}
              onKeyPress={(e) => e.key === 'Enter' && handleSend()}
              placeholder="Type your message..."
              className="flex-1 p-2 border rounded-lg"
              disabled={isProcessing}
            />
            
            <button
              onClick={handleSend}
              disabled={isProcessing}
              className="p-2 bg-blue-600 text-white rounded-lg disabled:bg-gray-400"
            >
              <FiSend size={20} />
            </button>
          </div>
          
          {file && (
            <div className="text-sm text-gray-600 bg-blue-50 p-2 rounded">
              File attached: {file.name}
              <button 
                onClick={() => setFile(null)}
                className="ml-2 text-red-500 hover:text-red-700"
              >
                Remove
              </button>
            </div>
          )}
        </div>

        {isProcessing && (
          <div className="mt-2 text-center text-gray-600">
            Processing with MarkAI Fusion...
          </div>
        )}
      </div>
    </div>
  );
}