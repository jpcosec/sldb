REFORMULACION
GO03 es un nodo ejecutable (`kind: code`, `node_role: delivery`), no agregado, del repo sldb. Encargo: definir el protocolo `GraphBackend` (`load`, `eval`, `analyze`) y una implementación networkx que envuelva el índice compuesto y el análisis de grafo actuales. Resultado: seis comandos `graph` y `api/graph` enrutados por `analyze` sin cambiar salidas; `eval` limitado al subconjunto de GO02 sin caminos; selección por `graph_backend` en `store.yaml` con `["networkx"]`; documentación, pruebas y CHANGELOG. Límites: no cambia comportamiento observable, no expone el grafo interno, no implementa caminos (`NotImplementedError`), no produce la proyección (GO04) ni evalúa caminos (GO05), y no admite otros motores.

AMBIGUEDADES
1. "Proyección = mapa export_id → facet payload o None; GO03 acepta el argumento y no lo usa" contradice "eval ... evaluado sobre la facet del sujeto si hay proyección o sobre el payload pasado". Obliga a inventar si `load` debe conservar la proyección para `eval`, y qué prevalece cuando hay proyección y payload.

DRY-RUN
Un ejecutor futuro leería GO02 (`rules-language.md`) para la firma y el subconjunto de `eval`, el índice compuesto actual (`compose.py`), `api/graph`, `cli/parsers/graph_analysis.py`, la carga de `store.yaml`, goldens y tests existentes, y la evidencia de G_BOUNDARY. Cambiaría/crearía `src/sldb/store/graph/backend*`, adaptaría `api/graph` y los seis comandos a `analyze`, añadiría validación de `graph_backend`, documentaría `docs/architecture/graph-backend.md`, y añadiría tests espía, de configuración, de `eval` y CHANGELOG. Depende de GO02 y G_BOUNDARY; produce G_SEAM. Validaría con pytest: goldens idénticos, tests de `api/graph` sin cambios, backend espía, índice del propio repo, `has(id) and status != "x"`, camino con `NotImplementedError`, ausencia/valor inválido de `graph_backend`, documentación y CHANGELOG.

FUTURO
GO04 producirá la proyección que GO03 solo acepta; GO05 consumirá la costura y habilitará caminos. La revisión en frío aceptada y la disposición del operador del desk resolverán G_SEAM; D5 ya está confirmada. No hay ejecución autorizada.
