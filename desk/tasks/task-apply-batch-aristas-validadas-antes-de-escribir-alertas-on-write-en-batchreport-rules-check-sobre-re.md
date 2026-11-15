---
sldb:
  by: agent
  at: '2026-11-15T15:52:07Z'
  authority: generated
  via: create_document
id: task-apply-batch-aristas-validadas-antes-de-escribir-alertas-on-write-en-batchreport-rules-check-sobre-re
status: draft
summary: ''
tags:
- workspace:desk
- artifact:task
current_node: ritual-execution
history: []
references: []
depends_on:
- task-apply-batch-dry-run-público-que-valida-sin-escribir-inbox-20261115-022430
pills: []
files: []
task_type: task.code
inherits_from: []
inherit_acceptance_context: false
atoms: []
---

# apply_batch: aristas validadas antes de escribir, alertas on_write en BatchReport, rules_check sobre RelationDoc y via/authority (inbox 20261115-022655)

## Rationale

_Explain why this task exists or the business driver behind it._

specIR escribe solo por apply_batch y hoy declara cuatro faltantes; ninguno es de dominio.

## Goal

_Describe the concrete result this task must produce._

Cerrar los cuatro puntos del pedido.

## Scope

_State what is in scope and what is out of scope._

Pedido del inbox sldb 20261115-022655, cuatro puntos: (1) validar un RelationDoc contra su RelationTypeDoc (tipos de extremo, cardinalidad, condición) en la prevalidación y en el dry_run, no solo en check_edges después de escribir; (2) BatchReport.alerts con las alertas on_write de cada documento escrito; (3) rules_check sobre un RelationDoc acepta lo que check_on_write acepta o falla con un error claro; (4) parámetros opcionales via y authority en apply_batch y Transaction, como ya existe actor. Verificar cada punto contra HEAD antes de implementarlo.

## Implementation Path

_Outline the expected implementation route or affected surface._



## Validation

_List the checks required before this task can close._

- TMPDIR=/dev/shm pytest -q de los archivos tocados, uno a la vez
- tools/check.sh
- sldb stores build --check

## Done When

_Name the observable condition that makes the task complete._

Cada punto con su test; reproducción del punto 1 (RelationDoc con origen fuera de source_types) rechazada antes de escribir; suite de a un archivo, tools/check.sh y stores build --check.
