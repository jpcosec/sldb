Task: task-la-doc-del-árbol-del-cli-cubre-todos-los-subcomandos-y-grupos-y-selfdoc-check-detecta-cuando-falta-a
Title: La doc del árbol del CLI cubre todos los subcomandos y grupos, y selfdoc check detecta cuando falta alguno
Status: active
Current node: ritual-testing
Task type: task.code
Lifecycle gates:
- task_hands_to_closeout -> ritual-closeout: open [nonempty(validation)]
  post-hook evento-para-el-coordinador: sh -c mkdir -p runs/hooks && printf '%s %s %s %s->%s\n' "$(date -u +%FT%TZ)" "$DESKOPS_TASK_ID" "$DESKOPS_TRANSITION" "$DESKOPS_FROM_NODE" "$DESKOPS_TO_NODE" >> runs/hooks/events.log
  post-hook encola-reap-del-tester: deskops queue add dispatch-reap --root .

---
sldb:
  by: agent
  at: '2026-11-21T10:13:59Z'
  authority: generated
  via: save_document_payload
id: task-la-doc-del-árbol-del-cli-cubre-todos-los-subcomandos-y-grupos-y-selfdoc-check-detecta-cuando-falta-a
status: active
summary: ''
tags:
- workspace:desk
- artifact:task
- host:robocop2
current_node: ritual-testing
history:
- task_activates
references:
- docs/architecture/current-cli-tree.md
depends_on: []
pills: []
files:
- docs/architecture/current-cli-tree.md
- src/sldb/cli/commands/selfdoc.py
- CHANGELOG.md
task_type: task.code
inherits_from: []
inherit_acceptance_context: false
atoms: []
---

# La doc del árbol del CLI cubre todos los subcomandos y grupos, y selfdoc check detecta cuando falta alguno

## Rationale

_Explain why this task exists or the business driver behind it._

docs/architecture/current-cli-tree.md omite unos 45 subcomandos y 11 grupos del CLI real, y sldb selfdoc check no lo detecta. Origen: un análisis de sldb que el supervisor del desk verificó en parte (2026-11-16).

## Goal

_Describe the concrete result this task must produce._

current-cli-tree.md lista todos los grupos y subcomandos que define el parser de sldb, y selfdoc check falla nombrando cada grupo o subcomando del parser que la doc no menciona (y cada uno que la doc nombra y ya no existe).

## Scope

_State what is in scope and what is out of scope._

Entra: (1) un chequeo en selfdoc que recorre el árbol de argparse de sldb y lo compara con los comandos nombrados en current-cli-tree.md, con hallazgos accionables; (2) completar current-cli-tree.md (si es generable desde el parser, generarlo y que el chequeo compare con lo generado); (3) tests en tests/selfdoc/. CHANGELOG. No entra: reescribir las descripciones de cada comando más allá de una línea.

Precisiones (coordinador, bundle-1): la doc sigue escrita a mano, no se genera. El chequeo extrae de current-cli-tree.md los comandos que aparecen como `sldb <grupo> [<subcomando>]` en spans de código y los compara con el árbol argparse; los alias registrados en el parser cuentan como válidos y no hace falta listarlos. Cada hallazgo usa el formato de hallazgos que selfdoc check ya emite y hace que el comando salga con rc distinto de 0. Los tests van en tests/selfdoc/test_parser.py (existe): uno que borra la línea de un subcomando en una copia de la doc y otro que agrega un comando inexistente; los dos fallan nombrando el comando.

Precisiones (coordinador, bundle-2; reemplazan lo dicho en bundle-1 sobre spans): la doc sigue escrita a mano y no se genera; esto prevalece sobre 'si es generable'. El chequeo lee el bloque de árbol ```text de current-cli-tree.md (líneas con ├──, └── o │) y arma el conjunto de rutas grupo/subcomando por indentación; lo compara con el árbol argparse sin contar alias ni 'help'. Cada diferencia es un hallazgo de severidad error con el formato que selfdoc check ya usa, y hace que report.ok sea falso. El conjunto exacto lo da el parser, no las cifras aproximadas del Rationale.

## Implementation Path

_Outline the expected implementation route or affected surface._

1) Leer src/sldb/cli/commands/selfdoc.py, current-cli-tree.md y cómo se arma el parser (src/sldb/cli/parsers/). 2) Implementar el chequeo y completar la doc. 3) Tests. 4) Validation.

## Validation

_List the checks required before this task can close._

- TMPDIR=/dev/shm uv run --frozen --extra code --extra dev pytest -q tests/selfdoc/test_parser.py
- TMPDIR=/dev/shm uv run --frozen --extra code --extra dev python -m sldb selfdoc check
- TMPDIR=/dev/shm uv run --frozen --extra code --extra dev pytest -q tests/test_clean_code_rules.py
- TMPDIR=/dev/shm uv run --frozen --extra code --extra dev bash tools/check.sh --fast

## Done When

_Name the observable condition that makes the task complete._

Los comandos de Validation pasan; borrar una línea de current-cli-tree.md hace fallar selfdoc check nombrando el comando; CHANGELOG y commit.

## Como probar (tester)

Ubica el trabajo del ejecutor:

    git log -1 --format=%H --grep "Task-Id: task-la-doc-del-árbol-del-cli-cubre-todos-los-subcomandos-y-grupos-y-selfdoc-check-detecta-cuando-falta-a"   # commit del ejecutor
    git show --name-only <commit>                           # sus archivos

Los tests a correr son los archivos tests/*.py de ese commit, mas tests/test_<modulo>.py cuando exista para cada modulo de codigo tocado; de a uno, con `TMPDIR=/tmp python -m pytest -q <archivo>`. No corras la suite completa: la corre integrate en el host.

Escribe result-summary.md con el veredicto PASA o FALLA en la primera linea.

## Gates rapidos del desk

Antes del veredicto corre, con el python del venv (/tmp/ws-venv en PATH):

    bash tools/check.sh --fast

Si termina con rc distinto de 0 el veredicto es FALLA.
