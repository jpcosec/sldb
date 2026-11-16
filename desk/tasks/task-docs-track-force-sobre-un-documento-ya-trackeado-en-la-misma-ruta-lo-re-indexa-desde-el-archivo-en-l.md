---
sldb:
  by: agent
  at: '2026-11-16T21:48:26Z'
  authority: generated
  via: create_document
id: task-docs-track-force-sobre-un-documento-ya-trackeado-en-la-misma-ruta-lo-re-indexa-desde-el-archivo-en-l
status: draft
summary: ''
tags:
- workspace:desk
- artifact:task
- host:robocop2
current_node: ritual-execution
history: []
references:
- desk/inbox/20261116-162239-unclear-docs-track-force-no-fuerza-sigue-diciendo-already-tracked.md
depends_on: []
pills: []
files:
- src/sldb/store/ops.py
- src/sldb/api/documents/track_document_file.py
- tests/api/test_api_documents.py
- CHANGELOG.md
task_type: task.code
inherits_from: []
inherit_acceptance_context: false
atoms: []
---

# docs track --force sobre un documento ya trackeado en la misma ruta lo re-indexa desde el archivo en lugar de fallar con already tracked

## Rationale

_Explain why this task exists or the business driver behind it._

Dos consumidores necesitan re-trackear un documento que ya está en el store: sldb-ui guarda un archivo y hace docs track --force (nota desk/inbox/20261116-162239-unclear-docs-track-force-no-fuerza-sigue-diciendo-already-tracked.md), y pron, que desde su commit 79ddb2d versiona .sldb/core/, corre make world (pron init --world) sobre un clon que ya trae los shards. El job store del CI de sldb sobre c5cb52f0 falla en 'Prepare pron's store' con SLDBStoreError: Doc 'rt-implements' already tracked, lanzado por StoreOperations._pre_check (src/sldb/store/ops.py) aunque track_document_file recibe force=True. Hoy force solo salta la comprobación de round-trip.

## Goal

_Describe the concrete result this task must produce._

track_document_file(..., force=True) y docs track --force sobre un documento ya trackeado con el mismo modelo, nombre y ruta lo re-indexan desde el contenido actual del archivo (shard, índice y aristas al día) y terminan sin error; sin force sigue fallando con already tracked; make world de pron vuelve a pasar contra este sldb.

## Scope

_State what is in scope and what is out of scope._

Entra: (1) con force, si el shard de (modelo, nombre) existe y apunta a la misma ruta del proyecto, track re-indexa ese documento desde el archivo como lo haría una edición externa reconocida, bajo store_lock, y no duplica la entrada en la declaración del store (declare_tracked queda idempotente). (2) con force, si el shard existe pero apunta a otra ruta, falla con SLDBStoreError que nombra las dos rutas (force no mueve documentos; para eso está move). (3) sin force, el comportamiento no cambia. (4) docstring de track_document_file y ayuda de docs track: force también re-indexa un documento ya trackeado en la misma ruta. (5) Tests en tests/api/test_api_documents.py: re-track con force tras editar el archivo deja el payload nuevo y el índice coherente (check_store ok); sin force falla igual que hoy; otra ruta falla y nombra las dos; repetir el track con force sin cambios es idempotente. CHANGELOG.md. No entra: cambiar pron ni el CI.

## Implementation Path

_Outline the expected implementation route or affected surface._

1) Leer src/sldb/store/ops.py (track, _pre_check, _do_track), src/sldb/api/documents/track_document_file.py, la sincronía de la declaración (declare_tracked) y cómo se re-indexa una edición externa (update o sync de un documento trackeado). 2) Pasar force hasta StoreOperations.track y, con force y la misma ruta, re-indexar reutilizando ese camino en vez de lanzar. 3) Tests. 4) Reproducir pron: clonar pron (master) a /dev/shm, crear un venv con este sldb y pron editables (uv venv; uv pip install -e sldb[code,mcp] -e pron[mcp]) y correr make world allí; anotar el resultado en result-summary.md. 5) Validation.

## Validation

_List the checks required before this task can close._

- TMPDIR=/dev/shm uv run --frozen --extra code --extra dev pytest -q tests/api/test_api_documents.py
- TMPDIR=/dev/shm uv run --frozen --extra code --extra dev pytest -q tests/api/test_on_write_entering.py
- TMPDIR=/dev/shm uv run --frozen --extra code --extra dev pytest -q tests/api/test_api_stores.py
- TMPDIR=/dev/shm uv run --frozen --extra code --extra dev pytest -q tests/test_links_batch_cli.py
- TMPDIR=/dev/shm uv run --frozen --extra code --extra dev pytest -q tests/test_clean_code_rules.py
- TMPDIR=/dev/shm uv run --frozen --extra code --extra dev bash tools/check.sh --fast

## Done When

_Name the observable condition that makes the task complete._

Los comandos de Validation pasan con los tests nuevos; result-summary.md muestra make world de pron con rc 0 contra este sldb en un clon limpio de pron; CHANGELOG y commit; aviso a sldb-ui y a pron.
