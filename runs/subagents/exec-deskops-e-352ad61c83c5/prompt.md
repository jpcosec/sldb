Task: task-los-specs-de-docs-architecture-spec2viz-se-construyen-con-specir-catalog-build-y-se-sincronizan-con
Title: Los specs de docs/architecture/spec2viz se construyen con specir catalog build y se sincronizan con sldb notations sync --catalog
Status: draft
Current node: ritual-execution
Task type: task.docs
Lifecycle gates:
- task_activates -> ritual-testing: open [(none)]
  post-hook encola-reap-del-ejecutor: deskops queue add dispatch-reap --root .
  post-hook encola-tester: deskops queue add dispatch-tester --root .

---
sldb:
  by: agent
  at: '2026-11-16T02:20:11Z'
  authority: generated
  via: create_document
id: task-los-specs-de-docs-architecture-spec2viz-se-construyen-con-specir-catalog-build-y-se-sincronizan-con
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
task_type: task.docs
inherits_from: []
inherit_acceptance_context: false
atoms: []
---

# Los specs de docs/architecture/spec2viz se construyen con specir catalog build y se sincronizan con sldb notations sync --catalog

## Rationale

_Explain why this task exists or the business driver behind it._

Decisión de JP 2026-11-15 (G7 aceptada y recomendación del coordinador aceptada): el YAML del spec queda subordinado al grafo; los specs existentes se quedan como fixtures durante la paridad y dejan de depender de spec2viz para construirse.

## Goal

_Describe the concrete result this task must produce._

docs/architecture/spec2viz/vistas.yml y sus specs se construyen con specir catalog build y se sincronizan al store con sldb notations sync --catalog; ninguna instrucción ni contrato de sldb invoca spec2viz para ellos.

## Scope

_State what is in scope and what is out of scope._

Entra: la instrucción de build y sync de esos specs, contracts/identity.toml:299 y la documentación que nombra spec2viz catalog build. Sale: mover o renombrar la carpeta (se decide al archivar spec2viz).

## Implementation Path

_Outline the expected implementation route or affected surface._

Reemplazar las invocaciones de spec2viz catalog build por specir catalog build y sldb notations sync --catalog; actualizar identity.toml y la doc; comprobar con sldb notations sync --catalog --check.

## Validation

_List the checks required before this task can close._

- sldb notations sync --catalog docs/architecture/spec2viz/vistas.yml --check; bash tools/check.sh --fast

## Done When

_Name the observable condition that makes the task complete._

grep de spec2viz en las instrucciones de build de docs/architecture/spec2viz y en contracts/identity.toml sin coincidencias de invocación; sldb notations sync --catalog --check limpio.

## Entrega del ejecutor

Al terminar, commitea solo los archivos que cambiaste para la tarea, nombrados uno por uno (los mismos que listas en result-summary.md):

    git add <ruta> <ruta> ...
    git commit -m "<resumen>" -m "Task-Id: task-los-specs-de-docs-architecture-spec2viz-se-construyen-con-specir-catalog-build-y-se-sincronizan-con"

Nunca uses `git add -A`, `git add -u` sobre todo el arbol ni `git stash`: puede haber trabajo ajeno sin commitear. No hagas push. Recien despues ejecuta `deskops advance task`.

## Gates rapidos del desk

Antes del commit corre, con el python del venv (/tmp/ws-venv en PATH):

    bash tools/check.sh --fast

Debe terminar con rc 0 antes de commitear; si falla, corrige y repite. Anota el comando y su rc en validation.log.

## Tu worktree

Tu codigo vive en un worktree propio, en la rama `deskops/deskops-e-352ad61c83c5`:

    /mnt/ssd/proyectos/SLDB_1/sldb/.worktrees/deskops-e-352ad61c83c5

Haz `cd` ahi: edita, corre los tests y commitea ahi (git add / git commit), no en el checkout principal /mnt/ssd/proyectos/SLDB_1/sldb. Las operaciones de desk (`deskops ... --root /mnt/ssd/proyectos/SLDB_1/sldb`, evidencia en runs/subagents/..., `deskops advance task`) siguen usando el checkout principal. Al terminar, reap trae tus commits a la rama principal y borra el worktree.
