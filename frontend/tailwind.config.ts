import type { Config } from "tailwindcss";

export default <Partial<Config>>{
  content: [
    "./components/**/*.{js,vue,ts}",
    "./layouts/**/*.vue",
    "./pages/**/*.vue",
    "./plugins/**/*.{js,ts}",
    "./nuxt.config.{js,ts}",
    "./app.vue",
  ],
  theme: {
    extend: {
      fontFamily: {
        roboto: ["Roboto", "sans-serif"],
      },
      colors: {
        green: "#24d292",
        purple: "#d558c8",
      },
      backgroundImage: {
        xbox: "linear-gradient(-20deg, #d558c8 0%, #24d292 100%)",
      },
    },
  },
};
