## REFORMULACION

Propósito: producir un plan (drawer) que reúna la reversión de D5 —motor Datalog dueño de aristas— y el daemon residente de sldb, con prueba de concepto medida y decisiones para JP. Resultado: `desk/drawer/plans/grafo-datalog-daemon/` con alcance, brief, decisiones y `dag.yaml`; D5 revertida en `grafo-operable/decisiones.md`; informe con tabla de tiempos/memoria; una `task.decision` por decisión abierta. Repo: sldb. Límites: no cambiar `GraphBackend` ni código de producción; la prueba vive fuera de producción; no reemplaza ni bloquea la tarea previa de live/stale.

Es un encargo de planificación/documentación, no ejecutable de producto. No declara átomos ni hijos; genera propuestas y `task.decision`.

## AMBIGUEDADES

1. “Datalevin u otro con cliente Python”: no fija candidatos ni criterio de elección; obligaría a inventar el conjunto comparado y el desempate.
2. “mide aristas de un nodo, recorrido, emparejamiento de atomos y stale”: no define dataset, escala ni umbral; obligaría a inventar el banco y el criterio de aceptación.
3. “consumo de memoria en robocop2 con el tope de 8 GB libres”: no describe robocop2 ni el método de medición; obligaría a inventar entorno y procedimiento.
4. “scripts en reports/ o en el plan”: alternativa sin criterio; obligaría a elegir e inventar ruta.
5. “con alcance, brief, decisiones y dag.yaml”: no hay esquema ni plantilla en el input; obligaría a inventar estructura y campos.
6. “sin faltantes nuevos”: no incluye baseline; obligaría a inventar el estado de referencia.

## DRY-RUN

Un ejecutor futuro leería `docs/architecture/graph-backend.md`, `desk/drawer/plans/grafo-operable/`, `GraphBackend`, compose, `edge_index`, las notas de inbox, el Board y los rituales. Cambios previstos: crear el plan y sus archivos, editar `decisiones.md`, crear `task.decision`, y dejar scripts/informe de la PoC. Dependencias: la tarea previa de live/stale, un motor con cliente Python disponible, acceso a robocop2 y 8 GB libres. Validaciones futuras: repetir la PoC con el comando documentado, `deskops graph missing --root .` sin faltantes nuevos, `deskops review node` leyendo `dag.yaml`, D5 con fecha/motivo y una decisión por tema. Sin hijos declarados, el resultado conjunto se valida por esos artefactos.

## FUTURO

JP decide motor, forma del daemon e invalidación. Tasks posteriores implementan `GraphBackend`/daemon; la tarea previa entrega live/stale. No son ambigüedades.
