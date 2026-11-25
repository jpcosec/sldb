## REFORMULACION

**Propósito:** que `graph_path` y `graph_paths` de `sldb.api.graph` devuelvan caminos explicados con la procedencia de cada tramo, sin romper la forma actual. **Resultado:** `path_steps.py` con `explain_path`; operaciones `path_explained`/`paths_explained` en `GraphBackend`/networkx; `explain: bool = False` en la API; `--explain` en CLI; `?explain=1` en serve; tests, CHANGELOG y aviso a IR. **Repo:** `/mnt/ssd/proyectos/SLDB_1`, paquete `src/sldb`. **Límites:** no cambiar `path`/`paths` ni goldens; procedencia desde metadata de `EdgeRecord`; mantener compatibilidad CLI/API.

## AMBIGUEDADES

1. “la impresión va a un módulo nuevo” (Implementation Path 4): no fija nombre, ruta ni API de ese módulo; obligaría a inventar su ubicación y firma.
2. “CHANGELOG y commit; aviso a IR anotado en result-summary.md” (Done When): no define mensaje de commit, formato del CHANGELOG ni canal/plazo del aviso; obligaría a inventarlos.
3. “provenance = {origin, relation_doc o field, from_store}” y “evidence no entra en provenance”: no aclara si `evidence` se descarta del tramo o se conserva en otro campo; obligaría a decidir su destino.
4. “ordenadas por precedencia relation_doc > schema > structural > alias”: no cubre empates dentro de la misma clase ni tipos desconocidos; obligaría a inventar desempate.

## DRY-RUN

**Lecturas:** `analyze.py`, `networkx_backend.py`, parsers/commands de `graph_analysis`, `graph_routes.py`, tests citados, goldens y CHANGELOG. **Cambios previstos:** crear `path_steps.py`; registrar operaciones; añadir `explain` en API/CLI/serve; tests; CHANGELOG. **Dependencias:** protocolo `GraphBackend`, `analysis.relations.resolve`, `EdgeRecord.metadata`, `AnalysisWorld`. **Validaciones futuras:** los seis comandos de Validation y comparación de goldens. Sin ejecutar.

## FUTURO

Un humano aprueba nombres/rutas del módulo de impresión y el texto de CHANGELOG/commit; otro nodo ejecuta la implementación y las validaciones; IR recibe y acepta el aviso. No son ambigüedades del encargo.
