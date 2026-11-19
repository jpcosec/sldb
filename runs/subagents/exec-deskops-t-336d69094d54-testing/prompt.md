Task: task-apply-batch-dry-run-público-que-valida-sin-escribir-inbox-20261115-022430
Title: apply_batch: dry_run público que valida sin escribir (inbox 20261115-022430)
Status: active
Current node: ritual-testing
Task type: task.code
Lifecycle gates:
- task_hands_to_closeout -> ritual-closeout: open [nonempty(validation)]
  post-hook evento-para-el-coordinador: sh -c mkdir -p runs/hooks && printf '%s %s %s %s->%s\n' "$(date -u +%FT%TZ)" "$DESKOPS_TASK_ID" "$DESKOPS_TRANSITION" "$DESKOPS_FROM_NODE" "$DESKOPS_TO_NODE" >> runs/hooks/events.log
  post-hook encola-reap-del-tester: deskops queue add dispatch-reap --root .

---
sldb:
  by: agent
  at: '2026-11-19T04:29:51Z'
  authority: generated
  via: save_document_payload
id: task-apply-batch-dry-run-público-que-valida-sin-escribir-inbox-20261115-022430
status: active
summary: ''
tags:
- workspace:desk
- artifact:task
current_node: ritual-testing
history:
- task_activates
references: []
depends_on: []
pills: []
files: []
task_type: task.code
inherits_from: []
inherit_acceptance_context: false
atoms: []
---

# apply_batch: dry_run público que valida sin escribir (inbox 20261115-022430)

## Rationale

_Explain why this task exists or the business driver behind it._

El MCP de specIR (decisión IR02 D1) valida una propuesta como lote de apply_batch sin escribir y luego la aplica. Hoy la prevalidación existe pero no es pública.

## Goal

_Describe the concrete result this task must produce._

apply_batch acepta dry_run=True: corre la prevalidación (forma, modelo, round-trip, guardas, destinos) y devuelve el informe o los errores, sin abrir transacción ni escribir.

## Scope

_State what is in scope and what is out of scope._

Pedido del inbox sldb 20261115-022430 (dry_run público de apply_batch). Verificado hoy: apply_batch no tiene dry_run y prevalidate_changes no está en sldb.api. Exponer el modo en la API pública, documentar la forma del informe, exportarlo y cubrirlo con tests que prueban que el store queda idéntico. Lo consume el propose_changes del MCP (tarea sldb mcp) que hoy lo simula. Cerrar la nota del inbox al terminar.

## Implementation Path

_Outline the expected implementation route or affected surface._

Ubicaciones (sldb HEAD al despachar): apply_batch en src/sldb/api/documents/apply_batch.py:27 (y apply_batches en :60, que encadena lotes en una transacción); la prevalidación es prevalidate_changes en src/sldb/api/documents/batch_prevalidate.py:22 (forma, modelo, round-trip, destinos) y los guards están en batch_guards.py; sldb.api exporta apply_batch y apply_batches (src/sldb/api/__init__.py:13). El dry run del MCP es propose_changes en src/sldb/mcp/write/tools.py:38. p1: test que falla antes: apply_batch(store, changes, dry_run=True) con un lote válido devuelve un BatchReport con saved vacío y applied=False (o el campo que se agregue, documentado) sin escribir nada: los archivos del store y del proyecto quedan byte a byte iguales. Con un lote inválido levanta el mismo error que apply_batch sin dry_run, también sin escribir. p2: implementar dry_run=False por defecto en apply_batch, con la misma prevalidación bajo el cerrojo, que vuelve antes de abrir la transacción; apply_batches no cambia. p3: si propose_changes reimplementa la prevalidación, que use apply_batch(dry_run=True); si ya usa prevalidate_changes, dejarlo y decirlo en el informe. p4: docstring de apply_batch, docs/architecture/mcp.md si propose_changes cambia, y CHANGELOG. p5: quick_gates del desk (bash tools/check.sh --fast) antes del commit, que lleva rutas nombradas y Task-Id.

## Validation

_List the checks required before this task can close._

- TMPDIR=/tmp python -m pytest -q -p no:cacheprovider tests/api
- TMPDIR=/tmp python -m pytest -q -p no:cacheprovider tests/mcp
- bash tools/check.sh --fast

## Done When

_Name the observable condition that makes the task complete._

apply_batch(dry_run=True) devuelve el mismo veredicto que la aplicación real sin escribir; tests y CHANGELOG; suite de a un archivo, tools/check.sh y stores build --check.

## Como probar (tester)

Ubica el trabajo del ejecutor:

    git log -1 --format=%H --grep "Task-Id: task-apply-batch-dry-run-público-que-valida-sin-escribir-inbox-20261115-022430"   # commit del ejecutor
    git show --name-only <commit>                           # sus archivos

Los tests a correr son los archivos tests/*.py de ese commit, mas tests/test_<modulo>.py cuando exista para cada modulo de codigo tocado; de a uno, con `TMPDIR=/tmp python -m pytest -q <archivo>`. No corras la suite completa: la corre integrate en el host.

Escribe result-summary.md con el veredicto PASA o FALLA en la primera linea.

## Gates rapidos del desk

Antes del veredicto corre, con el python del venv (/tmp/ws-venv en PATH):

    bash tools/check.sh --fast

Si termina con rc distinto de 0 el veredicto es FALLA.
