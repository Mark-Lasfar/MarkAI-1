/** @type {import('next').NextConfig} */
const nextConfig = {
  reactStrictMode: true,
  
  // Internationalization settings
  i18n: {
    locales: ['en', 'ar'],
    defaultLocale: 'ar',
    localeDetection: false,
  },

  // API proxy configuration
  async rewrites() {
    return [
      {
        source: '/api/:path*',
        destination: `${
          process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000'
        }/api/:path*`,
      },
      {
        source: '/docs',
        destination: `${
          process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000'
        }/docs`,
      },
      {
        source: '/openapi.json',
        destination: `${
          process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000'
        }/openapi.json`,
      }
    ];
  },

  // Production settings
  output: 'standalone',
  productionBrowserSourceMaps: false,
  compress: true,
  poweredByHeader: false,
  
  // Image optimization
  images: {
    domains: ['localhost', 'markai.example.com'],
  },

  // Security headers
  async headers() {
    return [
      {
        source: '/(.*)',
        headers: [
          {
            key: 'X-Frame-Options',
            value: 'DENY',
          },
          {
            key: 'X-Content-Type-Options',
            value: 'nosniff',
          },
          {
            key: 'Referrer-Policy',
            value: 'strict-origin-when-cross-origin',
          }
        ],
      },
    ];
  }
};

module.exports = nextConfig;