## REFORMULACION

Propósito: que los textos que acompañan a `EdgeIndex.stale` dejen de mandar a reconstruir y nombren `sldb stores update` (API `update_store_indexes`) como la operación que resuelve un documento editado fuera de sldb. Resultado: descripción del campo `stale` en `src/sldb/store/edge_index/edge_index.py`, docstring de `load_edge_index`, alerta `edges/stale` de la CLI, un test nuevo en `tests/api/test_api_edges.py` (edición manual → stale → `rebuild_edges` no lo saca → `update_store_indexes` sí) y una línea de CHANGELOG. Repo: sldb. Límites: no se toca `rebuild_edges` ni el stale por documento en graph_ui; `tests/api/test_composition_edges.py` solo como regresión; commit y aviso los hace el coordinador.

## AMBIGUEDADES

1. "alert(\"edges/stale\", s, \"tracked file changed since its shard was built\", \"sldb stores update\")" frente a la descripción que lista shard ausente, otro `hash_c`, otra `EDGE_INDEX_VERSION` y otra `contract_signature`: el mensaje nuevo describiría mal las demás causas; obligaría a inventar si se parten en varias alertas.
2. "Del grep solo se cambian los mensajes cuyo texto habla de stale o de documentos editados fuera de sldb": criterio interpretable; obligaría a inventar qué mensajes califican y dónde buscar si `docs/` no existe.
3. "un test prueba que después de stores update el documento editado sale de stale": ya existe `test_a_hand_edit_reaches_the_index_through_stores_update`, que no afirma el stale previo; obligaría a inventar si se amplía o se añade otro.
4. La entrada de CHANGELOG bajo `"## 0.1.13 — not released yet"`: si ese encabezado no existe, obligaría a inventar su lugar.

## DRY-RUN

Lecturas: los seis archivos del `files`, más `src/sldb/api/edges/rebuild_edges.py` (citado, no listado) para confirmar la docstring existente. Cambios previstos: tres textos, un test nuevo con `EdgeWorld`/`world`, una línea de CHANGELOG. Dependencias: `update_store_indexes` rehasha el archivo editado; fixtures actuales de `test_api_edges.py`. Validaciones futuras: los dos `pytest -q` con `TMPDIR=/dev/shm`, `grep -rn "edges rebuild"`, y que el test falle antes del cambio de textos si depende de ellos.

## FUTURO

El coordinador ejecuta `deskops closeout commit` y `deskops message send --to graph_ui`; si el test muestra que `update_store_indexes` tampoco saca el documento de stale, el ejecutor detiene la tarea y reporta; `deskops closeout verify` valida tests, commit y árbol limpio.
