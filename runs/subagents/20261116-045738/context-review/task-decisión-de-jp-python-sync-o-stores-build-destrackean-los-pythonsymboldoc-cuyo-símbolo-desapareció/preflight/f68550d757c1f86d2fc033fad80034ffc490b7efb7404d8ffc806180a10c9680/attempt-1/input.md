FILE:desk/tasks/task-decisión-de-jp-python-sync-o-stores-build-destrackean-los-pythonsymboldoc-cuyo-símbolo-desapareció.md
---
sldb:
  by: agent
  at: '2026-11-16T04:16:42Z'
  authority: generated
  via: create_document
id: task-decisión-de-jp-python-sync-o-stores-build-destrackean-los-pythonsymboldoc-cuyo-símbolo-desapareció
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
files:
- docs/self-documentation.md
task_type: task.decision
inherits_from: []
inherit_acceptance_context: false
atoms: []
from_drawer: desk/drawer/tasks/task-python-sync-no-destrackea-un-pythonsymboldoc-cuyo-s-mbolo-desapareci.md
---

# Decisión de JP: python-sync o stores build destrackean los PythonSymbolDoc cuyo símbolo desapareció

## Rationale

_Explain why this task exists or the business driver behind it._

selfdoc python-sync escribe PythonSymbolDoc pero nunca destrackea (write_python_plans, src/sldb/cli/commands/selfdoc_python.py:69; no hay untrack en src/sldb/selfdoc). El contrato actual los conserva a propósito: src/sldb/selfdoc/report.py:32 "Removed documents are retained" y el test tests/selfdoc/test_sync.py::test_removed_commands_are_reported_and_retained. Resultado: cuando c420809c borró el journal quedaron 108 PythonSymbolDoc huérfanos (stores build en sitio: undeclared 108), limpiados a mano con sldb docs untrack (dfa5c504; otro en 641ecdfa). Destrackear cambia la semántica (borra documentos trackeados derivados), por eso es del dueño. Origen: drawer desk/drawer/tasks/task-python-sync-no-destrackea-un-pythonsymboldoc-cuyo-s-mbolo-desapareci.md.

## Goal

_Describe the concrete result this task must produce._

JP decide (a) python-sync destrackea los PythonSymbolDoc de su system cuyo símbolo ya no existe y conserva los documentos de comandos y superficies escritos por personas; (b) también destrackea los de comandos y superficies; o (c) se mantiene la retención y solo se reportan. La decisión queda en docs/self-documentation.md, sección "Símbolos que desaparecen", y si es (a) o (b) se crea la tarea de código que cambia report.py y test_sync.py.

## Scope

_State what is in scope and what is out of scope._

Entra: presentar las tres opciones; recomendación del coordinador: (a), porque los PythonSymbolDoc son generados (knowledge/symbols/ está en derived) y los de comandos y superficies los escriben personas. Registrar el recibo owner (dispose accepted de JP), escribir la sección, crear la tarea de código si corresponde. No entra: implementar; la alerta de stores check sobre documentos derivados ausentes es otra tarea.

## Implementation Path

_Outline the expected implementation route or affected surface._

1) Leer report.py, selfdoc_python.py, tests/selfdoc/test_sync.py y docs/self-documentation.md. 2) Pedir decisión. 3) Escribir la sección. 4) Crear la tarea de código con validación TMPDIR=/dev/shm pytest -q tests/selfdoc/test_sync.py.

## Validation

_List the checks required before this task can close._

- grep -n 'Símbolos que desaparecen' docs/self-documentation.md

## Done When

_Name the observable condition that makes the task complete._

La sección existe con la opción y la fecha; recibo owner aceptado por JP; tarea de código creada si es (a) o (b); commit del doc.

FILE:instruccion
Preflight solo-TaskDoc de la tarea task-decisión-de-jp-python-sync-o-stores-build-destrackean-los-pythonsymboldoc-cuyo-símbolo-desapareció: reformula el encargo tal como lo leería un ejecutor sin ningún otro contexto, lista ambigüedades con cita textual del input y da el DRY-RUN sin ejecutar nada. No ejecutes nada.

