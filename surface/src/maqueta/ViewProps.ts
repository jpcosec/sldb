import type { Acta } from "../core/contract";
import type { AtomStore } from "../views/atoms/useAtomStore";
import type { MaquetaTab } from "./tabs";

/** Lo que la raíz le da a cada vista de la maqueta. */
export interface ViewProps {
  store: AtomStore;
  /** Documento de trabajo (el acta de la que salen los átomos). */
  acta: Acta;
  /** Átomo enfocado, compartido entre las tres vistas. */
  focusId: string | null;
  setFocusId(id: string | null): void;
  /** Cambia de pestaña, opcionalmente enfocando un átomo (la maqueta: "Ver en el texto", "Origen"). */
  go(tab: MaquetaTab, atomId?: string | null): void;
}
