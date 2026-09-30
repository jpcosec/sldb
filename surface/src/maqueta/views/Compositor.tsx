import type { ViewProps } from "../ViewProps";

/** Vista Compositor de la maqueta (provisional: la reemplaza su port). */
export default function Compositor({ acta }: ViewProps) {
  return <div className="mq-state">Compositor · {acta.id}</div>;
}
