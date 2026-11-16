# Resultado — executor deskops-e-a51428cebb72

Tarea: `task-carga-tolerante-en-la-api-pública-load-runtime-documents-aísla-los-documentos-inválidos-y-los-nombra`
Pill aplicado: `pill-pill-rechazados-de-la-carga-tolerante` (no choca con el contrato; autoriza `src/sldb/store/query.py`).

## Cambios (archivo y función)

- `src/sldb/store/query.py` (autorizado por el pill):
  - `_load_accepted(*args, rejected=None)`: si recibe `rejected`, le agrega `(doc.path, m_entry.name, str(exc))` cuando el modelo rechaza el documento. Los llamadores actuales no la pasan y no cambian.
  - `_load_one(..., rejected=None)` y `load_runtime_documents(..., rejected=None)`: llevan la lista hasta `_load_accepted` (con `functools.partial`). Sin `rejected` todo sigue igual (caché incluido).
- `src/sldb/api/documents/runtime_documents.py`:
  - Dataclasses nuevas `InvalidDocument(path, model, error)` y `RuntimeDocuments(documents, invalid)`, en `__all__` del módulo.
  - `load_runtime_documents(store_path, pythonpath=None, include_linked=False, on_invalid="raise")` (con `@overload` por modo):
    - `"skip"` → `_skipping`: llama al store con `accepted_only=True, rejected=[...]` y devuelve `RuntimeDocuments`.
    - `"raise"` (por defecto) → devuelve `list` como antes, por el camino con caché; si sale un `pydantic.ValidationError`, vuelve a cargar en modo `skip` para saber qué documento fue y relanza `SLDBValidationError("<ruta>: <mensaje original>", {"path", "model"}) from exc`. Solo envuelve `ValidationError` de pydantic (nunca un `SLDBValidationError` ya existente, como pide el pill). Si la segunda pasada no encuentra rechazados, se relanza la excepción original.
    - Otro valor de `on_invalid` → `ValueError`.
- `src/sldb/api/__init__.py`: exporta `RuntimeDocuments` e `InvalidDocument` (import + `__all__`). **Desvío menor**, ver abajo.
- `src/sldb/store/edge_index/edge_index.py`:
  - Modelo pydantic nuevo `EdgeProblem(kind, document, detail)`, constante `ENDPOINT_NOT_A_NODE = "endpoint-not-a-node"` y función `edge_problem(text)`.
  - `EdgeIndex.problem_details: list[EdgeProblem]`, junto a `problems` (que no cambia).
  - `@model_validator(mode="after") _details_follow_problems`: si `problem_details` no cuadra con `problems` (detail por detail), lo deriva: `kind="endpoint-not-a-node"`, `document="RelationDoc:<relation_doc>"` (el export id del RelationDoc que declaró la arista, leído del texto `relation '<name>': ...` que arma `resolve._authored`), `detail` = el mismo string.
- `tests/api/test_api_documents.py`: 3 tests nuevos (usa la fixture existente `store_with_invalid` de `tests/store/invalid_memo_store.py`):
  - `test_load_runtime_documents_skip_returns_the_sound_ones_and_names_the_invalid`: documentos = `["c"]`, invalid = `[("a.md","Memo"),("b.md","Memo")]` con el texto del error.
  - `test_load_runtime_documents_raise_names_the_path_of_the_invalid_document`: `SLDBValidationError` con mensaje `a.md: ...status bad is not a status`, `__cause__` es el `ValidationError`.
  - `test_load_runtime_documents_default_still_returns_a_list`: el default sigue dando `list`; `skip` sobre un store sano da los mismos y `invalid == []`.
- `tests/api/test_api_edges.py`: `test_problem_details_structure_each_problem` (2 problemas: relación huérfana + destino destrackeado): `len(problem_details) == len(problems)`, mismos `detail` en orden, `kind` único `endpoint-not-a-node`, `document` = `RelationDoc:b1-t12` y `RelationDoc:orphan`; y un índice releído sin `problem_details` (como uno guardado en disco antes del campo) lo reconstruye igual.
- `CHANGELOG.md`: una línea en español al principio de `## 0.1.13 — not released yet (no tag, not on PyPI)`.

## Done When

- Los tres comandos de Validation pasan con los tests nuevos: sí (13, 16 y 2 passed; rc=0 los tres; ver `validation.log`).
- `on_invalid="skip"` sobre un store con un documento inválido devuelve los sanos y el inválido en `invalid`: test `..._skip_returns_the_sound_ones_and_names_the_invalid`.
- `problem_details` existe y cuadra con `problems`: test `test_problem_details_structure_each_problem`.
- CHANGELOG: hecho. Commit: lo hace el coordinador con `deskops closeout commit` (no hice commit ni push).

## Comandos corridos

| Comando | rc |
|---|---|
| `TMPDIR=/dev/shm uv run --frozen --extra code --extra dev pytest -q tests/api/test_api_documents.py` | 0 (13 passed) |
| `TMPDIR=/dev/shm uv run --frozen --extra code --extra dev pytest -q tests/api/test_api_edges.py` | 0 (16 passed) |
| `TMPDIR=/dev/shm uv run --frozen --extra code --extra dev pytest -q tests/store/test_doc_invalid_check.py` | 0 (2 passed) |

`uv` funcionó; no hizo falta el fallback `uvx`. Una primera corrida falló solo por mi regex del test (el mensaje de pydantic es multilínea; se arregló con `(?s)`); la salida final de los tres está en `validation.log`. `ruff` no está instalado en el entorno (`Failed to spawn: ruff`), así que no hubo lint.

## Medición de resolve_runtime_doc (fuera de alcance cambiarlo)

Store de sldb (`.sldb`, 2680 documentos locales, 0 inválidos con `on_invalid="skip"`), pythonpath `.`, proceso nuevo cada vez, ref `PackagingDoc/packaging-instructions`:
- en frío: **1.34 s** (dos corridas, 1.34 s y 1.34 s); en caliente (misma llamada otra vez en el proceso): 0.002 s.
- Medí `runtime_document(store_path, ".", ref)`, que es lo que hace `resolve_runtime_doc` sin el `open_store(...)` previo: lo omití para no arriesgar escrituras/migración en `.sldb/` (prohibido tocarlo). `git status --porcelain .sldb` dio el mismo hash antes y después. El coste es el barrido total de `load_runtime_documents`; si se quiere bajar, es otra tarea.

## Archivos tocados (lista exacta)

- `src/sldb/store/query.py`
- `src/sldb/api/documents/runtime_documents.py`
- `src/sldb/api/__init__.py`
- `src/sldb/store/edge_index/edge_index.py`
- `tests/api/test_api_documents.py`
- `tests/api/test_api_edges.py`
- `CHANGELOG.md`
- (evidencia) `runs/subagents/20261116-exec-carga-tolerante/validation.log`, `result-summary.md`

No toqué los cambios ajenos (`apply_batch.py`, `lock.py`, `test_apply_batch_lock.py`, `uv.lock`, `desk/`, `.sldb/`, `.herdr-coordination.md`).

## Desvíos y dudas

1. **`src/sldb/api/__init__.py`** no está en `files`. El Scope dice que `RuntimeDocuments` se "define en el mismo módulo y exporta"; como la función es la de `sldb.api`, lo leí como exportarlo desde `sldb.api` (2 nombres en el import y en `__all__`). Si se quería solo en el módulo, basta revertir ese archivo y cambiar `api.RuntimeDocuments`/`api.InvalidDocument` de los tests por el import del módulo.
2. **`problem_details` se deriva en `EdgeIndex`, no en `resolve._authored`.** El Scope dice "poblado donde hoy se agregan strings a problems" (eso es `src/sldb/store/edge_index/resolve.py`, más `compose.py` para pasarlo), y ninguno de los dos está en `files`. Además el índice compuesto se guarda en disco (`composed_disk.py`, `FORMAT = "1"`) y un índice viejo releído llegaría sin el campo. Un validador en `edge_index.py` resuelve las dos cosas sin tocar otros archivos: cada vez que se arma un `EdgeIndex` (compuesto o releído), `problem_details` sale de `problems`, uno a uno y en el mismo orden. El precio: `document` se saca del texto con una regex sobre el único formato que hoy produce `resolve._authored`; un texto que no cuadre da `document=""` (y `kind` igual `endpoint-not-a-node`, como fija el contrato). Si se prefiere poblarlo estructurado en origen, hace falta autorizar `resolve.py` y `compose.py`.
3. `EdgeProblem` no se exportó desde `sldb.api` (el contrato no lo pide); se importa de `sldb.store.edge_index.edge_index`.
4. En modo `"raise"`, para nombrar la ruta se hace una segunda carga sin caché solo cuando ya falló; el camino normal sigue con caché. Con `include_linked=True` la ruta es relativa al proyecto del store donde vive el documento.
5. No hay avisos `deskops message send` que mandar desde el ejecutor (el contrato no pide aviso a otro repo en esta tarea).
