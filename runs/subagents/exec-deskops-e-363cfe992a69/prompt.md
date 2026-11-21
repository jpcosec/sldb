Task: task-el-generador-del-golden-de-d2-deja-de-importar-spec2viz-para-que-el-retiro-de-spec2viz-no-cuente-a-s
Title: El generador del golden de D2 deja de importar spec2viz, para que el retiro de spec2viz no cuente a sldb como consumidor
Status: draft
Current node: ritual-execution
Task type: task.code
Lifecycle gates:
- task_activates -> ritual-testing: open [(none)]
  post-hook encola-reap-del-ejecutor: deskops queue add dispatch-reap --root .
  post-hook encola-tester: deskops queue add dispatch-tester --root .

---
sldb:
  by: agent
  at: '2026-11-21T02:15:41Z'
  authority: generated
  via: create_document
id: task-el-generador-del-golden-de-d2-deja-de-importar-spec2viz-para-que-el-retiro-de-spec2viz-no-cuente-a-s
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

# El generador del golden de D2 deja de importar spec2viz, para que el retiro de spec2viz no cuente a sldb como consumidor

## Rationale

_Explain why this task exists or the business driver behind it._

2026-11-21: 'specir retirement check' de IR (gate final IR13) cuenta una sola dependencia de spec2viz en sldb: runs/subagents/20261116-exec-oraculo-d2/gen_golden.py:5 ('from spec2viz.generators import python_ast'). Es el script que congeló el oráculo de D2 en un golden (ce0bd384), y el acta de retiro de IR (docs/spec2viz/acta-de-retiro.md, punto 1 de 'Lo que falta') espera que sldb lo resuelva y responda con el commit.

## Goal

_Describe the concrete result this task must produce._

runs/subagents/20261116-exec-oraculo-d2/gen_golden.py ya no importa spec2viz: o se borra (el golden ya está commiteado en ce0bd384 y el script no lo usa ningún test), o se deja un README en esa carpeta que diga cómo se generó, sin el import. Después, el desk de IR recibe un aviso con el commit, con deskops message send --to IR.

## Scope

_State what is in scope and what is out of scope._

Dentro: runs/subagents/20261116-exec-oraculo-d2/gen_golden.py (borrarlo, con git rm) y, si hace falta, un README.md en la misma carpeta. Fuera: el golden y los tests de D2.

## Implementation Path

_Outline the expected implementation route or affected surface._

p1: 'grep -rn gen_golden' en src y tests para confirmar que nada lo usa. p2: 'git rm' del script, y un README.md de 3 líneas en la carpeta que diga que generó el golden de ce0bd384 a partir de spec2viz y que se retiró por el retiro de spec2viz. p3: 'TMPDIR=/tmp python -m pytest -q -p no:cacheprovider tests/notations/test_component_spec_python.py' en verde. p4: commit con 'git commit -- <rutas>' y trailer Task-Id.

## Validation

_List the checks required before this task can close._

- TMPDIR=/tmp python -m pytest -q -p no:cacheprovider tests/notations/test_component_spec_python.py

## Done When

_Name the observable condition that makes the task complete._

El script no existe o no importa spec2viz; el test de D2 pasa.

## Entrega del ejecutor

Al terminar, commitea solo los archivos que cambiaste para la tarea, nombrados uno por uno (los mismos que listas en result-summary.md):

    git add <ruta> <ruta> ...
    git commit -m "<resumen>" -m "Task-Id: task-el-generador-del-golden-de-d2-deja-de-importar-spec2viz-para-que-el-retiro-de-spec2viz-no-cuente-a-s"

Nunca uses `git add -A`, `git add -u` sobre todo el arbol ni `git stash`: puede haber trabajo ajeno sin commitear. No hagas push. Recien despues ejecuta `deskops advance task`.

## Gates rapidos del desk

Antes del commit corre, con el python del venv (/tmp/ws-venv en PATH):

    bash tools/check.sh --fast

Debe terminar con rc 0 antes de commitear; si falla, corrige y repite. Anota el comando y su rc en validation.log.

## Tu worktree

Tu codigo vive en un worktree propio, en la rama `deskops/deskops-e-363cfe992a69`:

    /mnt/ssd/proyectos/SLDB_1/sldb/.worktrees/deskops-e-363cfe992a69

Haz `cd` ahi: edita, corre los tests y commitea ahi (git add / git commit), no en el checkout principal /mnt/ssd/proyectos/SLDB_1/sldb. Las operaciones de desk (`deskops ... --root /mnt/ssd/proyectos/SLDB_1/sldb`, evidencia en runs/subagents/..., `deskops advance task`) siguen usando el checkout principal. Al terminar, reap trae tus commits a la rama principal y borra el worktree.
