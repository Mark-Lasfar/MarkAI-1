import { useState } from 'react'
import { useQuery } from 'react-query'
import axios from 'axios'
import Head from 'next/head'

export default function AIGenerate() {
  const [prompt, setPrompt] = useState('')
  const [model, setModel] = useState('bloom')
  const [maxLength, setMaxLength] = useState(200)

  const { data, isLoading, error, refetch } = useQuery(
    ['ai-generate', prompt, model, maxLength],
    async () => {
      if (!prompt.trim()) return null
      const res = await axios.post('/api/ai/generate', {
        model_name: model,
        prompt,
        max_length: maxLength
      })
      return res.data.result
    },
    { enabled: false }
  )

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault()
    refetch()
  }

  return (
    <div className="min-h-screen bg-gray-50 py-12 px-4 sm:px-6 lg:px-8">
      <Head>
        <title>MarkAI - Text Generation</title>
      </Head>

      <div className="max-w-3xl mx-auto">
        <div className="text-center mb-8">
          <h1 className="text-3xl font-bold text-gray-900">MarkAI Text Generation</h1>
          <p className="mt-2 text-lg text-gray-600">
            استخدم نماذج الذكاء الاصطناعي المحلية لتوليد النصوص
          </p>
        </div>

        <form onSubmit={handleSubmit} className="bg-white shadow rounded-lg p-6 mb-8">
          <div className="mb-4">
            <label htmlFor="model" className="block text-sm font-medium text-gray-700 mb-1">
              النموذج
            </label>
            <select
              id="model"
              value={model}
              onChange={(e) => setModel(e.target.value)}
              className="w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm"
            >
              <option value="bloom">BLOOM (7B)</option>
              <option value="falcon">Falcon (7B)</option>
              <option value="gpt-j">GPT-J (6B)</option>
            </select>
          </div>

          <div className="mb-4">
            <label htmlFor="prompt" className="block text-sm font-medium text-gray-700 mb-1">
              النص المطلوب
            </label>
            <textarea
              id="prompt"
              rows={4}
              value={prompt}
              onChange={(e) => setPrompt(e.target.value)}
              className="w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm"
              placeholder="اكتب النص الذي تريد إكماله..."
            />
          </div>

          <div className="mb-4">
            <label htmlFor="maxLength" className="block text-sm font-medium text-gray-700 mb-1">
              الطول الأقصى (Tokens)
            </label>
            <input
              type="number"
              id="maxLength"
              min="50"
              max="1000"
              value={maxLength}
              onChange={(e) => setMaxLength(Number(e.target.value))}
              className="w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm"
            />
          </div>

          <button
            type="submit"
            disabled={isLoading}
            className="w-full bg-blue-600 text-white py-2 px-4 rounded-md hover:bg-blue-700 disabled:opacity-50"
          >
            {isLoading ? 'جاري التوليد...' : 'توليد النص'}
          </button>
        </form>

        {error && (
          <div className="bg-red-50 border-l-4 border-red-400 p-4 mb-8">
            <div className="flex">
              <div className="text-red-400">
                <svg className="h-5 w-5" fill="currentColor" viewBox="0 0 20 20">
                  <path fillRule="evenodd" d="M10 18a8 8 0 100-16 8 8 0 000 16zM8.707 7.293a1 1 0 00-1.414 1.414L8.586 10l-1.293 1.293a1 1 0 101.414 1.414L10 11.414l1.293 1.293a1 1 0 001.414-1.414L11.414 10l1.293-1.293a1 1 0 00-1.414-1.414L10 8.586 8.707 7.293z" clipRule="evenodd" />
                </svg>
              </div>
              <div className="ml-3">
                <p className="text-sm text-red-700">
                  {error.message || 'حدث خطأ أثناء توليد النص'}
                </p>
              </div>
            </div>
          </div>
        )}

        {data && (
          <div className="bg-white shadow rounded-lg p-6">
            <h2 className="text-lg font-medium text-gray-900 mb-4">النتيجة</h2>
            <div className="prose max-w-none">
              <p className="whitespace-pre-wrap">{data}</p>
            </div>
          </div>
        )}
      </div>
    </div>
  )
}
