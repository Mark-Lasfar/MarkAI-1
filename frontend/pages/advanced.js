// frontend/pages/advanced.js
import { useState } from 'react';
import axios from 'axios';

export default function AdvancedTools() {
  const [files, setFiles] = useState([]);
  const [output, setOutput] = useState(null);

  const handleComplexOperation = async () => {
    const formData = new FormData();
    files.forEach(file => formData.append('files', file));
    
    const response = await axios.post('/api/complex_operation', formData, {
      headers: {'Content-Type': 'multipart/form-data'}
    });
    
    setOutput(response.data.result_url);
  };

  return (
    <div className="container">
      <h1>أدوات متقدمة</h1>
      <input 
        type="file" 
        multiple 
        onChange={(e) => setFiles([...e.target.files])}
      />
      <button onClick={handleComplexOperation}>
        معالجة متقدمة
      </button>
      
      {output && (
        <div className="result">
          <a href={output} download>تحميل النتيجة</a>
        </div>
      )}
    </div>
  );
}