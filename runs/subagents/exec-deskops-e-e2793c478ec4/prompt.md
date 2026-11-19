Task: task-higiene-del-cli-para-sldb-ui-fields-update-append-con-string-y-format-inbox-show-con-error-por-stder
Title: Higiene del CLI para sldb-ui: fields update/append con --string y --format, inbox --show con error por stderr e inbox --store sin .sldb que falla
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
  at: '2026-11-19T08:43:22Z'
  authority: generated
  via: save_document_payload
id: task-higiene-del-cli-para-sldb-ui-fields-update-append-con-string-y-format-inbox-show-con-error-por-stder
status: draft
summary: ''
tags:
- workspace:desk
- artifact:task
- host:robocop2
current_node: ritual-execution
history: []
references:
- desk/drawer/tasks/task-fields-update-parsea-el-valor-como-yaml-y-el-inbox-no-tiene-promote-matriz-ux-de-sldb-ui.md
- desk/inbox/20261116-094415-unclear-models-validate-falla-con-no-module-named-deskops-base-para-modelos-deskops-models.md
depends_on: []
pills: []
files:
- src/sldb/cli/commands/inbox_create.py
- src/sldb/cli/commands/inbox_parse.py
- tests/test_cli_v2.py
- CHANGELOG.md
task_type: task.code
inherits_from: []
inherit_acceptance_context: false
atoms: []
---

# Higiene del CLI para sldb-ui: fields update/append con --string y --format, inbox --show con error por stderr e inbox --store sin .sldb que falla

## Rationale

_Explain why this task exists or the business driver behind it._

La matriz UX de sldb-ui encontró huecos del CLI: fields update interpreta el valor como YAML y un texto con ': ' falla; fields update y append no aceptan --format; inbox --show de una nota inexistente escribe el error por stdout con exit 1; inbox <msg> --store <dir sin .sldb> no falla y escribe en desk/inbox/ del directorio padre. Origen: desk/drawer/tasks/task-fields-update-parsea-el-valor-como-yaml-y-el-inbox-no-tiene-promote-matriz-ux-de-sldb-ui.md y desk/inbox/20261116-094415-unclear-models-validate-falla-con-no-module-named-deskops-base-para-modelos-deskops-models.md (huecos a, b y c).

## Goal

_Describe the concrete result this task must produce._

fields update y append aceptan --string (el valor se toma literal, sin YAML) y --format json|text|yaml como el resto de comandos; inbox --show de una nota inexistente escribe el error por stderr con exit distinto de 0; inbox con un --store que no contiene .sldb falla con un error que lo dice y no escribe nada.

## Scope

_State what is in scope and what is out of scope._

Entra: esos cuatro cambios en los parsers y comandos de fields e inbox, su ayuda, y tests en tests/test_cli_v2.py. CHANGELOG. No entra: promote del inbox (va al drawer), otros comandos.

## Implementation Path

_Outline the expected implementation route or affected surface._

1) Leer los parsers y comandos de fields e inbox (src/sldb/cli/commands/inbox_create.py, inbox_parse.py y los de fields). 2) Implementar los cuatro cambios. 3) Tests en tests/test_cli_v2.py, uno por cambio, que fallen antes. 4) Como hay flags nuevos (--string, --format), correr 'PYTHONPATH=src sldb selfdoc sync' y commitear la referencia CLI que regenere; después 'PYTHONPATH=src sldb selfdoc check' en 0 (integrate lo exige). 5) CHANGELOG. 6) quick_gates del desk (bash tools/check.sh --fast) en 0 antes del commit, con rutas nombradas y Task-Id.

## Validation

_List the checks required before this task can close._

- TMPDIR=/dev/shm uv run --frozen --extra code --extra dev pytest -q tests/test_cli_v2.py
- TMPDIR=/dev/shm uv run --frozen --extra code --extra dev pytest -q tests/test_address_surface.py
- TMPDIR=/dev/shm uv run --frozen --extra code --extra dev pytest -q tests/test_clean_code_rules.py
- TMPDIR=/dev/shm uv run --frozen --extra code --extra dev bash tools/check.sh --fast

## Done When

_Name the observable condition that makes the task complete._

Los comandos de Validation pasan con los tests nuevos; 'sldb fields update <dir>/<campo> "Uno: dos" --string' guarda el texto literal; CHANGELOG y commit; aviso a sldb-ui.

## Entrega del ejecutor

Al terminar, commitea solo los archivos que cambiaste para la tarea, nombrados uno por uno (los mismos que listas en result-summary.md):

    git add <ruta> <ruta> ...
    git commit -m "<resumen>" -m "Task-Id: task-higiene-del-cli-para-sldb-ui-fields-update-append-con-string-y-format-inbox-show-con-error-por-stder"

Nunca uses `git add -A`, `git add -u` sobre todo el arbol ni `git stash`: puede haber trabajo ajeno sin commitear. No hagas push. Recien despues ejecuta `deskops advance task`.

## Gates rapidos del desk

Antes del commit corre, con el python del venv (/tmp/ws-venv en PATH):

    bash tools/check.sh --fast

Debe terminar con rc 0 antes de commitear; si falla, corrige y repite. Anota el comando y su rc en validation.log.
