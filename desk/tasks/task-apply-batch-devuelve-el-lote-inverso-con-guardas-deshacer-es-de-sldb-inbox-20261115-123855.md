---
sldb:
  by: agent
  at: '2026-11-15T15:52:03Z'
  authority: generated
  via: create_document
id: task-apply-batch-devuelve-el-lote-inverso-con-guardas-deshacer-es-de-sldb-inbox-20261115-123855
status: draft
summary: ''
tags:
- workspace:desk
- artifact:task
current_node: ritual-execution
history: []
references: []
depends_on:
- task-apply-batch-guardas-expected-source-hash-bajo-el-cerrojo-del-store-inbox-20261115-022444
pills: []
files: []
task_type: task.code
inherits_from: []
inherit_acceptance_context: false
atoms: []
---

# apply_batch devuelve el lote inverso con guardas: deshacer es de sldb (inbox 20261115-123855)

## Rationale

_Explain why this task exists or the business driver behind it._

Decisión de JP 2026-11-15: deshacer es de sldb, no de los consumidores (specIR, deskops, la UI).

## Goal

_Describe the concrete result this task must produce._

BatchReport lleva el lote inverso, en la forma que acepta apply_batch; deshacer = apply_batch(report.inverse).

## Scope

_State what is in scope and what is out of scope._

Pedido del inbox sldb 20261115-123855. Crear X se invierte en borrar X; actualizar en restaurar campos o texto previos; borrar en recrear con el contenido previo; aristas igual sobre sus RelationDoc. Cada operación del inverso lleva expected_source_hash del estado que dejó el lote, así que aplicarlo tras un cambio ajeno se rechaza como ConflictError sin escritura parcial. Procedencia del inverso registrada como cualquier escritura. Decidir si se apoya en los snapshots que Transaction ya tiene para el rollback (pregunta de la nota). Cuando esté, la tool undo_changes del MCP de sldb (tarea sldb mcp) lo expone.

## Implementation Path

_Outline the expected implementation route or affected surface._



## Validation

_List the checks required before this task can close._

- TMPDIR=/dev/shm pytest -q de los archivos tocados, uno a la vez
- tools/check.sh
- sldb stores build --check

## Done When

_Name the observable condition that makes the task complete._

apply_batch(report.inverse) deja el store idéntico al previo; un cambio ajeno intermedio rechaza el deshacer sin escritura parcial; cubre documentos y aristas; suite de a un archivo, tools/check.sh y stores build --check.
