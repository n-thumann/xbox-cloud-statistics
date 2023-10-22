import { resolve } from "path";
import { defineNuxtModule } from "@nuxt/kit";

// Adapted from https://content.nuxt.com/recipes/transformers
export default defineNuxtModule({
  setup(_options, nuxt) {
    nuxt.hook("content:context", (contentContext) => {
      contentContext.transformers.push(
        resolve("./modules/body-content/transformer.ts"),
      );
    });
  },
});
