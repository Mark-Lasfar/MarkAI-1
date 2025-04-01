// frontend/src/components/SmartInterface.jsx
import React, { useState } from 'react';
import axios from 'axios';

const SmartInterface = () => {
  const [input, setInput] = useState('');
  const [file, setFile] = useState(null);
  const [result, setResult] = useState(null);
  const [isProcessing, setIsProcessing] = useState(false);

  const handleSubmit = async (e) => {
    e.preventDefault();
    setIsProcessing(true);
    
    try {
      const formData = new FormData();
      if (file) {
        formData.append('file', file);
      } else if (input) {
        formData.append('text', input);
      }

      const response = await axios.post('/api/smart-process', formData, {
        headers: {
          'Content-Type': 'multipart/form-data'
        }
      });

      setResult(response.data.result);
    } catch (error) {
      console.error('Error:', error);
    } finally {
      setIsProcessing(false);
    }
  };

  return (
    <div className="max-w-4xl mx-auto p-6">
      <div className="bg-white rounded-lg shadow-md p-6">
        <h1 className="text-2xl font-bold text-gray-800 mb-6">النظام الذكي المتكامل</h1>
        
        <form onSubmit={handleSubmit} className="space-y-4">
          <div>
            <label className="block text-gray-700 mb-2">أدخل النص أو اختر ملف:</label>
            <textarea
              value={input}
              onChange={(e) => setInput(e.target.value)}
              className="w-full p-3 border border-gray-300 rounded-lg"
              rows={4}
              placeholder="اكتب شيئاً..."
              disabled={file !== null}
            />
          </div>
          
          <div className="flex items-center justify-between">
            <input
              type="file"
              onChange={(e) => setFile(e.target.files[0])}
              className="block w-full text-sm text-gray-500
                file:mr-4 file:py-2 file:px-4
                file:rounded-md file:border-0
                file:text-sm file:font-semibold
                file:bg-blue-50 file:text-blue-700
                hover:file:bg-blue-100"
              disabled={input !== ''}
            />
            
            <button
              type="submit"
              disabled={isProcessing || (!input && !file)}
              className="px-6 py-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700 disabled:opacity-50"
            >
              {isProcessing ? 'جاري المعالجة...' : 'ابدأ'}
            </button>
          </div>
        </form>

        {result && (
          <div className="mt-6 p-4 bg-gray-50 rounded-lg">
            <h2 className="text-lg font-semibold mb-2">النتيجة:</h2>
            {typeof result === 'string' ? (
              <p className="whitespace-pre-line">{result}</p>
            ) : (
              <pre className="overflow-auto max-h-60 p-2 bg-gray-100 rounded">
                {JSON.stringify(result, null, 2)}
              </pre>
            )}
          </div>
        )}
      </div>
    </div>
  );
};

export default SmartInterface;