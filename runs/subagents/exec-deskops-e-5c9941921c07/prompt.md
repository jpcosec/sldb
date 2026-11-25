Task: task-una-regla-puede-preguntar-por-los-tags-semanticos-del-modelo-de-un-documento-y-por-los-de-sus-ancest
Title: una regla puede preguntar por los tags semánticos del modelo de un documento y por los de sus ancestros en el DAG
Status: draft
Current node: ritual-execution
Task type: task.code
Lifecycle gates:
- task_activates -> ritual-testing: closed [(none)]
  post-hook encola-reap-del-ejecutor: deskops queue add dispatch-reap --root .
  post-hook encola-tester: deskops queue add dispatch-tester --root .
  blocked by: error: [rules/rule-activation-task-code] TaskCodeDoc:task-una-regla-puede-preguntar-por-los-tags-semanticos-del-modelo-de-un-documento-y-por-los-de-sus-ancest: Una tarea task.code se activa con recibos preflight y bundle aceptados e intactos y sus dependencias cerradas. | any(^subject: anchor_state = "intact" and verdict = "accepted" and kind = "preflight") (seen: {}) (witness: ReviewDoc:review-task-una-regla-puede-preguntar-por-los-tags-semanticos-del-modelo-de-un-documento-y-por-los-de-sus-ancest-bundle-1 {"anchor_state":"changed"})

---
sldb:
  by: agent
  at: '2026-11-25T18:24:20Z'
  authority: generated
  via: save_document_payload
id: task-una-regla-puede-preguntar-por-los-tags-semanticos-del-modelo-de-un-documento-y-por-los-de-sus-ancest
status: draft
summary: ''
tags: []
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

# una regla puede preguntar por los tags semánticos del modelo de un documento y por los de sus ancestros en el DAG

## Rationale

_Explain why this task exists or the business driver behind it._

Pedido de specIR (desk/drawer/plans/pedidos-de-specir-y-graph-ui/). El lenguaje de reglas no puede leer los tags que salen de __semantics__ ni recorrer el DAG semántico, así que una regla se escribe por nombre de modelo. Revisar un estándar pide reglas por concepto, que valgan para todos los modelos que lo implementan.

## Goal

_Describe the concrete result this task must produce._

Un predicado del lenguaje de reglas que sea verdadero cuando el modelo del documento tiene un tag dado o uno que desciende de él en el DAG semántico.

## Scope

_State what is in scope and what is out of scope._

Dentro: el lenguaje de reglas y su evaluador. Fuera: reglas concretas de specIR, cambios al DAG semántico.

## Implementation Path

_Outline the expected implementation route or affected surface._

Leer docs/architecture/rules-language.md, rules.md y tags.md, y sldb semantic --help. El predicado usa la relación de padre y equivalencia que el DAG ya resuelve; no se calcula otra.

Aclaraciones de la revisión: Dirección: el predicado casa un documento cuyo modelo declara el tag Q o un tag que desciende de Q (Q es ancestro); es decir, pedir el tag padre casa modelos con tags hijos, no al revés. Equivalencia = las equivalencias de tags que ya resuelve el DAG (sldb semantic, docs/architecture/tags.md); un tag equivalente a Q cuenta como Q. Un tag que no existe en el DAG es un error al validar la regla, con el nombre del tag. Docs en sldb/docs/architecture/ (rules-language.md, rules.md, tags.md). Nombre y sintaxis del predicado siguiendo los predicados existentes del lenguaje de reglas, documentado en rules-language.md. Alcance: predicado, validación y tests; ninguna RuleDoc real. No poner Task-Id en el commit de código.

## Validation

_List the checks required before this task can close._

- python -m pytest -q tests/test_rules_semantic_tag_predicate.py
- python -m pytest -q tests -k rules

## Done When

_Name the observable condition that makes the task complete._

Una RuleDoc con el predicado casa un documento cuyo modelo declara el tag, casa otro cuyo modelo declara un tag hijo, y no casa uno sin relación. Un tag que no existe en el DAG se informa al validar la regla. rules-language.md describe el predicado con un ejemplo.

## Entrega del ejecutor

Al terminar, commitea solo los archivos que cambiaste para la tarea, nombrados uno por uno (los mismos que listas en result-summary.md):

    git add <ruta> <ruta> ...
    git commit -m "<resumen>" -m "Task-Id: task-una-regla-puede-preguntar-por-los-tags-semanticos-del-modelo-de-un-documento-y-por-los-de-sus-ancest"

Nunca uses `git add -A`, `git add -u` sobre todo el arbol ni `git stash`: puede haber trabajo ajeno sin commitear. No hagas push. Recien despues ejecuta `deskops advance task`.

## Temporales de pytest

Antes de cualquier pytest exporta, para que sus temporales caigan en el /tmp del contenedor (muere con el agente) y no en el /dev/shm del host:

    export PYTEST_ADDOPTS="--basetemp=/tmp/pytest-deskops-e-5c9941921c07"

## Gates rapidos del desk

Antes del commit corre, con el python del venv (/tmp/ws-venv en PATH):

    bash tools/check.sh --fast

Debe terminar con rc 0 antes de commitear; si falla, corrige y repite. Anota el comando y su rc en validation.log.

## Tu worktree

Tu codigo vive en un worktree propio, en la rama `deskops/deskops-e-5c9941921c07`:

    /mnt/ssd/proyectos/SLDB_1/sldb/.worktrees/deskops-e-5c9941921c07

Haz `cd` ahi: edita, corre los tests y commitea ahi (git add / git commit), no en el checkout principal /mnt/ssd/proyectos/SLDB_1/sldb. Las operaciones de desk (`deskops ... --root /mnt/ssd/proyectos/SLDB_1/sldb`, evidencia en runs/subagents/..., `deskops advance task`) siguen usando el checkout principal. Al terminar, reap trae tus commits a la rama principal y borra el worktree.
