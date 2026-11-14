import { defineConfig } from "vitest/config";
import react from "@vitejs/plugin-react";

// En desarrollo, /sldb se redirige al `sldb serve` y /desk a la vista HTTP de deskops.
const sldbTarget = process.env.SLDB_TARGET ?? "http://127.0.0.1:8085";
const deskTarget = process.env.DESK_TARGET ?? "http://127.0.0.1:8091";

export default defineConfig({
  plugins: [react()],
  build: { rollupOptions: { input: { main: "index.html" } } },
  server: {
    proxy: {
      "/sldb": { target: sldbTarget, changeOrigin: true, rewrite: (path) => path.replace(/^\/sldb/, "") },
      "/desk": { target: deskTarget, changeOrigin: true, rewrite: (path) => path.replace(/^\/desk/, "") },
    },
  },
  test: {
    environment: "jsdom",
    globals: true,
    setupFiles: ["./src/test-setup.ts"],
  },
});
