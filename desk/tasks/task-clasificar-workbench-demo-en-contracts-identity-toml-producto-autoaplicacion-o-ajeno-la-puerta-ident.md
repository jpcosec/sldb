---
sldb:
  by: agent
  at: '2026-11-20T07:13:41Z'
  authority: generated
  via: create_document
id: task-clasificar-workbench-demo-en-contracts-identity-toml-producto-autoaplicacion-o-ajeno-la-puerta-ident
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
task_type: task.decision
inherits_from: []
inherit_acceptance_context: false
atoms: []
---

# Clasificar workbench_demo en contracts/identity.toml (producto, autoaplicación o ajeno): la puerta identidad de check.sh está en rojo

## Rationale

_Explain why this task exists or the business driver behind it._

2026-11-20: el directorio workbench_demo entró a la raíz de sldb con 562847e2 ('feat(surface): asistente y tour del workbench, DESIGN/PRODUCT y store demo workbench', mergeado por github-actions). tools/check_identity.py exige que todo directorio versionado de primer nivel esté clasificado en contracts/identity.toml, así que 'bash tools/check.sh --fast' (quick_gates de todos los ejecutores) sale rc 1 en la puerta identidad. Mientras tanto el coordinador autoriza commitear con esa puerta en rojo, tarea por tarea.

## Goal

_Describe the concrete result this task must produce._

JP o el dueño de surface decide qué es workbench_demo: producto (sldb lo distribuye), autoaplicación (sldb usado sobre sí mismo) o ajeno (va en contract foreign, o se mueve fuera de la raíz, por ejemplo bajo surface/), y se clasifica en contracts/identity.toml. Con eso, check.sh --fast vuelve a 0.

## Scope

_State what is in scope and what is out of scope._

Solo la decisión y la línea en contracts/identity.toml, o mover el directorio si esa es la decisión.

## Implementation Path

_Outline the expected implementation route or affected surface._



## Validation

_List the checks required before this task can close._

- 

## Done When

_Name the observable condition that makes the task complete._
