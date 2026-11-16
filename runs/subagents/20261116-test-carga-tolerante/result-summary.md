# Tester deskops-t-b92e84cfea3e — task-carga-tolerante-en-la-api-pública-load-runtime-documents-aísla-los-documentos-inválidos-y-los-nombra

**Veredicto global: PASA** (con dos observaciones que no bloquean, abajo).

Entorno: `uv run --frozen --extra code --extra dev` funcionó; no hizo falta `uvx`. `uv.lock` ya traía cambios ajenos antes de mi corrida (listados en el brief); no lo toqué. Salida completa: `validation.log`.

## Validation (corridos por mí)

| Comando | Resultado | Veredicto |
|---|---|---|
| `TMPDIR=/dev/shm pytest -q tests/api/test_api_documents.py` | 13 passed, rc=0 | PASA |
| `TMPDIR=/dev/shm pytest -q tests/api/test_api_edges.py` | 16 passed, rc=0 | PASA |
| `TMPDIR=/dev/shm pytest -q tests/store/test_doc_invalid_check.py` | 2 passed, rc=0 | PASA |

## Done When, punto por punto

1. **Los tres comandos pasan con los tests nuevos**: PASA. Los tests nuevos están en el diff y corrieron: `test_load_runtime_documents_skip_returns_the_sound_ones_and_names_the_invalid`, `..._raise_names_the_path_of_the_invalid_document`, `..._default_still_returns_a_list` y `test_problem_details_structure_each_problem`.
2. **`on_invalid="skip"` devuelve los sanos y el inválido en `invalid`**: PASA. Lo cubre el test con la fixture `store_with_invalid` (documents=`["c"]`, invalid=`a.md`, `b.md`), y lo reproduje por separado: un inválido en `notes/deep/x.md` da `invalid=[notes/deep/x.md]` (ruta relativa al proyecto) y `documents=[y]`. Coincide con las Precisiones: `RuntimeDocuments(documents, invalid: list[InvalidDocument(path, model, error)])`, se implementa con `accepted_only=True` y `rejected` en `_load_accepted`. Con `raise`, la función devuelve `list`, y si un documento es inválido lanza `SLDBValidationError("<ruta>: <msg>") from ValidationError` (comprobado también con la ruta de subcarpeta). Solo envuelve `pydantic.ValidationError`, como pide el pill.
3. **`problem_details` existe y cuadra con `problems`**: PASA. El test comprueba la misma cantidad, el mismo `detail` en el mismo orden, `kind="endpoint-not-a-node"` y `document="RelationDoc:<name>"`. Verifiqué que `resolve._authored` (`src/sldb/store/edge_index/resolve.py:55`) es el único punto que agrega a `problems` y que su formato coincide con el regex. `problems` sigue siendo `list[str]` sin cambios.
4. **CHANGELOG**: PASA. Hay una línea en español bajo `## 0.1.13 — not released yet`, con el estilo de las entradas vecinas. **Commit**: no aplica al ejecutor; lo hace el coordinador con `deskops closeout commit`. Confirmé que no hay commit ni push del ejecutor (HEAD sigue en 336cde87).

## Alcance de archivos (punto 5 del brief)

Archivos del ejecutor: los 5 de `files`, más:
- `src/sldb/store/query.py`: **autorizado** por el pill (`_load_accepted` recibe `rejected`). Los llamadores actuales no cambian.
- `src/sldb/api/__init__.py`: **fuera de `files`**. Agrega 2 nombres al import y a `__all__` (`RuntimeDocuments`, `InvalidDocument`). Es un desvío menor que el ejecutor declaró. Lo justifica con el "exportado" del Scope, y los tests usan `api.RuntimeDocuments`. No lo considero un fallo, pero **el coordinador debe decidir** si lo acepta en el commit o pide revertirlo.
- `.sldb/core/models/RunDoc.yaml`, `.sldb/core/store_index.yaml`, `.sldb/store.yaml` y los `RunDoc/run-deskops-{e,t}-*.yaml`: registro de los RunDoc de este despacho (coordinador), no del ejecutor.
- Cambios ajenos (`apply_batch.py`, `lock.py`, `test_apply_batch_lock.py`, `uv.lock`, `desk/runtimes/`, `.herdr-coordination.md`, `runs/subagents/2026110*`): no los revisé ni los toqué.

## Casos no cubiertos por el ejecutor (scripts: `/dev/shm/tcarga/edge_cases.py`, `/dev/shm/tcarga/cache_case.py`, copiados en este run-dir)

- Inválido en una subcarpeta: la ruta relativa incluye la subcarpeta, en `skip` y en `raise`. OK.
- `on_invalid="ignore"`: lanza `ValueError`. OK.
- Store enlazado con `include_linked=True`: `skip` devuelve `j`, `m` e invalid=`[k.md]`, y `raise` nombra `k.md`. OK. Nota: la ruta es relativa al proyecto del store enlazado, no al del store raíz, como anota el ejecutor. Con eso solo no se distingue un `k.md` homónimo entre stores, porque `InvalidDocument` no lleva el nombre del store.
- `skip` repetido: estable, no acumula rechazados. OK.
- `EdgeIndex` con un `problem_details` incoherente pasado a mano: se re-deriva desde `problems`. Un texto con formato desconocido da `document=""`. Un nombre de relación con `': '` se extrae bien. OK.
- **Observación (preexistente, fuera de alcance):** tras una carga sana en el mismo proceso, editar a mano un documento y dejarlo inválido sin `stores update` no hace lanzar `raise`, y `skip` tampoco lo lista. Los dos devuelven el documento viejo desde `cached_document`, que se indexa por el `source_hash` del índice. El camino de HEAD (`sldb.store.query.load_runtime_documents` crudo) se comporta igual, y `runtime_cache.py` no cambió. En un proceso nuevo, `raise` sí lanza `SLDBValidationError p.md: ...`. No es una regresión de esta tarea. Si graph_ui recarga en el mismo proceso tras ediciones externas, sirve como candidata para otra tarea.

## Observación sobre el diseño de `problem_details`

Se deriva en un `model_validator` de `EdgeIndex` que lee el texto de `problems` con un regex, en vez de poblarse en origen (`resolve.py`/`compose.py`, que no están en `files`). El resultado observable cumple el contrato. El riesgo: si cambia el texto de `resolve._authored`, `document` queda en `""` sin que falle ningún test. El ejecutor lo declaró.
