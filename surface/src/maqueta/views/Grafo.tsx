import type { ViewProps } from "../ViewProps";

/** Vista Grafo de la maqueta (provisional: la reemplaza su port). */
export default function Grafo({ acta }: ViewProps) {
  return <div className="mq-state">Grafo · {acta.id}</div>;
}
