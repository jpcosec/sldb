Task: task-check-edges-clasifica-como-stale-propio-los-de-stores-enlazados-cuyo-nombre-lleva-dos-puntos-inbox-2
Title: check_edges clasifica como stale propio los de stores enlazados cuyo nombre lleva dos puntos (inbox 20261115-015936)
Status: draft
Current node: ritual-execution
Task type: task.debug
Lifecycle gates:
- task_activates -> ritual-testing: open [(none)]
  post-hook encola-reap-del-ejecutor: deskops queue add dispatch-reap --root .
  post-hook encola-tester: deskops queue add dispatch-tester --root .

---
sldb:
  by: agent
  at: '2026-11-19T06:45:29Z'
  authority: generated
  via: save_document_payload
id: task-check-edges-clasifica-como-stale-propio-los-de-stores-enlazados-cuyo-nombre-lleva-dos-puntos-inbox-2
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
task_type: task.debug
inherits_from: []
inherit_acceptance_context: false
atoms: []
---

# check_edges clasifica como stale propio los de stores enlazados cuyo nombre lleva dos puntos (inbox 20261115-015936)

## Rationale

_Explain why this task exists or the business driver behind it._

En un repo con stores enlazados, sldb edges check reporta cientos de stale propios y ok=False mientras --local da OK.

## Goal

_Describe the concrete result this task must produce._

Clasificar el stale por el store dueño del nodo, no por el conteo de ':'.

## Scope

_State what is in scope and what is out of scope._

Bug del inbox sldb 20261115-015936, verificado hoy en HEAD: check_edges separa linked_stale con un conteo de ':' igual a 2, y un documento de un store enlazado con ':' en su nombre cuenta como propio. Reproducir con un store enlazado cuyo documento lleve ':' en el nombre, antes con caché frío y caliente; corregir clasificando por el store dueño; test de regresión.

## Implementation Path

_Outline the expected implementation route or affected surface._

Ubicaciones (sldb HEAD al despachar): la clasificación está en src/sldb/api/edges/check_edges.py:29 (linked_stale = [s for s in index.stale if s.count(':') == 2]); los ids de los stores enlazados se califican en src/sldb/store/edge_index/federation.py, qualify_id (líneas 30-38: 'store:Model:nombre', y solo si el nombre no nombra ya un store). p1: test que falla antes en tests/test_api_edges.py: un store con un store enlazado, un documento propio y uno enlazado, ambos stale y con un ':' en el nombre, y check_edges(include_linked=True) los pone en stale y linked_stale respectivamente (hoy los cruza). Ver runs/subagents/20261119-repro-check-edges/. p2: clasificar por el store dueño y no por el conteo de ':': el índice federado sabe de qué store viene cada nodo (from_store en las contribuciones de qualify, o los nombres de los stores enlazados del índice); usar eso. Si el dato no llega a index.stale, agregarlo donde se arma stale, sin cambiar el formato de los ids. p3: CHANGELOG. p4: quick_gates del desk (bash tools/check.sh --fast) antes del commit, con rutas nombradas y Task-Id.

## Validation

_List the checks required before this task can close._

- TMPDIR=/tmp python -m pytest -q -p no:cacheprovider tests/test_api_edges.py
- TMPDIR=/tmp python -m pytest -q -p no:cacheprovider tests/test_edge_effects.py
- bash tools/check.sh --fast

## Done When

_Name the observable condition that makes the task complete._

El test de regresión pasa; EdgeCheckReport.ok coincide entre include_linked=False y --local para ese caso; suite de a un archivo, tools/check.sh y stores build --check.

## Entrega del ejecutor

Al terminar, commitea solo los archivos que cambiaste para la tarea, nombrados uno por uno (los mismos que listas en result-summary.md):

    git add <ruta> <ruta> ...
    git commit -m "<resumen>" -m "Task-Id: task-check-edges-clasifica-como-stale-propio-los-de-stores-enlazados-cuyo-nombre-lleva-dos-puntos-inbox-2"

Nunca uses `git add -A`, `git add -u` sobre todo el arbol ni `git stash`: puede haber trabajo ajeno sin commitear. No hagas push. Recien despues ejecuta `deskops advance task`.

## Gates rapidos del desk

Antes del commit corre, con el python del venv (/tmp/ws-venv en PATH):

    bash tools/check.sh --fast

Debe terminar con rc 0 antes de commitear; si falla, corrige y repite. Anota el comando y su rc en validation.log.
