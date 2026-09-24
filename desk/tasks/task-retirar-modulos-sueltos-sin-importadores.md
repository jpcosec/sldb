---
id: task-retirar-modulos-sueltos-sin-importadores
status: draft
summary: ''
tags:
- workspace:desk
- artifact:task
routine: routine-task-retirar-modulos-sueltos-sin-importadores
current_node: checklist-task-retirar-modulos-sueltos-sin-importadores-execution-ready
history: []
references: []
depends_on: []
pills: []
files: []
checklists:
- checklist-task-retirar-modulos-sueltos-sin-importadores-execution-ready
- checklist-task-retirar-modulos-sueltos-sin-importadores-testing-ready
- checklist-task-retirar-modulos-sueltos-sin-importadores-closeout-ready
task_type: implementation
inherits_from: []
inherit_acceptance_context: false
atoms: []
---

# Retirar modulos sueltos sin importadores

## Rationale

_Explain why this task exists or the business driver behind it._

Cinco modulos sin consumidores reales, confirmados por censo AST: doc_helpers.py (100 lin, cero menciones en todo el repo, duplica core.exceptions + runtime.validation), predicates_format.py (42 lin, cero menciones), model_update.py (67 lin, solo lo toca un monkeypatch en tests/test_cli_v2.py:1664 que es INERTE porque 'models update' va por commands/models.py:37-39 -> ModelCLI), model_source.py y federated_utils.py (compat bridges cuyos consumidores ya migraron a api/model_drafts/source_location.py y api/model_registry/federated_lookup.py).

## Goal

_Describe the concrete result this task must produce._

Borrar los 5 modulos (230 lineas) y limpiar el monkeypatch inerte del test.

## Scope

_State what is in scope and what is out of scope._

IN: cli/commands/doc_helpers.py, cli/commands/predicates_format.py, cli/commands/model_update.py, cli/commands/model_source.py, cli/federated_utils.py, y el monkeypatch de tests/test_cli_v2.py:1664. OUT: no tocar los modulos destino a los que ya migraron los consumidores.

## Implementation Path

_Outline the expected implementation route or affected surface._

Uno por uno: censo AST de importadores, borrar, correr suite. Para model_update.py, ademas reescribir el test que lo monkeypatchea para que ejercite la ruta REAL (ModelCLI), no para que desaparezca la cobertura.

## Validation

_List the checks required before this task can close._

- PYTHONPATH=src python -m pytest -q

## Done When

_Name the observable condition that makes the task complete._

pytest completo en 1015 passed 0 failed; los 5 modulos no existen; el test de models update ejercita ModelCLI de verdad.
