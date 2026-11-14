import { defineConfig } from "vitest/config";
import react from "@vitejs/plugin-react";

// En desarrollo, /sldb se redirige al `sldb serve` (o al servidor de referencia).
const target = process.env.SLDB_TARGET ?? "http://127.0.0.1:8787";

export default defineConfig({
  plugins: [react()],
  // Dos entradas: la superficie genérica (index.html) y la maqueta de átomos (maqueta.html).
  build: { rollupOptions: { input: { main: "index.html", maqueta: "maqueta.html" } } },
  server: {
    proxy: {
      "/sldb": { target, changeOrigin: true, rewrite: (path) => path.replace(/^\/sldb/, "") },
    },
  },
  test: {
    environment: "jsdom",
    globals: true,
    setupFiles: ["./src/test-setup.ts"],
  },
});
