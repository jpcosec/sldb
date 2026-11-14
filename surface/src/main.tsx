import { StrictMode } from "react";
import { createRoot } from "react-dom/client";
import { createHttpClient } from "./core/client";
import { SldbProvider } from "./react/context";
import { initTheme } from "./core/theme";
import { App } from "./views/App";
import "./styles/app.css";

// Antes del primer render: evita el parpadeo claro al recargar con tema oscuro.
initTheme();

const client = createHttpClient(import.meta.env.VITE_SLDB_URL ?? "/sldb");

createRoot(document.getElementById("root") as HTMLElement).render(
  <StrictMode>
    <SldbProvider client={client}>
      <App />
    </SldbProvider>
  </StrictMode>,
);
