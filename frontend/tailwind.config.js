/** @type {import('tailwindcss').Config} */
export default {
  prefix: 'tw-',
  content: [
    './pages/**/*.{vue}',
    './components/**/*.{vue}',
  ],
  theme: {
    extend: {
      colors: {
        primary: '#ef3025',
        secondary: '#7b8ba9',
      },
    },
    screens: {
      desktop: '1440px',
      laptop: '1000px',
      tablet: '640px',
      mobile: '320px',
    },
  },
  plugins: [],
};
