## REFORMULACION

Propósito: corregir en el repo SLDB_1 (`src/sldb/api/edges/`) la API de referrers y reescritura de referencias para que acepte un grafo armado en proceso, excluya fuentes indicadas y no duplique menciones del frontmatter. Resultado: `referrers(store, target, graph=g)` y `rewrite_references(..., graph=g, excluded_sources=[...])` keyword-only, con `optional_graph` como fallback; `find_hits` sin duplicar un campo schema como mention; tests nuevos en `tests/api/test_referrers.py` y `tests/api/test_rewrite_references.py`; `CHANGELOG.md`. Límites: no tocar deskops, no declarar `project_graph` en su `store.yaml`, no cambiar el formato de `Referrer`, y conservar el comportamiento actual sin los parámetros nuevos.

## AMBIGUEDADES

1. “fuentes nombradas por ruta trackeada o export id Model:name”: no se define normalización, prioridad ni comparación entre ambas formas; obligaría a inventar el parser y las reglas de matching.
2. “cuya línea cae dentro del frontmatter de ese documento”: no se definen delimitadores ni convención de líneas del frontmatter; obligaría a inventar cómo calcular ese rango.
3. “graph: ProjectGraph | None = None”: no se indica módulo de importación de `ProjectGraph`; obligaría a inventar la ruta de importación.
4. “una fuente excluida queda byte a byte igual”: no se aclara si la ruta se resuelve respecto al store, al cwd o al archivo; obligaría a inventar la resolución.
5. “CHANGELOG, commit y aviso”: no se especifica formato del commit ni entrada del CHANGELOG; obligaría a inventar la convención.

## DRY-RUN

Lecturas: `referrers.py`, `rewrite_references.py`, ambos tests, `CHANGELOG.md` y la nota de inbox. Cambios previstos: añadir parámetros keyword-only; pasar `graph` a `find_hits`; filtrar campos y menciones por `excluded_sources`; deduplicar mentions frontmatter; agregar casos H-a, H-b y H-c; actualizar CHANGELOG. Dependencias: tipo `ProjectGraph`, helpers de store/rutas y fixtures `tmp_path`. Validaciones futuras: `TMPDIR=/dev/shm pytest -q tests/api/test_referrers.py` y `TMPDIR=/dev/shm pytest -q tests/api/test_rewrite_references.py`. Sin ejecutar nada.

## FUTURO

Deskops decide y declara su `project_graph` y recibe el aviso al cierre; otro nodo o un humano ejecuta tests/commit y acepta el resultado. No son ambigüedades del encargo.
