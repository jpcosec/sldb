## REFORMULACION
Propósito: introducir en sldb la costura `GraphBackend` con `load(índice compuesto, proyección)` y `eval(regla o predicado, sujeto opcional) → findings`, más una implementación networkx que envuelva compose y el análisis de grafo existente sin alterar salidas. Documentar el protocolo y la selección por `store.yaml` (default networkx). Resultado: backend, doc y `G_SEAM`. Repo dueño: sldb. Límites: solo `src/sldb/store/graph/backend*` y `docs/architecture/graph-backend.md`; depende de GO01/`G_BOUNDARY`; no cambia salidas; D5 queda pendiente de confirmación del dueño.

## AMBIGUEDADES
1. «eval(regla o predicado, sujeto opcional) → findings»: no se define la representación de entrada ni la forma de `findings`. GO02 es hermano sin arista y no transfiere contrato. Obligaría a inventar la API de predicado/regla y los campos del resultado; además, la aceptación no prueba `eval`.
2. «Selección del backend por store.yaml con default networkx»: no se especifica clave, esquema ni comportamiento ante valor ausente o inválido. Obligaría a inventar el contrato de configuración; la aceptación tampoco lo verifica.
3. «Implementación networkx que envuelve lo que hoy hace compose + graph analysis» frente a un `output_scope` limitado a `backend*`: no queda claro si los comandos `graph` deben enrutarse por la costura —tocando módulos fuera del scope— o si basta probarla aislada. Obligaría a decidir el alcance de la integración.

## DRY-RUN
Lecturas: `dag.yaml`, brief, alcance, decisiones, `compose.py`, comandos `graph`, `store.yaml` y goldens. Cambios previstos: protocolo y backend networkx, documento de arquitectura y, si se confirma, lectura de configuración. Dependencias: GO01 ejecutado/`G_BOUNDARY`; confirmación de D5; sin contrato de GO02 para `eval`. Validaciones futuras: goldens de `path/cycles/order/components/central/similar`, test que carga el índice compuesto del propio repo y revisión del doc. `eval` y selección solo tendrían validación si se añaden criterios. Sin ejecutar.

## FUTURO
El dueño confirma D5; la revisión en frío acepta GO03 y resuelve `G_SEAM`; GO04 consume la costura; la implementación del lenguaje (GO02 y posteriores) provee el `eval` real.
