FILE:desk/tasks/task-sldb-notations-validate-valida-una-notación-una-paleta-o-un-spec-por-nombre-o-ruta-e-imprime-finding.md
---
sldb:
  by: agent
  at: '2026-11-16T04:28:45Z'
  authority: generated
  via: save_document_payload
id: task-sldb-notations-validate-valida-una-notación-una-paleta-o-un-spec-por-nombre-o-ruta-e-imprime-finding
status: draft
summary: ''
tags:
- workspace:desk
- artifact:task
current_node: ritual-execution
history: []
references:
- desk/inbox/20261115-192054-suggestion-sldb-notations-validar-una-notaci-n-una-paleta-o-un-spec-por-nombre-o-ruta-desde-la-cli.md
depends_on: []
pills: []
files:
- src/sldb/cli/parsers/notations.py
- src/sldb/cli/commands/notations.py
- tests/notations/test_notations_sync_spec_cli.py
- CHANGELOG.md
task_type: task.code
inherits_from: []
inherit_acceptance_context: false
atoms:
- atom-las-vistas-de-notacion-y-proyeccion-se-resuelven-en-sldb-api-notations-por-cli-y-por-sldb-serve
---

# sldb notations validate valida una notación, una paleta o un spec por nombre o ruta e imprime findings

## Rationale

_Explain why this task exists or the business driver behind it._

La matriz de cobertura de spec2viz (IR 456b862, el doc matriz-de-cobertura de spec2viz en IR) deja la validación de notaciones y paletas (spec2viz notation validate / palette validate, con contraste WCAG) en "usar sldb directamente" y la de specs en "migrado a sldb". sldb ya tiene las comprobaciones pero ningún comando las expone: los subcomandos de sldb notations son list, sync, view, resolve y from-graph (src/sldb/cli/parsers/notations.py). Origen: desk/inbox/20261115-192054-suggestion-sldb-notations-validar-una-notaci-n-una-paleta-o-un-spec-por-nombre-o-ruta-desde-la-cli.md.

## Goal

_Describe the concrete result this task must produce._

`sldb notations validate <nombre|ruta>` detecta si el objetivo es una notación, una paleta o un spec, corre la validación que sldb ya tiene para ese tipo y devuelve findings en el formato de findings de sldb, con exit 0 si no hay errores y 1 si los hay.

## Scope

_State what is in scope and what is out of scope._

Entra: subcomando validate en src/sldb/cli/parsers/notations.py (nuevo _add_validate registrado en add_notations_group) y su comando en src/sldb/cli/commands/notations.py. Resolución del objetivo: una ruta existente se carga por extensión y contenido; un nombre se busca entre las notaciones y paletas builtin y del store. Validadores que se reusan sin reimplementar: load_notation (src/sldb/notations/notation_files.py), load_palette y check_palette (src/sldb/notations/palette_files.py, src/sldb/notations/palette_checks.py, contraste en src/sldb/notations/wcag_contrast.py), load_spec y validate_spec (src/sldb/api/notations/spec_models.py). Salida con --format text|json como el resto de la CLI. Tests en tests/notations/test_notations_sync_spec_cli.py: una notación builtin válida (exit 0), una paleta con contraste insuficiente (finding, exit 1), un spec inválido (exit 1), un nombre desconocido (exit 2 y mensaje "unknown notation, palette or spec: <nombre>"). CHANGELOG.md. No entra: portar las pruebas de spec2viz (tarea aparte), validar catálogos vistas.yml, ni cambiar las reglas de validación existentes.

## Implementation Path

_Outline the expected implementation route or affected surface._

1) Leer src/sldb/cli/parsers/notations.py y src/sldb/cli/commands/notations.py para copiar el patrón de un subcomando con --store y --format. 2) Escribir la detección de tipo. 3) Convertir las excepciones y los resultados de check_palette/validate_spec en findings (buscar el tipo Finding que usan otros comandos, p. ej. stores check). 4) Tests con tmp_path. 5) CHANGELOG.

## Validation

_List the checks required before this task can close._

- TMPDIR=/dev/shm pytest -q tests/notations/test_notations_sync_spec_cli.py

## Done When

_Name the observable condition that makes the task complete._

`sldb notations validate default` (o el nombre de una notación builtin) sale con 0 (el nombre exacto se toma de `sldb notations list`); los cuatro casos de test pasan; `sldb notations --help` lista validate; CHANGELOG commiteado.

FILE:instruccion
Preflight solo-TaskDoc de la tarea task-sldb-notations-validate-valida-una-notación-una-paleta-o-un-spec-por-nombre-o-ruta-e-imprime-finding: reformula el encargo tal como lo leería un ejecutor sin ningún otro contexto, lista ambigüedades con cita textual del input y da el DRY-RUN sin ejecutar nada. No ejecutes nada.

