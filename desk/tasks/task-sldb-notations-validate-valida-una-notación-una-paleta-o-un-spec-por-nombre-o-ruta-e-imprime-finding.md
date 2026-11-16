---
sldb:
  by: agent
  at: '2026-11-16T08:13:38Z'
  authority: generated
  via: save_document_payload
id: task-sldb-notations-validate-valida-una-notación-una-paleta-o-un-spec-por-nombre-o-ruta-e-imprime-finding
status: draft
summary: ''
tags:
- workspace:desk
- artifact:task
- host:robocop2
current_node: ritual-execution
history: []
references:
- desk/inbox/20261115-192054-suggestion-sldb-notations-validar-una-notaci-n-una-paleta-o-un-spec-por-nombre-o-ruta-desde-la-cli.md
depends_on: []
pills:
- desk/contexts/pill-pill-salida-y-orden-de-sldb-notations-validate.md
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

Entra: subcomando validate en src/sldb/cli/parsers/notations.py (nuevo _add_validate registrado en add_notations_group) y su comando en src/sldb/cli/commands/notations.py. Resolución del objetivo: una ruta existente se carga por extensión y contenido; un nombre se busca entre las notaciones y paletas builtin y del store. Validadores que se reusan sin reimplementar: load_notation (src/sldb/notations/notation_files.py), load_palette y check_palette (src/sldb/notations/palette_files.py, src/sldb/notations/palette_checks.py, contraste en src/sldb/notations/wcag_contrast.py), load_spec y validate_spec (src/sldb/api/notations/spec_models.py). Salida en texto por defecto y en JSON con --json, el mismo flag que usa sync (no se agrega --format). Para un archivo .json se aplican las mismas claves que para YAML (palette o colors: paleta; type: spec; si no, notación). Por nombre, una paleta builtin se busca con load_palette(nombre) y una notación con builtin_notations(). Las alertas, incluida la de nombre repetido en dos tipos, no cambian el exit code. Tests en tests/notations/test_notations_sync_spec_cli.py: una notación builtin válida (exit 0), una paleta con contraste insuficiente (finding, exit 1), un spec inválido (exit 1), un nombre desconocido (exit 2 y mensaje "unknown notation, palette or spec: <nombre>"). CHANGELOG.md. No entra: portar las pruebas de spec2viz (tarea aparte), validar catálogos vistas.yml, ni cambiar las reglas de validación existentes.

Precisiones (preflight-1): detección por ruta: si el argumento es un archivo existente, .json o .yml/.yaml; un YAML con clave "palette" o "colors" en la raíz es paleta, con clave "type" de diagrama (la que lee load_spec) es spec, y el resto se intenta como notación con load_notation; si el contenido no cuadra con ningún loader, exit 1 con el error del último loader. Por nombre: primero el store (si --store se pasa), después las builtin; notación antes que paleta; si el nombre existe en dos tipos, se valida el primero y se avisa con una alerta. Una ruta que no existe y no es un nombre conocido da exit 2 con el mismo mensaje. Findings: la clase Finding de sldb.core.finding (las funciones error() y alert() que usa src/sldb/cli/commands/edges.py), impresas con el alert_sink de la CLI como hace stores check. La notación builtin del test es la primera que devuelve builtin_notations() (de sldb.notations), leída en el test, no fija.

Convenciones (valen para todo el contrato): la entrada de CHANGELOG.md es una línea en español bajo el encabezado "## 0.1.13 — not released yet", con el estilo de las entradas vecinas. El commit lo hace el coordinador con deskops closeout commit (mensaje "<título corto de la tarea>"); el ejecutor no hace push. El informe del ejecutor es runs/subagents/<run-dir>/result-summary.md y ahí va todo lo que el contrato manda "anotar en el informe". Los números de línea citados son orientativos a HEAD 7288d93e: se localiza por nombre de función. Un aviso con deskops message send --to <repo> lleva como título el de la tarea y como cuerpo qué cambió y el commit; si el comando responde que el repo no está registrado, el aviso va como línea "Aviso a <repo>: ..." en el informe. "Un store de prueba" se arma con las fixtures o helpers que ya usa el archivo de test nombrado (leerlo primero); si no hay, con sldb.api (stores init, add_model, create_document) en tmp_path.

## Implementation Path

_Outline the expected implementation route or affected surface._

1) Leer src/sldb/cli/parsers/notations.py y src/sldb/cli/commands/notations.py para copiar el patrón de un subcomando con --store y --format. 2) Escribir la detección de tipo. 3) Convertir las excepciones y los resultados de check_palette/validate_spec en findings (buscar el tipo Finding que usan otros comandos, p. ej. stores check). 4) Tests con tmp_path. 5) CHANGELOG.

## Validation

_List the checks required before this task can close._

- TMPDIR=/dev/shm pytest -q tests/notations/test_notations_sync_spec_cli.py

## Done When

_Name the observable condition that makes the task complete._

`sldb notations validate default` (o el nombre de una notación builtin) sale con 0 (el nombre exacto se toma de `sldb notations list`); los cuatro casos de test pasan; `sldb notations --help` lista validate; CHANGELOG commiteado.
