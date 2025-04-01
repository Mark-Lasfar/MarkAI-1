// frontend/tailwind.config.js
module.exports = {
  content: [
    "./pages/**/*.{js,ts,jsx,tsx}",
    "./components/**/*.{js,ts,jsx,tsx}",
    "./app/**/*.{js,ts,jsx,tsx}", // إذا كنت تستخدم Next.js 13+ مع App Router
  ],
  theme: {
    extend: {
      fontFamily: {
        arabic: ['Tajawal', 'sans-serif'],
        english: ['Inter', 'sans-serif'],
      },
      colors: {
        primary: {
          light: '#4f9eff',
          DEFAULT: '#2563eb',
          dark: '#1e40af',
        },
        secondary: {
          light: '#f59e0b',
          DEFAULT: '#d97706',
          dark: '#b45309',
        },
      },
      textAlign: {
        'right': 'right', // مهم للغة العربية
      },
      direction: {
        'rtl': 'rtl', // إضافة دعم للاتجاه من اليمين لليسار
      },
    },
  },
  plugins: [
    require('@tailwindcss/forms'), // إذا كنت تستخدم عناصر Forms
    require('@tailwindcss/typography'), // إذا كنت تحتاج تحكم أفضل في النصوص
  ],
  corePlugins: {
    textAlign: true, // تأكيد تفعيل محاذاة النص
  },
}