## REFORMULACION

Encargo ejecutable (`task.code`, nodo ritual-execution): corregir tres textos que hoy mandan a reconstruir cuando el índice está stale por edición externa —descripción del campo `stale` en `edge_index.py`, docstring de `load_edge_index` en `edge_reading.py` y alerta `edges/stale` en `commands/edges.py`— para que nombren `sldb stores update` (API `update_store_indexes`), y añadir prueba en `tests/api/test_api_edges.py` de que tras `stores update` el documento editado sale de stale. Repo SLDB_1; resultado: textos alineados, test verde, CHANGELOG bajo "0.1.13 — not released yet", commit del coordinador y aviso a graph_ui. Límites: no cambia `rebuild_edges`, no toca stale por documento en graph_ui; si `update_store_indexes` no resuelve, se detiene y reporta.

## AMBIGUEDADES

1. "Test nuevo en tests/api/test_api_edges.py: editar a mano un documento…" frente al pill: "El test se hace extendiendo el que ya existe (test_a_hand_edit_reaches_the_index_through_stores_update)". Obliga a inventar si se crea test nuevo o se modifica el existente.
2. Texto de alerta: Precisiones dan `alert("edges/stale", s, "tracked file changed since its shard was built", "sldb stores update")`; el pill exige "shard out of date (missing, built by another version, or the file changed outside sldb), con fix 'sldb stores update'". Obliga a elegir entre dos mensajes exactos y contradictorios.
3. El pill "Where" solo cubre "src/sldb/cli/commands/edges.py, tests/api/test_api_edges.py", pero el encargo también cambia `edge_index.py` y `edge_reading.py`: ningún pill cubre esos dos textos exactos.
4. "grep -rn 'edges rebuild' src/sldb docs/ para encontrar otros mensajes" frente a `files:`, que no incluye `docs/`. Obliga a decidir si se editan archivos de `docs/` fuera del alcance declarado.

## DRY-RUN

Leería: el TaskDoc, el pill, `edge_index.py`, `edge_reading.py`, `commands/edges.py`, `tests/api/test_api_edges.py`, `CHANGELOG.md` y, si existe, `tests/api/test_composition_edges.py`. Cambios previstos: tres textos exactos (descripción de `stale`, docstring, alerta), prueba nueva o extendida del ciclo stale→`rebuild_edges` no lo saca→`update_store_indexes` sí, línea en CHANGELOG y grep de mensajes residuales. Dependencias: fixtures `EdgeWorld`/`world`, `api.update_store_indexes`, `api.rebuild_edges`, `api.load_edge_index`. Validaciones futuras: `TMPDIR=/dev/shm pytest -q tests/api/test_api_edges.py` y `TMPDIR=/dev/shm pytest -q tests/api/test_composition_edges.py`, sin leerlas todavía; aviso con `deskops message send --to graph_ui`. Nada ejecutado.

## FUTURO

El coordinador ejecuta `deskops closeout commit` y verifica con `deskops closeout verify`; el humano resuelve las ambigüedades 1–4 y decide si, al fallar `update_store_indexes`, se abre tarea aparte.
