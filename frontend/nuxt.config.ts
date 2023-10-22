import { resolve } from "path";

export default defineNuxtConfig({
  modules: [
    "./modules/body-content",
    "@nuxt/content",
    "@nuxtjs/google-fonts",
    "@nuxtjs/tailwindcss",
  ],
  // Disable payloadExtraction, because otherwise the measurements will be
  // stored in _payload.json files and indefinetly cached by the browser.
  // This can be removed / enabled again, as soon as Nuxt adds e.g. a hash
  // to the payload files (see https://github.com/nuxt/nuxt/issues/15427).
  experimental: {
    payloadExtraction: false,
  },
  content: {
    sources: {
      content: {
        driver: "fs",
        base: resolve(__dirname, "results"),
      },
    },
  },
  nitro: {
    preset: "github-pages",
  },
  app: {
    baseURL:
      process.env.NODE_ENV === "production" ? "/xbox-cloud-statistics/" : "",
  },
  tailwindcss: {
    exposeConfig: true,
  },
  googleFonts: {
    families: {
      Roboto: [400, 700],
    },
  },
  typescript: {
    typeCheck: true,
  },
});
