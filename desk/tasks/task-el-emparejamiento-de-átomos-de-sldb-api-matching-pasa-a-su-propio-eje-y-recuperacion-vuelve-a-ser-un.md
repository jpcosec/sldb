---
sldb:
  by: agent
  at: '2026-11-16T02:19:42Z'
  authority: generated
  via: create_document
id: task-el-emparejamiento-de-átomos-de-sldb-api-matching-pasa-a-su-propio-eje-y-recuperacion-vuelve-a-ser-un
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
task_type: task.refactor
inherits_from: []
inherit_acceptance_context: false
atoms: []
---

# El emparejamiento de átomos de sldb.api.matching pasa a su propio eje y recuperacion vuelve a ser un puerto puro

## Rationale

_Explain why this task exists or the business driver behind it._

Decisión de JP 2026-11-15 (recomendación del coordinador aceptada): tras D4, la unidad recuperacion (api/matching) quedó marcada extractable_today=true pero depende de 9 unidades en vez de 4 por el emparejamiento de átomos.

## Goal

_Describe the concrete result this task must produce._

El emparejamiento de átomos (explicit_atoms, explicit_refs, atom_*, coverage*, spec_view*, store_reader, store_documents, store_edges, matching_findings, unknown_atom_error) vive en un eje propio en contracts/layers.toml; recuperacion vuelve a sus 4 dependencias medidas y sigue siendo extraíble.

## Scope

_State what is in scope and what is out of scope._

Entra: mover los módulos de átomos a un subpaquete propio (p. ej. sldb.api.matching.atoms o un eje nuevo) manteniendo los nombres públicos exportados desde sldb.api.matching, y ajustar ejes y cuentas medidas. Sale: cambiar la lógica del emparejamiento.

## Implementation Path

_Outline the expected implementation route or affected surface._

Medir con tools/check.sh las dependencias de recuperacion; crear el eje o subpaquete; reexportar desde sldb.api.matching; ajustar contracts/layers.toml con comentario medido.

## Validation

_List the checks required before this task can close._

- TMPDIR=/dev/shm pytest -q tests/matching/ tests/test_clean_code_rules.py; bash tools/check.sh --fast

## Done When

_Name the observable condition that makes the task complete._

tools/check.sh --fast en PASS con recuperacion extractable_today=true y sus dependencias medidas como antes de D4; tests/matching/ en verde.
