import { defineConfig } from "vite";
import react from "@vitejs/plugin-react";

export default defineConfig({
  plugins: [react()],
  server: {
    port: 5173,
    proxy: {
      // Forward API requests to backend server
      "/api": {
        target: "http://localhost:5001",
        changeOrigin: true,
        secure: false,
        // Rewrite if your backend doesn’t expect /api prefix
        // rewrite: (path) => path.replace(/^\/api/, "")
      }
    }
  }
});
