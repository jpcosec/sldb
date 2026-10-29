---
id: task-cerrar-task-sldb-serve-sldb-serve-ya-existe
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
task_type: ''
inherits_from: []
inherit_acceptance_context: false
atoms: []
---

# Cerrar TASK-sldb-serve: sldb serve ya existe

## Rationale

_Explain why this task exists or the business driver behind it._

TASK-sldb-serve.md quedó en la raíz del repo como pedido suelto de otro worktree (iso-lab). El servidor existe en src/sldb/cli/serve/ y el archivo huérfano confunde: una tarea integrada nunca aparece como pendiente.

## Goal

_Describe the concrete result this task must produce._

Verificar que lo que TASK-sldb-serve.md pide está implementado y probado, dejar la evidencia en el desk y retirar el archivo de la raíz.

## Scope

_State what is in scope and what is out of scope._

Solo verificación y evidencia: correr los tests de serve, comparar los endpoints pedidos (/health, /schema, /graph, POST /save, /kgdb/snapshot opcional) con src/sldb/cli/serve/routes.py, escribir runs/subagents/<run>/result-summary.md. Sin cambios de código. git rm TASK-sldb-serve.md lo hace el supervisor al cerrar.

## Implementation Path

_Outline the expected implementation route or affected surface._

Agente Scion (template deskops-executor) ejecuta la verificación; el supervisor cierra con deskops closeout commit.

## Validation

_List the checks required before this task can close._

- python -m pytest -q tests -k serve

## Done When

_Name the observable condition that makes the task complete._

result-summary.md lista endpoint pedido -> ruta implementada -> test; los tests de serve pasan; TASK-sldb-serve.md ya no existe en la raíz.
