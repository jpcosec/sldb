---
id: task-stores-check-escala-mal-con-el-inventario-de-símbolos-python
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
task_type: implementation
inherits_from: []
inherit_acceptance_context: false
atoms: []
---

# stores check escala mal con el inventario de símbolos Python

## Rationale

_Explain why this task exists or the business driver behind it._

Con los 2482 PythonSymbolDoc (4d1126b2) el store pasó de 1553 a 2756 documentos y stores check de 25 s a 43 s; --quiet de 5 s a 10 s. Medido el 2026-10-18 en el store de sldb: diagnose 8.7 s, structural_noise 7.4 s, rewrite_loss 23.2 s.

## Goal

_Describe the concrete result this task must produce._

Que stores check completo del store de sldb vuelva a quedar bajo ~20 s sin perder hallazgos.

## Scope

_State what is in scope and what is out of scope._

Las tres pasadas re-extraen o re-renderizan cada documento por separado: rewrite_loss renderiza y re-extrae todo, structural_noise vuelve a parsear, diagnose extrae. Opciones: una sola extracción por documento compartida por las tres, cachear rewrite_loss por source_hash+contract_hash (un documento que no cambió no puede perder contenido nuevo), o saltar los modelos generados por selfdoc (PythonSymbolDoc, CliCommandDoc) cuyo texto lo escribe el propio renderer.

## Implementation Path

_Outline the expected implementation route or affected surface._

src/sldb/api/stores/scan_rewrite_loss.py

## Validation

_List the checks required before this task can close._

- .venv/bin/python -m pytest -q tests/api/test_rewrite_loss.py
- /usr/bin/time sldb stores check --store .sldb --pythonpath .

## Done When

_Name the observable condition that makes the task complete._

stores check completo del store de sldb bajo ~20 s, con los mismos hallazgos que hoy; un test fija que una segunda corrida sobre un store sin cambios no re-renderiza.
