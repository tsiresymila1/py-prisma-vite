import { defineConfig } from "vite";
import vue from "@vitejs/plugin-vue";
import ViteStarlitePlugin from "./vite-starlite-plugin";
import eslint from 'vite-plugin-eslint';
export default defineConfig({
  plugins: [
    vue(),
    ViteStarlitePlugin({
      apiServer: "http://locahost:8000",
      entry: "main.ts"
    }),
    eslint()
  ],
});
