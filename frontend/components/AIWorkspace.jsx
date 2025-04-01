// frontend/components/AIWorkspace.jsx
import { useState, useRef, useEffect } from 'react'
import { useRouter } from 'next/router'
import dynamic from 'next/dynamic'

// Dynamic imports for better performance
const CodeEditor = dynamic(() => import('./CodeEditor'), { ssr: false })
const MediaPlayer = dynamic(() => import('./MediaPlayer'), { ssr: false })

export default function AIWorkspace() {
  const [activeTab, setActiveTab] = useState('chat')
  const [darkMode, setDarkMode] = useState(false)
  const fileInputRef = useRef()
  const router = useRouter()

  const tabs = [
    { id: 'chat', name: 'محادثة', icon: '💬' },
    { id: 'code', name: 'توليد أكواد', icon: '💻' },
    { id: 'media', name: 'وسائط', icon: '🎬' },
    { id: 'files', name: 'ملفات', icon: '📁' }
  ]

  return (
    <div className={`min-h-screen ${darkMode ? 'dark bg-gray-900' : 'bg-gray-50'}`}>
      <div className="container mx-auto px-4 py-8">
        {/* شريط التحكم العلوي */}
        <div className="flex justify-between items-center mb-8">
          <h1 className="text-3xl font-bold text-primary dark:text-white">
            مساحة العمل الذكية
          </h1>
          <button 
            onClick={() => setDarkMode(!darkMode)}
            className="p-2 rounded-full bg-gray-200 dark:bg-gray-700"
          >
            {darkMode ? '☀️' : '🌙'}
          </button>
        </div>

        {/* شريط التبويبات */}
        <div className="flex border-b border-gray-200 dark:border-gray-700 mb-6">
          {tabs.map(tab => (
            <button
              key={tab.id}
              onClick={() => setActiveTab(tab.id)}
              className={`px-4 py-2 font-medium ${activeTab === tab.id 
                ? 'border-b-2 border-primary text-primary dark:text-white' 
                : 'text-gray-500 dark:text-gray-400'}`}
            >
              {tab.icon} {tab.name}
            </button>
          ))}
        </div>

        {/* محتوى التبويبات */}
        <div className="bg-white dark:bg-gray-800 rounded-xl shadow-lg p-6">
          {activeTab === 'chat' && <ChatInterface darkMode={darkMode} />}
          {activeTab === 'code' && <CodeEditor darkMode={darkMode} />}
          {activeTab === 'media' && <MediaPlayer />}
          {activeTab === 'files' && <FileProcessor ref={fileInputRef} />}
        </div>
      </div>
    </div>
  )
}