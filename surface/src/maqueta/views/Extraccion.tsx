import type { ViewProps } from "../ViewProps";

/** Vista Extraccion de la maqueta (provisional: la reemplaza su port). */
export default function Extraccion({ acta }: ViewProps) {
  return <div className="mq-state">Extraccion · {acta.id}</div>;
}
