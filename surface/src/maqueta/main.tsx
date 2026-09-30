import { StrictMode } from "react";
import { createRoot } from "react-dom/client";
import { createHttpClient } from "../core/client";
import { SldbProvider } from "../react/context";
import { MaquetaApp } from "./MaquetaApp";
import "./maqueta.css";
import "./maqueta-extra.css";

const client = createHttpClient(import.meta.env.VITE_SLDB_URL ?? "/sldb");

createRoot(document.getElementById("root") as HTMLElement).render(
  <StrictMode>
    <SldbProvider client={client}>
      <MaquetaApp />
    </SldbProvider>
  </StrictMode>,
);
