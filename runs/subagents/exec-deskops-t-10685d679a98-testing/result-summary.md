PASA

# Testing H11b — caché de disco de filas de documentos y costo del import

Commit verificado: `d3568eea674b1e89a758c4a755ea168b343e3a5a` (`select_documents: caché de disco de las filas de documentos; networkx perezoso; store.yaml con libyaml (H11b)`), HEAD del checkout al momento del testing.

## Veredicto

El trabajo pasa los tests del commit, los tests de los módulos tocados, `tests/test_clean_code_rules.py` y `tools/check.sh --fast` (rc 0). No encontré una regresión funcional en la caché de filas, en la invalidación ni en los imports perezosos.

## Tests ejecutados

Uno por archivo, con `TMPDIR=/tmp`, `/tmp/ws-venv` en `PATH`:

- `tests/api/test_select_documents_disk.py`: 6 passed (archivo nuevo del commit).
- Núcleo del cambio: `test_select_documents.py` 19, `test_views.py` 17, `test_views_linked.py` 7, `test_run_view_reads.py` 6, `test_guard_views.py` 2.
- Stores/declaración: `test_api_stores.py` 14, `test_store_init_failures.py` 3, `test_declare_store_authored.py` 1.
- Grafo/semántica: `test_graph_analysis.py` 16, `test_graph_backend.py` 9, `test_semantic_dag_walk.py` 8, `test_semantic_export.py` 4, `test_semantic_rebuild.py` 10, `test_api_semantic.py` 8, `test_api_graph_analysis.py` 10.
- Superficie relacionada: `test_project_graph_config.py` 11, `test_replace_text.py` 16, `test_scaffold_store.py` 20, `test_tags.py` 37, `test_tags_scope.py` 11, `test_include_resolution.py` 5, `test_stores_build.py` 35, `test_composition_edges.py` 7, `test_composition.py` 4.
- `tests/test_clean_code_rules.py`: 1214 passed.

No se ejecutó la suite completa, según la instrucción del rol de testing; la corre el host.

## Gate rápido

    PATH=/tmp/ws-venv/bin:$PATH bash tools/check.sh --fast   -> rc 0
    TODAS LAS PUERTAS PASAN (núcleo aislado, capas, identidad, ejes y superficie)

## Benchmark

Repetí el benchmark del ejecutor (`bench-run-board.sh`) sobre el layout H11 de `/dev/shm/h11b` con el `src` actual: `sldb views run board`, store construido, proceso nuevo, mediana de 5 = **1,43 s** (1,4135/1,4313/1,4207/1,4285/1,4264; load average 1,08/1,40/2,19). Coincide con el 1,44 s informado. La meta de <1 s no se alcanza; el informe del ejecutor y `docs/architecture/views.md` cuantifican lo que falta (import de modelos pydantic, JSON del índice compuesto y `live_stale`) y la tarea admite esa explicación con medición.

## Nota de entorno

`tests/mcp/*` no se pudieron correr en este venv por faltar el extra `mcp` (`ModuleNotFoundError: anyio`). No son archivos del commit; el informe del ejecutor dice haberlos verificado tras `pip install -e '.[mcp]'`.

## Evidencia revisada

- La caché es JSON en `.sldb_cache/document_rows/`, con clave de stats (índice del store, índice y roster hash de cada modelo, stat de los directorios de shards y versión del índice) y lectura de shards como fallback ante cualquier diferencia o corrupción.
- El test nuevo cubre mismo resultado/revisión con y sin caché, invalidación al trackear un documento, caché corrupta/de otra versión ignorada y que la vista lee la caché sin volver a los shards.
- `networkx` pasó a import perezoso y `load_declaration` usa `CSafeLoader`; los tests de grafo, semántica y stores mantienen el comportamiento.
