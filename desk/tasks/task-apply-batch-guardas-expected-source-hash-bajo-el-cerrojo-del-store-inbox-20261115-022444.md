---
sldb:
  by: agent
  at: '2026-11-15T15:51:43Z'
  authority: generated
  via: create_document
id: task-apply-batch-guardas-expected-source-hash-bajo-el-cerrojo-del-store-inbox-20261115-022444
status: draft
summary: ''
tags:
- workspace:desk
- artifact:task
current_node: ritual-execution
history: []
references: []
depends_on: []
pills: []
files: []
task_type: task.code
inherits_from: []
inherit_acceptance_context: false
atoms: []
---

# apply_batch: guardas expected_source_hash bajo el cerrojo del store (inbox 20261115-022444)

## Rationale

_Explain why this task exists or the business driver behind it._

Con dos procesos escribiendo, otro puede cambiar un documento entre la comprobación del guarda y la escritura; el guarda no lo ve.

## Goal

_Describe the concrete result this task must produce._

apply_batch sostiene el cerrojo del store desde la prevalidación hasta la última escritura, y los guardas se comprueban dentro de la transacción.

## Scope

_State what is in scope and what is out of scope._

Pedido del inbox sldb 20261115-022444. Hoy los guardas se comprueban en la prevalidación y la aplicación no los recibe; el cerrojo StoreIOLock se toma por escritura de índice. Tomar el cerrojo en todo el lote, comprobar guardas dentro, test con dos procesos que prueba que no hay escritura parcial ni guarda saltado. Prerrequisito del lote inverso (inbox 20261115-123855) porque el inverso lleva guardas del estado que dejó el lote.

## Implementation Path

_Outline the expected implementation route or affected surface._



## Validation

_List the checks required before this task can close._

- TMPDIR=/dev/shm pytest -q de los archivos tocados, uno a la vez
- tools/check.sh
- sldb stores build --check

## Done When

_Name the observable condition that makes the task complete._

Test de concurrencia con dos procesos reales sobre un store copiado: el guarda rechaza como ConflictError sin escritura parcial; suite de a un archivo, tools/check.sh y stores build --check.
