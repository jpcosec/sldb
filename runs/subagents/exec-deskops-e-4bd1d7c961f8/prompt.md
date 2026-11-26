Task: task-la-suite-de-sldb-vuelve-a-verde-cuatro-reglas-de-codigo-limpio-el-test-de-docs-create-contra-el-cwd
Title: La suite de sldb vuelve a verde: cuatro reglas de código limpio, el test de docs create contra el cwd y anchors_resolve entre las herramientas de lectura de MCP
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
  at: '2026-11-26T04:55:58Z'
  authority: generated
  via: create_document
id: task-la-suite-de-sldb-vuelve-a-verde-cuatro-reglas-de-codigo-limpio-el-test-de-docs-create-contra-el-cwd
status: draft
summary: ''
tags: []
current_node: ritual-execution
history: []
references: []
depends_on: []
pills: []
files: []
pointers: []
task_type: task.code
inherits_from: []
inherit_acceptance_context: false
atoms: []
---

# La suite de sldb vuelve a verde: cuatro reglas de código limpio, el test de docs create contra el cwd y anchors_resolve entre las herramientas de lectura de MCP

## Rationale

_Explain why this task exists or the business driver behind it._

La suite de sldb sobre d81c4fee7 (merge con origin del 26-11) da 6 failed, 3352 passed, y eso bloquea el empuje de sldb. Las seis fallas vienen de tareas cerradas el 25-11: NotationDoc declara su estándar (318a353d9), propose-changes (560e5a1e0), partition-lanes (80e7fb7ae), docs create -o contra el cwd (c5a5e2b02) y qué documentos aplican (f68074750). Además, el test de docs create deja un cli.md en el directorio de trabajo de quien corre la suite.

## Goal

_Describe the concrete result this task must produce._

python -m pytest -q -n 4 de sldb pasa sin fallos, sin cambiar el comportamiento de lo que entró.

## Scope

_State what is in scope and what is out of scope._

Dentro: los seis fallos y nada más. (1) tests/test_clean_code_rules.py en sldb/api/notations/notation_listing.py: notation_standards tiene 20 líneas de lógica y el tope es 10. (2) Lo mismo en sldb/api/documents/batch_edges.py: _simulated tiene 22. (3) sldb/notations/notation_spec.py tiene 2 clases y el tope es 1. (4) sldb/cli/commands/notations_validate.py: _standard_shown tiene 13. (5) tests/api/test_api_creation.py::test_cli_docs_create_names_the_document espera cli.md en el repo temporal del test, pero desde c5a5e2b02 docs create -o resuelve la ruta relativa contra el cwd, así que el archivo cae en el cwd de quien corre pytest. (6) tests/mcp/test_no_writes.py::test_every_read_tool_leaves_the_store_untouched: anchors_resolve está entre las herramientas de lectura de MCP y no en la lista del test. Fuera: cambiar las reglas de tests/test_clean_code_rules.py, y cambiar el comportamiento de docs create -o o de anchors_resolve.

## Implementation Path

_Outline the expected implementation route or affected surface._

(1), (2) y (4): partir cada función en funciones de 10 líneas de lógica o menos, en el mismo archivo, sin cambiar lo que devuelven. (3): mover la segunda clase de notation_spec.py a un módulo propio en sldb/notations/ y reexportarla desde notation_spec para que los imports existentes sigan funcionando. (5): el test hace monkeypatch.chdir al repo temporal antes de llamar a docs create -o, para que la ruta relativa caiga ahí; no se cambia el comando. (6): agregar anchors_resolve a las herramientas de lectura que recorre el test, con argumentos válidos (un archivo del store de prueba), y comprobar que no escribe. Commit con prefijo fix:, sin trailer Task-Id. Correr tests/test_clean_code_rules.py, tests/api/test_api_creation.py, tests/mcp/test_no_writes.py y los tests de notations y batch_edges que importen los módulos tocados; la suite completa la corre el host.

## Validation

_List the checks required before this task can close._

- python -m pytest -q tests/test_clean_code_rules.py tests/api/test_api_creation.py tests/mcp/test_no_writes.py

## Done When

_Name the observable condition that makes the task complete._

tests/test_clean_code_rules.py, tests/api/test_api_creation.py::test_cli_docs_create_names_the_document y tests/mcp/test_no_writes.py pasan, y correr la suite ya no deja un cli.md en el cwd.

## Entrega del ejecutor

Al terminar, commitea solo los archivos que cambiaste para la tarea, nombrados uno por uno (los mismos que listas en result-summary.md):

    git add <ruta> <ruta> ...
    git commit -m "<resumen>" -m "Task-Id: task-la-suite-de-sldb-vuelve-a-verde-cuatro-reglas-de-codigo-limpio-el-test-de-docs-create-contra-el-cwd"

Nunca uses `git add -A`, `git add -u` sobre todo el arbol ni `git stash`: puede haber trabajo ajeno sin commitear. No hagas push. Recien despues ejecuta `deskops advance task`.

## Temporales de pytest

Antes de cualquier pytest exporta, para que sus temporales caigan en el /tmp del contenedor (muere con el agente) y no en el /dev/shm del host:

    export PYTEST_ADDOPTS="--basetemp=/tmp/pytest-deskops-e-4bd1d7c961f8"

## Gates rapidos del desk

Antes del commit corre, con el python del venv (/tmp/ws-venv en PATH):

    bash tools/check.sh --fast

Debe terminar con rc 0 antes de commitear; si falla, corrige y repite. Anota el comando y su rc en validation.log.

## Tu worktree

Tu codigo vive en un worktree propio, en la rama `deskops/deskops-e-4bd1d7c961f8`:

    /mnt/ssd/proyectos/SLDB_1/sldb/.worktrees/deskops-e-4bd1d7c961f8

Haz `cd` ahi: edita, corre los tests y commitea ahi (git add / git commit), no en el checkout principal /mnt/ssd/proyectos/SLDB_1/sldb. Las operaciones de desk (`deskops ... --root /mnt/ssd/proyectos/SLDB_1/sldb`, evidencia en runs/subagents/..., `deskops advance task`) siguen usando el checkout principal. Al terminar, reap trae tus commits a la rama principal y borra el worktree.
