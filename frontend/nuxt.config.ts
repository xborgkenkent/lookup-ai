import tailwindcss from "@tailwindcss/vite"

// https://nuxt.com/docs/api/configuration/nuxt-config
export default defineNuxtConfig({
  compatibilityDate: '2024-11-01',
  // devtools: { enabled: true },
  css: ['~/assets/css/main.css'],
  modules: ['@nuxt/scripts'],
  vite: {
    plugins: [
      tailwindcss(),
    ],
  },
  devServer: {
    host: '127.0.0.1'
  },
  runtimeConfig: {
    public: {
      baseUrl: ''
    }
  }
})