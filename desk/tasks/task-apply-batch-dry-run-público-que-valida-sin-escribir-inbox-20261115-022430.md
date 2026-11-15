---
sldb:
  by: agent
  at: '2026-11-15T15:51:39Z'
  authority: generated
  via: create_document
id: task-apply-batch-dry-run-público-que-valida-sin-escribir-inbox-20261115-022430
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



## Validation

_List the checks required before this task can close._

- TMPDIR=/dev/shm pytest -q de los archivos tocados, uno a la vez
- tools/check.sh
- sldb stores build --check

## Done When

_Name the observable condition that makes the task complete._

apply_batch(dry_run=True) devuelve el mismo veredicto que la aplicación real sin escribir; tests y CHANGELOG; suite de a un archivo, tools/check.sh y stores build --check.
