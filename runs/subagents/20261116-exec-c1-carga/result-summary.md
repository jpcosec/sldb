# Resultado — executor deskops-e-bdda64e24677

Tarea: `task-clean-code-tras-carga-tolerante-edge-index-py-y-runtime-documents-py-con-una-clase-cada-uno-y-query`
Pills atados: ninguno. Sin choque de pills.

## Qué cambió

- `src/sldb/store/edge_index/edge_problem.py` (nuevo): `ENDPOINT_NOT_A_NODE`, `_ENDPOINT_PROBLEM`, clase `EdgeProblem` y función `edge_problem`, movidos tal cual desde `edge_index.py`.
- `src/sldb/store/edge_index/edge_index.py`: queda solo `EdgeIndex`; importa y reexporta `ENDPOINT_NOT_A_NODE`, `EdgeProblem`, `edge_problem` (`__all__`). Se fueron `import re` y `RELATION_MODEL` (ya no se usan acá).
- `src/sldb/api/documents/invalid_document.py` (nuevo): dataclass `InvalidDocument`, movida tal cual.
- `src/sldb/api/documents/runtime_documents.py`: importa `InvalidDocument` del módulo nuevo (sigue en `__all__`, reexport). Además `load_runtime_documents` delega la rama `raise` en una función privada nueva `_raising` (try/except idéntico): al quitar la 2.ª clase, la regla de funciones dejó ver que `load_runtime_documents` tenía 11 líneas de lógica (máx. 10); antes la tapaba el fallo de clases. Mismo comportamiento.
- `src/sldb/store/query_engine/accepted_load.py` (nuevo): `load_accepted(load_doc, *args, rejected=None)`, el antiguo `_load_accepted` de `query.py` con el cargador recibido como parámetro (evita import circular y conserva que `query._load_doc`/`query._extract_doc` sigan siendo los que se monkeypatchean).
- `src/sldb/store/query.py`: sin `_load_accepted` ni `from pydantic import ValidationError`; `_load_one` usa `partial(load_accepted, _load_doc, rejected=rejected)`. Queda en ≤ 80 líneas efectivas.
- `CHANGELOG.md`: una línea bajo `## 0.1.13 — not released yet` como arreglo de clean code sin cambio de comportamiento.

## Desvíos

1. **Ubicación del helper de query.py**: el Scope dice "módulo vecino". Primero lo puse en `src/sldb/store/accepted_load.py`, pero `tools/check.sh --fast` falló en la puerta *ejes* (`archivo sin eje: store/accepted_load.py`): el eje de `store/query.py` en `contracts/layers.toml` lista archivos sueltos, y editar el contrato no está autorizado. Lo moví a `src/sldb/store/query_engine/accepted_load.py` (paquete vecino, eje de carpeta entera; `query.py` ya importaba `query_engine`). Con eso check.sh --fast pasa.
2. **`_raising` en runtime_documents.py**: extracción no listada en el Scope, pero necesaria para cumplir la regla de 10 líneas en un archivo tocado (el brief la cuenta como falla).

## Done When

- Validation: test_api_documents (13 passed), test_api_edges (16 passed), test_doc_invalid_check (2 passed), check.sh --fast rc 0. Extra: tests/store/test_runtime_cache_outside_store.py (monkeypatch de `sldb.store.query._extract_doc`) 3 passed.
- `tests/test_clean_code_rules.py`: rc 1, **pero ninguno de los archivos de esta tarea falla**: `edge_index.py`, `runtime_documents.py` y `query.py` pasan, y los 3 módulos nuevos también (1159 passed, antes 1153 con 10 fallos). Los 7 fallos restantes son ajenos y existían antes de este cambio (corrida inicial: 10 fallos = estos 7 + los 3 de la tarea): `sldb/mcp/write/tools.py`, `sldb/api/edges/referrers.py`, `sldb/api/edges/rewrite_references.py`, `sldb/api/documents/create_document.py`, `sldb/store/package_version.py`, `sldb/store/section_sync.py`, `sldb/store/io/lock.py` (este último con cambios ajenos sin commitear). Fuera de alcance por el Scope; no tocados. Por eso el comando completo no queda en rc 0 hasta que otra tarea los arregle.
- `git diff --stat -- tests` vacío: ningún test tocado.
- Commit: prohibido por el brief; queda para el closeout del coordinador.
- API pública intacta: `sldb.api.InvalidDocument is sldb.api.documents.runtime_documents.InvalidDocument` → True; `from sldb.store.edge_index.edge_index import EdgeProblem, edge_problem, ENDPOINT_NOT_A_NODE` funciona.

## Comandos (salida completa en validation.log)

| comando | rc |
|---|---|
| `TMPDIR=/dev/shm uv run --frozen --extra code --extra dev pytest -q tests/api/test_api_documents.py` | 0 |
| `... pytest -q tests/api/test_api_edges.py` | 0 |
| `... pytest -q tests/store/test_doc_invalid_check.py` | 0 |
| `... pytest -q tests/test_clean_code_rules.py` | 1 (7 fallos ajenos preexistentes; 0 en archivos de la tarea) |
| `... bash tools/check.sh --fast` | 0 |
| `... pytest -q tests/store/test_runtime_cache_outside_store.py` (extra) | 0 |

Nota: `ruff` no es puerta de Validation; los avisos I001/UP037/RUF100 en `edge_index.py` y `query.py` ya existían en HEAD.

## Archivos tocados

- `CHANGELOG.md`
- `src/sldb/store/edge_index/edge_index.py`
- `src/sldb/store/edge_index/edge_problem.py` (nuevo)
- `src/sldb/api/documents/runtime_documents.py`
- `src/sldb/api/documents/invalid_document.py` (nuevo)
- `src/sldb/store/query.py`
- `src/sldb/store/query_engine/accepted_load.py` (nuevo)
- `runs/subagents/20261116-exec-c1-carga/validation.log`, `result-summary.md` (entrega)

Nada stageado ni commiteado; cambios ajenos (`apply_batch.py`, `io/lock.py`, `uv.lock`, `desk/`, `.sldb/`, etc.) sin tocar.
