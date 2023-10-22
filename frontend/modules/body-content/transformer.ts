// @ts-ignore: Broken for whatever reason
import { defineTransformer } from "@nuxt/content/transformers";

export default defineTransformer({
  name: "body-transformer",
  extensions: [".json"],
  parse: (_id: string, content: any) => {
    return {
      body: content,
      path: _id.split(":"),
      _id,
    };
  },
});
