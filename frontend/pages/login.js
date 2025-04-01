// frontend/pages/login.js
import { useState } from 'react';
import { useRouter } from 'next/router';
import { useAuthStore } from '@/store/auth';
import Head from 'next/head';

export default function Login() {
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [error, setError] = useState('');
  const [isLoading, setIsLoading] = useState(false);
  const router = useRouter();
  const { setToken, setUser } = useAuthStore();

  const handleLogin = async (e) => {
    e.preventDefault();
    setIsLoading(true);
    setError('');

    try {
      // محاكاة طلب تسجيل الدخول
      await new Promise(resolve => setTimeout(resolve, 1000));
      
      // في تطبيق حقيقي، ستستخدم fetch للاتصال بالباكيند
      // const response = await fetch('/api/login', { ... });
      
      setToken('fake-jwt-token');
      setUser({ id: '1', name: 'مستخدم تجريبي', email });
      router.push('/chat');
    } catch (err) {
      setError('بيانات الدخول غير صحيحة أو الخادم غير متاح');
      console.error('Login error:', err);
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <div className="min-h-screen flex items-center justify-center bg-gray-50">
      <Head>
        <title>تسجيل الدخول | MarkAI</title>
      </Head>
      
      <div className="bg-white p-8 rounded-lg shadow-md w-full max-w-md">
        <h1 className="text-2xl font-bold text-center mb-6 text-gray-800">تسجيل الدخول إلى MarkAI</h1>
        
        {error && (
          <div className="mb-4 p-3 bg-red-100 text-red-700 rounded-lg text-sm">
            {error}
          </div>
        )}
        
        <form onSubmit={handleLogin} className="space-y-4">
          <div>
            <label className="block text-sm font-medium text-gray-700 mb-1">البريد الإلكتروني</label>
            <input
              type="email"
              value={email}
              onChange={(e) => setEmail(e.target.value)}
              className="w-full p-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
              required
              dir="ltr"
            />
          </div>
          
          <div>
            <label className="block text-sm font-medium text-gray-700 mb-1">كلمة المرور</label>
            <input
              type="password"
              value={password}
              onChange={(e) => setPassword(e.target.value)}
              className="w-full p-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
              required
            />
          </div>
          
          <button
            type="submit"
            disabled={isLoading}
            className={`w-full py-3 px-4 bg-blue-600 hover:bg-blue-700 text-white font-medium rounded-lg transition-colors ${
              isLoading ? 'opacity-70 cursor-not-allowed' : ''
            }`}
          >
            {isLoading ? 'جاري التسجيل...' : 'تسجيل الدخول'}
          </button>
        </form>
      </div>
    </div>
  );
}