Task: task-docs-track-reindex-re-indexa-un-documento-ya-trackeado-validándolo-sin-saltar-el-round-trip-como-for
Title: docs track --reindex re-indexa un documento ya trackeado validándolo, sin saltar el round-trip como --force
Status: active
Current node: ritual-testing
Task type: task.code
Effective atoms:
- atom-track-con-force-re-indexa-desde-el-archivo-un-documento-ya-trackeado-en-la-misma-ruta
Lifecycle gates:
- task_hands_to_closeout -> ritual-closeout: open [nonempty(validation)]
  post-hook evento-para-el-coordinador: sh -c mkdir -p runs/hooks && printf '%s %s %s %s->%s\n' "$(date -u +%FT%TZ)" "$DESKOPS_TASK_ID" "$DESKOPS_TRANSITION" "$DESKOPS_FROM_NODE" "$DESKOPS_TO_NODE" >> runs/hooks/events.log
  post-hook encola-reap-del-tester: deskops queue add dispatch-reap --root .

---
sldb:
  by: agent
  at: '2026-11-19T10:51:37Z'
  authority: generated
  via: save_document_payload
id: task-docs-track-reindex-re-indexa-un-documento-ya-trackeado-validándolo-sin-saltar-el-round-trip-como-for
status: active
summary: ''
tags:
- workspace:desk
- artifact:task
- host:robocop2
current_node: ritual-testing
history:
- task_activates
references:
- desk/inbox/20261117-080455-suggestion-docs-track-force-re-indexa-sin-validar-pedido-de-un-re-index-que-valide.md
depends_on: []
pills: []
files:
- src/sldb/api/documents/track_document_file.py
- src/sldb/store/ops.py
- src/sldb/cli/parsers/docs1.py
- tests/api/test_api_documents.py
- CHANGELOG.md
task_type: task.code
inherits_from: []
inherit_acceptance_context: false
atoms:
- atom-track-con-force-re-indexa-desde-el-archivo-un-documento-ya-trackeado-en-la-misma-ruta
---

# docs track --reindex re-indexa un documento ya trackeado validándolo, sin saltar el round-trip como --force

## Rationale

_Explain why this task exists or the business driver behind it._

En sldb-ui, docs track --force sobre un documento ya trackeado devuelve rc 0 aunque el archivo no valide (enum inválido, frontmatter YAML roto) y queda indexado; después docs show falla. Es lo que dice el contrato: --force salta el round-trip. Por eso la UI guarda con untrack + track (5,5-6,2 s contra 4-5 s). Origen: desk/inbox/20261117-080455-suggestion-docs-track-force-re-indexa-sin-validar-pedido-de-un-re-index-que-valide.md.

## Goal

_Describe the concrete result this task must produce._

docs track --reindex (y track_document_file(..., reindex=True)) re-indexa desde el archivo un documento ya trackeado en la misma ruta, como --force, pero corre las mismas validaciones que un track normal: si el archivo no valida falla con el error de validación y deja el índice como estaba. --force no cambia.

## Scope

_State what is in scope and what is out of scope._

Entra: el flag --reindex en el parser y el comando de docs track, el parámetro reindex en track_document_file (src/sldb/api/documents/track_document_file.py) y su paso hasta StoreOperations.track (src/sldb/store/ops.py); --reindex y --force juntos se rechazan con un error claro; tests en tests/api/test_api_documents.py: reindex de un archivo válido editado deja el payload nuevo, de uno inválido falla y no cambia el índice, sobre un documento no trackeado se comporta como track. CHANGELOG y ayuda. No entra: cambiar --force.

## Implementation Path

_Outline the expected implementation route or affected surface._

1) Leer src/sldb/api/documents/track_document_file.py, src/sldb/store/ops.py (StoreOperations.track y el camino de force de la tarea CI2) y el parser y el comando de docs track. 2) Tests que fallen antes, en tests/api/test_api_documents.py: --reindex sobre un documento ya trackeado y válido lo re-indexa; sobre uno cuyo archivo no valida falla con el error de validación y el índice queda byte a byte igual; --reindex con --force da un error claro; --force no cambia. 3) Implementar. 4) Como hay un flag nuevo (--reindex), correr 'PYTHONPATH=src sldb selfdoc sync' y commitear la referencia CLI que regenere; después 'PYTHONPATH=src sldb selfdoc check' en 0. 5) CHANGELOG. 6) quick_gates del desk (bash tools/check.sh --fast) en 0 antes del commit, con rutas nombradas y Task-Id.

## Validation

_List the checks required before this task can close._

- TMPDIR=/dev/shm uv run --frozen --extra code --extra dev pytest -q tests/api/test_api_documents.py
- TMPDIR=/dev/shm uv run --frozen --extra code --extra dev pytest -q tests/api/test_on_write_entering.py
- TMPDIR=/dev/shm uv run --frozen --extra code --extra dev pytest -q tests/test_links_batch_cli.py
- TMPDIR=/dev/shm uv run --frozen --extra code --extra dev pytest -q tests/test_clean_code_rules.py
- TMPDIR=/dev/shm uv run --frozen --extra code --extra dev bash tools/check.sh --fast

## Done When

_Name the observable condition that makes the task complete._

Los comandos de Validation pasan con los tests nuevos; CHANGELOG y commit; aviso a sldb-ui.

## Como probar (tester)

Ubica el trabajo del ejecutor:

    git log -1 --format=%H --grep "Task-Id: task-docs-track-reindex-re-indexa-un-documento-ya-trackeado-validándolo-sin-saltar-el-round-trip-como-for"   # commit del ejecutor
    git show --name-only <commit>                           # sus archivos

Los tests a correr son los archivos tests/*.py de ese commit, mas tests/test_<modulo>.py cuando exista para cada modulo de codigo tocado; de a uno, con `TMPDIR=/tmp python -m pytest -q <archivo>`. No corras la suite completa: la corre integrate en el host.

Escribe result-summary.md con el veredicto PASA o FALLA en la primera linea.

## Gates rapidos del desk

Antes del veredicto corre, con el python del venv (/tmp/ws-venv en PATH):

    bash tools/check.sh --fast

Si termina con rc distinto de 0 el veredicto es FALLA.
