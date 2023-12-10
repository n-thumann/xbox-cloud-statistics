// @ts-ignore: Broken for whatever reason
import { defineTransformer } from "@nuxt/content/transformers";

export default defineTransformer({
  name: "body-transformer",
  extensions: [".json"],
  parse: (_id: string, content: any) => {
    const path = _id.split(":");
    return {
      title: path[path.length - 1].slice(0, -5),
      body: content,
      path,
      _id,
    };
  },
});
