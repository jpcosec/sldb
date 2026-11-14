import type { Acta, Fuente, Informe, Respuesta } from "../core/contract";
import type { AtomStore } from "../views/atoms/useAtomStore";
import type { MaquetaTab } from "./tabs";

/** Lo que la raíz le da a cada vista de la maqueta. */
export interface ViewProps {
  store: AtomStore;
  /** Documento de trabajo (el acta de la que salen los átomos). */
  acta: Acta;
  /** TODAS las fuentes de texto del caso (system prompt, folleto, mensaje…; en el store viejo, el acta). */
  fuentes: Fuente[];
  /** Informe del caso (slots persistidos): el Compositor lo edita y la Respuesta lo lee. */
  informe: Informe | undefined;
  /** Respuesta del asistente al caso, si el store la tiene. */
  respuesta: Respuesta | undefined;
  /** Cabecera `sldb / <proyecto> / <caso>`; `null` en el store viejo (`sldb / actas / <archivo>`). */
  caso: { proyecto: string; caso: string } | null;
  /** Átomo enfocado, compartido entre las tres vistas. */
  focusId: string | null;
  setFocusId(id: string | null): void;
  /** Cambia de pestaña, opcionalmente enfocando un átomo (la maqueta: "Ver en el texto", "Origen"). */
  go(tab: MaquetaTab, atomId?: string | null): void;
}
