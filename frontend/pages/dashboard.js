// frontend/pages/dashboard.js
import { useState } from 'react';
import axios from 'axios';

export default function Dashboard() {
  const [file, setFile] = useState(null);
  const [output, setOutput] = useState('');

  const handleFileUpload = async (e) => {
    e.preventDefault();
    const formData = new FormData();
    formData.append('file', file);
    
    const response = await axios.post('/api/process_file', formData);
    setOutput(response.data);
  };

  return (
    <div>
      <input type="file" onChange={(e) => setFile(e.target.files[0])} />
      <button onClick={handleFileUpload}>Process</button>
      <div>{output}</div>
    </div>
  );
}