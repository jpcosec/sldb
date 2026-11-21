---
sldb:
  by: agent
  at: '2026-11-21T06:31:14Z'
  authority: generated
  via: save_document_payload
id: task-respaldar-562847e2-surface-asistente-tour-y-workbench-demo-con-la-suite-completa-y-sldb-stores-build
status: draft
summary: ''
tags:
- workspace:desk
- artifact:task
current_node: ritual-execution
history: []
references:
- desk/inbox/20261121-032515-suggestion-trabajo-de-surface-562847e2-entr-a-main-sin-tarea-ni-suite-completa-gitattributes-y-herdr-coordination-md.md
depends_on: []
pills: []
files: []
task_type: task.code
inherits_from: []
inherit_acceptance_context: false
atoms: []
---

# Respaldar 562847e2 (surface: asistente, tour y workbench_demo) con la suite completa y sldb stores build --check, e ignorar .herdr-coordination.md

## Rationale

_Explain why this task exists or the business driver behind it._

Nota de JP desk/inbox/20261121-032515 (sesión local 2026-11-20): 562847e2 entró directo a main sin tarea; solo se verificó con tsc, vitest de surface y tools/check.sh --fast. No se corrió la suite completa de sldb ni sldb stores build --check. Además .herdr-coordination.md queda sin trackear y sin ignorar. La decisión de si workbench_demo/ queda versionado ya la cubre task-clasificar-workbench-demo-en-contracts-identity-toml-producto-autoaplicacion-o-ajeno-la-puerta-ident; el auto-install del merge driver (.gitattributes de 830dfe08) lo cubre task-el-merge-driver-de-sldb-se-instala-solo-en-un-clon-que-tiene-las-lineas-de-gitattributes-pero-no-la.

## Goal

_Describe the concrete result this task must produce._

Dejar constancia verificada de que main con 562847e2 pasa la suite completa de sldb (pytest -n 4) y sldb stores build --check; corregir lo que falle por ese commit; agregar .herdr-coordination.md al .gitignore de sldb.

## Scope

_State what is in scope and what is out of scope._

Dentro: correr la suite completa y stores build --check sobre el worktree que dispatch le da al ejecutor; arreglar fallas atribuibles a 562847e2 (surface/, workbench_demo/); una línea en .gitignore para .herdr-coordination.md. Fuera: decidir la clasificación de workbench_demo (es la tarea.decision citada) y la falla conocida del gate identidad de tools/check.sh --fast por workbench_demo (excepción autorizada, task.decision f055723d).

## Implementation Path

_Outline the expected implementation route or affected surface._

1) TMPDIR=/dev/shm pytest -n 4 -q en la raíz del worktree. 2) sldb stores build --check. 3) Si algo falla por surface/ o workbench_demo/, corregirlo con tests. 4) Agregar '.herdr-coordination.md' a .gitignore. Commit con trailer 'Task-Id: <id>' en el cuerpo.

## Validation

_List the checks required before this task can close._

- TMPDIR=/dev/shm pytest -n 4 -q
- sldb stores build --check
- git check-ignore .herdr-coordination.md

## Done When

_Name the observable condition that makes the task complete._

La suite completa de sldb y sldb stores build --check salen rc 0 en el worktree (salvo la puerta identidad ya exceptuada), y git status no muestra .herdr-coordination.md como no trackeado.
