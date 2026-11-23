/**
 * El rechazo de SLDB al guardar, para leerlo: un título en palabras y debajo qué pasó y qué
 * hacer, en español (`core/rechazo` lo lee de la respuesta; aquí no se valida nada). El texto
 * del servidor queda como detalle cuando no se reconoce el rechazo y siempre en la lente Fierros.
 */
import React from "react";
import { leerRechazo } from "../core/rechazo";
import { rotulo } from "./Ficha";

export const AvisoGuardado: React.FC<{
  titulo: string;
  /** El mensaje tal como lo entregó SLDB. */
  mensaje: string;
  /** Código HTTP de la respuesta, si la hubo. */
  status?: number;
  /** La descripción que el tipo da de un field, para explicar el formato que espera. */
  ayuda?: (campo: string) => string | undefined;
  /** Lente Fierros: el texto del servidor va siempre a la vista. */
  fierros?: boolean;
  testId?: string;
  onDismiss?: () => void;
}> = ({ titulo, mensaje, status, ayuda, fierros = false, testId = "prosa-save-error", onDismiss }) => {
  const rechazo = leerRechazo(mensaje, { status, rotulo, ayuda });
  return (
    <div role="alert" className="wb-aviso" data-testid={testId}>
      <strong className="wb-aviso__titulo">{titulo}</strong>
      {rechazo.lineas.length === 1 ? (
        <span className="wb-aviso__mensaje">{rechazo.lineas[0]!.texto}</span>
      ) : (
        <ul className="wb-aviso__mensaje wb-aviso__lista">
          {rechazo.lineas.map((linea, i) => (
            <li key={i}>{linea.texto}</li>
          ))}
        </ul>
      )}
      {(fierros || !rechazo.reconocido) && (
        <details className="wb-aviso__detalle" open={fierros} data-testid={`${testId}-original`}>
          <summary>Detalle técnico</summary>
          <pre className="wb-aviso__original">{rechazo.original}</pre>
        </details>
      )}
      {onDismiss && (
        <button type="button" className="wb-aviso__cerrar" aria-label="Cerrar el aviso" onClick={onDismiss}>
          ×
        </button>
      )}
    </div>
  );
};
