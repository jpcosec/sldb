---
sldb:
  by: agent
  at: '2026-11-22T12:15:35Z'
  authority: generated
  via: create_document
id: task-heading-scan-scan-heading-bodies-baja-a-10-lineas-de-logica-regla-de-codigo-limpio
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

# heading_scan: scan_heading_bodies baja a 10 líneas de lógica (regla de código limpio)

## Rationale

_Explain why this task exists or the business driver behind it._

2026-11-22: la tarea del guard de sobrescritura con pérdida agotó sus intentos de tester. El reap perdió el commit del intento 2 y el coordinador lo recuperó y trajo a main como 074bc3bc. Funciona: tests/api/test_lossy_overwrite_content.py da 6 passed y tests/api 649 passed (verificación en runs/subagents/20261122-verif-guard-lossy/verificacion.log). Pero tests/test_clean_code_rules.py falla: 'Function scan_heading_bodies in heading_scan.py has 11 lines of logic (max 10)'. Bloquea el integrate de sldb.

## Goal

_Describe the concrete result this task must produce._

src/sldb/api/documents/heading_scan.py cumple tests/test_clean_code_rules.py: scan_heading_bodies queda en 10 líneas de lógica o menos, partiéndola en una auxiliar privada del mismo archivo, sin cambiar el comportamiento.

## Scope

_State what is in scope and what is out of scope._

Dentro: src/sldb/api/documents/heading_scan.py. Fuera: cambiar tests o comportamiento.

## Implementation Path

_Outline the expected implementation route or affected surface._

p1: partir scan_heading_bodies. p2: correr tests/test_clean_code_rules.py, tests/api/test_lossy_overwrite_content.py y tests/test_extraction_segments.py, en verde. p3: bash tools/check.sh --fast en verde salvo 'identidad' por workbench_demo (excepción f055723d). p4: commit desde el worktree que dispatch te da con 'git commit -- src/sldb/api/documents/heading_scan.py' y el trailer 'Task-Id: <id de esta tarea>' en el cuerpo. Las métricas son las del test: líneas de lógica = del primer al último statement del cuerpo, sin docstring.

## Validation

_List the checks required before this task can close._

- TMPDIR=/tmp python -m pytest -q -p no:cacheprovider tests/test_clean_code_rules.py tests/api/test_lossy_overwrite_content.py

## Done When

_Name the observable condition that makes the task complete._

Los tres archivos de tests pasan.
