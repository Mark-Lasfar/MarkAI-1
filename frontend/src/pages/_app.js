// frontend/src/pages/_app.js
import { useState, useEffect } from 'react'
import { AuthProvider } from '../context/AuthContext'
import { AIProvider } from '../context/AIContext'
import { MediaProvider } from '../context/MediaContext'
import '../styles/globals.css'
import '../styles/chat.css'
import Layout from '../components/Layout'
import Head from 'next/head'

function MyApp({ Component, pageProps }) {
  const [loading, setLoading] = useState(false)

  useEffect(() => {
    // Handle route changes
    const handleStart = () => setLoading(true)
    const handleComplete = () => setLoading(false)

    window.addEventListener('routeChangeStart', handleStart)
    window.addEventListener('routeChangeComplete', handleComplete)
    window.addEventListener('routeChangeError', handleComplete)

    return () => {
      window.removeEventListener('routeChangeStart', handleStart)
      window.removeEventListener('routeChangeComplete', handleComplete)
      window.removeEventListener('routeChangeError', handleComplete)
    }
  }, [])

  return (
    <>
      <Head>
        <title>{process.env.NEXT_PUBLIC_APP_NAME || 'MarkAI'}</title>
        <meta name="description" content="AI-powered content platform" />
        <link rel="icon" href="/favicon.ico" />
      </Head>

      <AuthProvider>
        <AIProvider>
          <MediaProvider>
            <Layout>
              {loading ? (
                <div className="loading-overlay">
                  <div className="loader"></div>
                </div>
              ) : (
                <Component {...pageProps} />
              )}
            </Layout>
          </MediaProvider>
        </AIProvider>
      </AuthProvider>
    </>
  )
}

export default MyApp