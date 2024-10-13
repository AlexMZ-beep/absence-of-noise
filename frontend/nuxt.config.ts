// https://nuxt.com/docs/api/configuration/nuxt-config
export default defineNuxtConfig({
  devtools: { enabled: false },
  ssr: false,
  modules: [
    '@nuxtjs/tailwindcss',
    '@nuxtjs/eslint-module',
    'nuxt-quasar-ui',
    'nuxt-mdi',
  ],
  quasar: {
    plugins: [
      'Notify',
      'Loading',
    ],
    lang: 'ru',

    config: {
      brand: {
        primary: '#ef3025',
        secondary: '#7b8ba9',
      },
    },
  },
  app: {
    head: {
      link: [
        { rel: 'icon', href: '/rzd_icon.png' },
      ],
      title: 'Поддержка сотрудников РЖД',
    },
  },
  css: ['@/public/style/main.css', '@/public/style/font.css'],
  runtimeConfig: {
    public: {
      baseURL: process.env.NUXT_API_URL,
      headers: {},
    },
  },

});
