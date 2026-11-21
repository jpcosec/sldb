---
sldb:
  by: agent
  at: '2026-11-21T04:16:27Z'
  authority: generated
  via: create_document
id: task-el-merge-driver-de-sldb-se-instala-solo-en-un-clon-que-tiene-las-lineas-de-gitattributes-pero-no-la
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

# El merge driver de sldb se instala solo en un clon que tiene las líneas de .gitattributes pero no la config de git

## Rationale

_Explain why this task exists or the business driver behind it._

2026-11-21: en /mnt/ssd/proyectos/SLDB_1/sldb, .gitattributes tenía merge=sldb pero .git/config no tenía merge.sldb.driver, y un merge de origin/main dejó store.yaml, store_index.yaml y un modelo en conflicto como texto. 'sldb stores merge-driver --install' puso las 2 claves y el merge rehecho resolvió solo. El auto-install de 9007f78a/5900a3eb no se disparó en este clon (nota del inbox 20261121-011013).

## Goal

_Describe the concrete result this task must produce._

Cualquier comando de sldb que abra un store dentro de un repo git cuyo .gitattributes tenga líneas merge=sldb, y cuya config no tenga merge.sldb.driver, instala las claves de git (lo mismo que hace --install con la config, sin tocar .gitattributes) y lo dice una vez por stderr. stores check emite un alert stores/merge-driver-missing si no pudo instalarlo.

## Scope

_State what is in scope and what is out of scope._

Dentro: el auto-install existente (buscar dónde lo dejó 9007f78a/5900a3eb), su test y CHANGELOG. Fuera: cambiar el driver.

## Implementation Path

_Outline the expected implementation route or affected surface._

p1: test que falla antes: repo temporal con .gitattributes merge=sldb y sin config; sldb stores check deja merge.sldb.driver puesto. p2: implementar en el punto de auto-install existente, ampliando la condición. p3: CHANGELOG; commit desde tu worktree con 'git commit -- <rutas>' y trailer Task-Id.

## Validation

_List the checks required before this task can close._

- TMPDIR=/tmp python -m pytest -q -p no:cacheprovider -k merge_driver

## Done When

_Name the observable condition that makes the task complete._

El test nuevo y los tests del merge driver pasan.
