// frontend/pages/index.js
import { useRouter } from 'next/router';
import { useEffect } from 'react';
import { useAuthStore } from '@/store/auth';

export default function Home() {
  const router = useRouter();
  const { token } = useAuthStore();

  useEffect(() => {
    if (token) {
      router.push('/chat');
    } else {
      router.push('/login');
    }
  }, [token, router]);

  return null;
}