FILE:desk/tasks/task-sldb-version-dice-qué-commit-corre-versión-del-paquete-más-git-describe-del-checkout-editable.md
---
sldb:
  by: agent
  at: '2026-11-16T04:07:39Z'
  authority: generated
  via: create_document
id: task-sldb-version-dice-qué-commit-corre-versión-del-paquete-más-git-describe-del-checkout-editable
status: draft
summary: ''
tags:
- workspace:desk
- artifact:task
current_node: ritual-execution
history: []
references:
- desk/inbox/inbox-note-dos-instalaciones-de-sldb-y-la-versión-no-dice-qué-commit-corre.md
depends_on: []
pills: []
files:
- src/sldb/store/package_version.py
- src/sldb/cli/parser.py
- tests/test_cli_v2.py
- CHANGELOG.md
task_type: task.code
inherits_from: []
inherit_acceptance_context: false
atoms: []
---

# sldb --version dice qué commit corre (versión del paquete más git describe del checkout editable)

## Rationale

_Explain why this task exists or the business driver behind it._

En robocop hubo dos instalaciones de sldb (una editable sobre el checkout principal con cambios ajenos, otra sobre ~/herramientas/sldb) y las dos decían 0.1.13, aunque git describe daba v0.1.13-283-gb965c62d: ningún comando dice qué commit corre. La instalación ya quedó en una sola (uv tool deskops, editable sobre /home/robocop/herramientas/sldb); falta lo de sldb. src/sldb/store/package_version.py devuelve solo la versión del pyproject y la CLI (src/sldb/cli/parser.py) no tiene --version. Origen: desk/inbox/inbox-note-dos-instalaciones-de-sldb-y-la-versión-no-dice-qué-commit-corre.md.

## Goal

_Describe the concrete result this task must produce._

`sldb --version` imprime una línea "sldb <versión> (<git describe --always --dirty> at <ruta del checkout>)" cuando corre desde un checkout git, y "sldb <versión>" cuando corre desde un paquete instalado sin .git; exit 0.

## Scope

_State what is in scope and what is out of scope._

Entra: en src/sldb/store/package_version.py una función source_revision() -> str | None que, si el pyproject encontrado por _source_checkout_version está en un directorio con .git (archivo o carpeta, para worktrees), corre `git -C <dir> describe --tags --always --dirty` con subprocess (timeout 2 s) y devuelve su salida, o None si git falla o no está; en src/sldb/cli/parser.py el argumento global --version con action que imprime la línea de Goal. Tests en tests/test_cli_v2.py: --version sale con 0 y empieza con "sldb "; con source_revision parcheada a None no hay paréntesis; con un valor fijo aparece entre paréntesis. CHANGELOG.md. No entra: cambiar producer.version de los sellos de procedencia, decidir qué instalación es la de referencia (ya resuelto: una sola instalación), limpiar los review dirs huérfanos del desk.

## Implementation Path

_Outline the expected implementation route or affected surface._

1) Leer src/sldb/store/package_version.py y src/sldb/cli/parser.py (construcción del parser raíz). 2) Agregar source_revision. 3) Agregar --version con una argparse.Action propia que imprime y sale. 4) Tests. 5) Probar a mano `sldb --version` desde el checkout.

## Validation

_List the checks required before this task can close._

- TMPDIR=/dev/shm pytest -q tests/test_cli_v2.py
- TMPDIR=/dev/shm pytest -q tests/test_cli_envelope.py
- PYTHONPATH=src python -m sldb --version

## Done When

_Name the observable condition that makes the task complete._

Los tests pasan; `PYTHONPATH=src python -m sldb --version` desde el checkout imprime la versión con el describe entre paréntesis; CHANGELOG y commit.

FILE:instruccion
Preflight solo-TaskDoc de la tarea task-sldb-version-dice-qué-commit-corre-versión-del-paquete-más-git-describe-del-checkout-editable: reformula el encargo tal como lo leería un ejecutor sin ningún otro contexto, lista ambigüedades con cita textual del input y da el DRY-RUN sin ejecutar nada. No ejecutes nada.

