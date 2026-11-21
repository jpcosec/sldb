Task: task-el-tercer-valor-del-lenguaje-de-predicados-incomplete-se-demuestra-alcanzable-con-un-test-sobre-dato
Title: El tercer valor del lenguaje de predicados (incomplete) se demuestra alcanzable con un test sobre datos reales o se retira
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
  at: '2026-11-17T15:13:46Z'
  authority: generated
  via: save_document_payload
id: task-el-tercer-valor-del-lenguaje-de-predicados-incomplete-se-demuestra-alcanzable-con-un-test-sobre-dato
status: draft
summary: ''
tags:
- workspace:desk
- artifact:task
- host:robocop2
current_node: ritual-execution
history: []
references:
- docs/architecture/rules-language.md
depends_on: []
pills: []
files:
- src/sldb/api/where.py
- docs/architecture/rules-language.md
- tests/test_predicates_cli.py
- CHANGELOG.md
- tests/api/test_rules_evaluation.py
task_type: task.code
inherits_from: []
inherit_acceptance_context: false
atoms: []
---

# El tercer valor del lenguaje de predicados (incomplete) se demuestra alcanzable con un test sobre datos reales o se retira

## Rationale

_Explain why this task exists or the business driver behind it._

El lenguaje de predicados tiene tres valores (true, false, incomplete), pero incomplete parece inalcanzable con datos reales: ningún camino de evaluación sobre un store real lo produce. Origen: un análisis de sldb que el supervisor del desk verificó en parte (2026-11-16). Código: src/sldb/api/where.py, src/sldb/store/graph/language/predicate_explain.py, predicate_reach.py y src/sldb/api/rules/.

## Goal

_Describe the concrete result this task must produce._

O hay un test que, con un store real armado en tmp_path, obtiene incomplete de una evaluación pública (where o rules check) y documenta cuándo ocurre; o incomplete se retira del lenguaje, de la API y de la doc sin cambiar los resultados true/false existentes.

## Scope

_State what is in scope and what is out of scope._

Entra: buscar todos los productores y consumidores de incomplete; intentar construir el caso real; decidir con evidencia en result-summary.md; implementar la opción elegida con tests en tests/test_predicates_cli.py o tests/api/test_rules_evaluation.py; actualizar docs/architecture/rules-language.md. CHANGELOG. No entra: otros cambios del lenguaje.

Precisiones (coordinador, bundle-1): dato real = un store armado con la API pública en tmp_path; vale un store enlazado que después se borra o se renombra para que quede no disponible. Primero se intenta demostrar; solo si en result-summary.md queda la evidencia de que ningún camino público lo produce (grep de cada sitio que emite incomplete y por qué no se alcanza), se retira. El retiro abarca GraphBackend.eval, StructuredQuery, el tipo de holds, los tests de especificación que lo nombran y docs/architecture/rules-language.md; si el hash del contrato GO02 de esa doc cambia, se actualiza con el mecanismo que check.sh --fast señala. Línea base: los tests existentes pasan sin cambiar sus valores esperados true/false. tests/api/test_rules_evaluation.py existe y se amplía.

Precisiones (coordinador, bundle-2): si se retira incomplete, toda evaluación que hoy lo devolvería devuelve false, que es lo que ya da hoy cuando compose_edge_index descarta las aristas hacia nodos que no existen (H4). El test de alcance o de retiro va en tests/api/test_rules_evaluation.py, que se agrega a files; tests/test_predicates_cli.py solo se ajusta si nombra incomplete. El índice se compone después de dejar no disponible el store enlazado.

## Implementation Path

_Outline the expected implementation route or affected surface._

1) grep de incomplete en src/sldb. 2) Intentar el caso real. 3) Decidir y documentar la decisión. 4) Implementar y testear. 5) Validation.

## Validation

_List the checks required before this task can close._

- TMPDIR=/dev/shm uv run --frozen --extra code --extra dev pytest -q tests/test_predicates_cli.py
- TMPDIR=/dev/shm uv run --frozen --extra code --extra dev pytest -q tests/api/test_rules_evaluation.py
- TMPDIR=/dev/shm uv run --frozen --extra code --extra dev pytest -q tests/test_clean_code_rules.py
- TMPDIR=/dev/shm uv run --frozen --extra code --extra dev bash tools/check.sh --fast

## Done When

_Name the observable condition that makes the task complete._

Los comandos de Validation pasan; result-summary.md explica la decisión con evidencia; CHANGELOG y commit.

## Entrega del ejecutor

Al terminar, commitea solo los archivos que cambiaste para la tarea, nombrados uno por uno (los mismos que listas en result-summary.md):

    git add <ruta> <ruta> ...
    git commit -m "<resumen>" -m "Task-Id: task-el-tercer-valor-del-lenguaje-de-predicados-incomplete-se-demuestra-alcanzable-con-un-test-sobre-dato"

Nunca uses `git add -A`, `git add -u` sobre todo el arbol ni `git stash`: puede haber trabajo ajeno sin commitear. No hagas push. Recien despues ejecuta `deskops advance task`.

## Gates rapidos del desk

Antes del commit corre, con el python del venv (/tmp/ws-venv en PATH):

    bash tools/check.sh --fast

Debe terminar con rc 0 antes de commitear; si falla, corrige y repite. Anota el comando y su rc en validation.log.

## Tu worktree

Tu codigo vive en un worktree propio, en la rama `deskops/deskops-e-5cfcba8143e9`:

    /mnt/ssd/proyectos/SLDB_1/sldb/.worktrees/deskops-e-5cfcba8143e9

Haz `cd` ahi: edita, corre los tests y commitea ahi (git add / git commit), no en el checkout principal /mnt/ssd/proyectos/SLDB_1/sldb. Las operaciones de desk (`deskops ... --root /mnt/ssd/proyectos/SLDB_1/sldb`, evidencia en runs/subagents/..., `deskops advance task`) siguen usando el checkout principal. Al terminar, reap trae tus commits a la rama principal y borra el worktree.
