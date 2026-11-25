REFORMULACION
Nodo ejecutable (`task.code`), no agregado. Propósito: que `graph_path`/`graph_paths` expliquen cada tramo con procedencia. Resultado: `explain=True` devuelve `{"path", "steps"}` o lista de dicts; sin `explain`, forma actual intacta. Repo: sldb (`src/sldb/api/graph`, `store/graph`, `cli`, `cli/serve`, tests, CHANGELOG). Límites: no romper goldens; no incluir `evidence`; solo las superficies listadas; precedencia `relation_doc > schema > structural > alias`.

AMBIGUEDADES
1. “provenance = {origin, relation_doc o field, from_store} tomado de EdgeRecord.metadata”: no define qué claves de metadata producen cada `origin` ni cómo distinguir `structural`/`alias`. Obligaría a inventar el mapeo.
2. “from_store (solo si viene de un store enlazado)”: no indica cómo detectarlo en la arista. Obligaría a inventar la marca.
3. “Empates dentro de la misma clase de precedencia: orden alfabético por relation y luego por relation_doc o field”: no cubre empate total ni dirección. Obligaría a inventar desempate.
4. “una arista espejo con metadata.reverse true no se lista aparte”: no dice qué ocurre si existen ambas aristas. Obligaría a inventar deduplicación.
5. “La impresión de --explain va a un módulo nuevo graph_path_print.py”: no fija formato de salida. Obligaría a inventar formato.
6. La lista `files:` omite `tests/store/test_graph_analysis.py`, `tests/store/test_graph_backend.py` y `result-summary.md`, pero Validation y Done When los exigen. Obligaría a inventar si se crean o modifican.
7. “graph_paths una lista de esos dicts”: `graph_paths` no recibe `directed`; no dice cómo explicar rutas no dirigidas ni si `--explain --directed` aplica. Obligaría a inventar semántica.
8. “?explain=1”: no define el parser booleano. Obligaría a inventar aceptación de valores.

DRY-RUN
Lecturas: `analyze.py`, `networkx_backend.py`, `EdgeRecord`/índice, `parsers/graph_analysis.py`, `commands/graph_analysis.py`, `serve/graph_routes.py`, tests y goldens. Cambios: nuevo `path_steps.py`; registrar `path_explained`/`paths_explained`; añadir `explain`; `--explain` y `graph_path_print.py`; `?explain=1`; tests; CHANGELOG. Dependencias: `resolve`, `path_between`, `paths_between`, metadata de aristas. Validaciones futuras: los seis comandos de Validation y goldens.

FUTURO
JP/IR deciden formato y precedencia; otro nodo implementa; un humano valida commit y closeout.
