## REFORMULACION

Nodo ejecutable (`task.code`), no agregado. **Propósito:** que `graph_path` y `graph_paths` de SLDB puedan devolver caminos explicados, indicando por qué arista se recorre cada tramo y su procedencia, sin romper la salida actual. **Resultado:** con `explain=True`, `graph_path` devuelve `{"path": [...], "steps": [...]}` y `graph_paths` una lista de esos dicts; cada step contiene `source`, `target` y `edges`, y cada edge `relation`, `direction` y `provenance` según las precisiones. Con `explain=False` no cambia la forma. Debe exponerse por API, CLI (`--explain`) y serve (`?explain=1`). **Repo:** `/mnt/ssd/proyectos/SLDB_1`. **Límites:** no cambiar las operaciones `path`/`paths`, preservar goldens, pasar por `GraphBackend`, ordenar aristas por precedencia y documentar el criterio cuando haya varias.

## AMBIGUEDADES

1. “provenance = {origin, relation_doc o field, from_store} tomado de EdgeRecord.metadata”: no se especifican las claves exactas de `metadata` ni el fallback si faltan. Obligaría a inventar el mapeo.
2. “Un origin desconocido va al final”: no define el orden entre varios desconocidos. Obligaría a inventar un desempate.
3. “una arista espejo con metadata.reverse true no se lista aparte”: no aclara qué ocurre si coexisten arista directa y espejo. Obligaría a inventar la deduplicación.
4. “(70 líneas: la impresión va a un módulo nuevo)”: no queda claro si “70 líneas” es límite, estimación o criterio de extracción. Obligaría a inventar una restricción de tamaño.
5. “aviso a IR anotado en result-summary.md”: no indica ruta ni formato esperado. Obligaría a inventar ubicación y plantilla.

## DRY-RUN

**Lecturas:** los siete archivos de `files`, tests de graph analysis/backend/serve, goldens y `tools/check.sh`. **Cambios previstos:** crear `sldb/store/graph/analysis/path_steps.py`; registrar `path_explained`/`paths_explained` en `networkx_backend.py`; añadir `explain` en `api/graph/analyze.py`; parser y comando CLI; nuevo `graph_path_print.py`; ruta serve; tests y CHANGELOG. **Dependencias:** `path_between`, `paths_between`, `edges_from`/`edges_to`, `analysis.relations.resolve`, `EdgeRecord.metadata`. **Validaciones futuras:** ejecutar los seis comandos de Validation y comprobar que los goldens permanecen intactos.

## FUTURO

El ejecutor producirá código, tests, CHANGELOG y `result-summary.md`; un humano o nodo posterior hará commit y revisará el aviso a IR.
