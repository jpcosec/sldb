FILE:desk/tasks/task-decisión-de-jp-si-sldb-agrega-un-ast-intermedio-entre-marcador-y-campo-y-clases-anidadas-en-un-docum.md
---
sldb:
  by: agent
  at: '2026-11-16T06:21:24Z'
  authority: generated
  via: save_document_payload
id: task-decisión-de-jp-si-sldb-agrega-un-ast-intermedio-entre-marcador-y-campo-y-clases-anidadas-en-un-docum
status: draft
summary: ''
tags:
- workspace:desk
- artifact:task
- host:robocop2
current_node: ritual-execution
history: []
references:
- desk/drawer/features/feature-nested-primitive-classes-via-composition.md
depends_on: []
pills: []
files:
- docs/architecture/model-authoring.md
task_type: task.decision
inherits_from: []
inherit_acceptance_context: false
atoms: []
from_drawer: desk/drawer/features/feature-decoupled-ast-and-field-instances.md
---

# Decisión de JP: si sldb agrega un AST intermedio entre marcador y campo y clases anidadas en un documento (dos features del drawer)

## Rationale

_Explain why this task exists or the business driver behind it._

Dos features del drawer piden cambiar el núcleo de extracción. (1) AST desacoplado: un marcador nombraría una forma de AST (por ejemplo un ítem de lista de tareas con estado marcado) que luego se mapea al campo, en lugar del mapeo 1:1 de hoy entre marcador y handler (src/sldb/core/handlers/router.py; src/sldb/core/handlers/list.py solo da strings). (2) Clases anidadas por composición: campos list[SubModelo] extraídos recursivamente de una lista o sección; hoy las tablas dan filas como dicts (src/sldb/core/handlers/table.py:8) y __compositions__ (src/sldb/models/structured_doc.py:13) compone otros documentos, no objetos en línea. Las dos tocan el mismo código y la propia feature 2 pregunta si van juntas. Es una decisión de dirección del núcleo, por eso es del dueño. Origen: desk/drawer/features/feature-decoupled-ast-and-field-instances.md y desk/drawer/features/feature-nested-primitive-classes-via-composition.md.

## Goal

_Describe the concrete result this task must produce._

JP decide una de: (a) no se hacen (se retiran las dos features); (b) se hace solo (2), clases anidadas sobre listas y tablas, sin AST intermedio; (c) se hacen las dos juntas. La decisión queda en docs/architecture/model-authoring.md, sección "AST intermedio y clases anidadas", con fecha, y si no es (a) se crea la tarea de diseño correspondiente.

## Scope

_State what is in scope and what is out of scope._

Entra: presentar a JP las opciones con costo y quién lo pide hoy: ningún consumidor activo lo pide en el inbox; la tarea task-diseño-set-bootstrap-de-modelos-tras-la-convergencia-átomo-field toca la misma frontera átomo/field. Recomendación del coordinador: (a) por ahora, y reabrir si la tarea del set bootstrap lo necesita. Registrar el recibo owner (dispose accepted de JP), escribir la sección, y crear con deskops add task la tarea de diseño si corresponde. No entra: implementar ni prototipar.

Protocolo de decisión (vale para todo el contrato): el coordinador del desk de sldb le pregunta a JP por el canal de coordinación (herdr o el supervisor), con las opciones, costos y recomendación de este contrato copiados tal cual. La respuesta se registra con `deskops review record <esta tarea> --kind owner --reason "JP <AAAA-MM-DD>: <opción y motivo>" --root sldb`; el dispose accepted lo hace JP con `deskops review dispose <id del recibo> --verdict accepted --reason ... --root sldb`; nada se ejecuta ni se cierra sin ese recibo aceptado. "La fecha" es la de la respuesta de JP, en ISO (AAAA-MM-DD). La sección del documento tiene esta forma: un encabezado "## <nombre de la sección>", una línea "Decisión (AAAA-MM-DD, JP): <opción>", una línea "Motivo: <motivo>" y la lista de las opciones consideradas con su costo. Una tarea que la decisión crea se escribe con deskops add task --root sldb con el contrato completo (title, why, goal, scope, implementation_path, files, validation, done_when) y references a la nota o ítem de origen de esta tarea. El commit del documento lo hace el coordinador con deskops closeout commit; nadie hace push salvo el integrador.
Precisiones (preflight-1): si JP elige (a), el coordinador retira las dos features del drawer con deskops drawer remove en el mismo cierre; si elige (b) o (c), las features se retiran cuando exista la tarea de diseño creada (que las cita en references).

Referencia kimun (solo lectura, github jpcosec/kimun main b14a30f; JP: "lo que no está marcado no necesita quedar registrado"). Principio en kimun: doc v2 de kimun 00-nucleo.md:55 (5.3) "no todo lo expresado se vuelve conocimiento registrado" y doc v2 de kimun 14-juego-del-lenguaje.md:424,434 "Lo que no selecciona no entra al store ... No hace falta marcar documentos ni subclases para ignorar un párrafo". Objetos anidados: kimun no los incrusta; son documentos aparte referenciados por compositions, "Los documentos referenciados se resuelven por índice, no por embebido" (doc v2 de kimun 07-modelos-como-nodos.md:78), y sus tipos de campo no tienen submodelo incrustado (07:80). El AST con selectores es su diseño objetivo (14:196-206, decisión 28) pero el lenguaje de selectores sigue pendiente (14:208). Recomendación para que JP confirme: (a), no se hacen. Lo anidado se modela como documentos aparte con __compositions__, que sldb ya tiene, y lo que ningún marcador reclama se queda en el archivo sin registrarse. El AST intermedio se reabre solo si la tarea del set bootstrap lo necesita.

## Implementation Path

_Outline the expected implementation route or affected surface._

1) Leer las dos features y docs/architecture/model-authoring.md. 2) Pedir decisión a JP. 3) Escribir la sección. 4) Crear la tarea de diseño o dejar las features para retiro (deskops drawer remove) según la respuesta.

## Validation

_List the checks required before this task can close._

- grep -n 'AST intermedio y clases anidadas' docs/architecture/model-authoring.md

## Done When

_Name the observable condition that makes the task complete._

La sección existe con la opción y la fecha; recibo owner aceptado por JP; tarea de diseño creada si no es (a); commit del doc.

FILE:desk/rituals/execution.md
---
# ritual-xxx
id: ritual-execution
# Ordered prose steps; not document references
steps:
- 'Atomize: break the work into the smallest possible child tasks.'
- 'Dedupe: merge overlapping items.'
- 'Clean: delete legacy content that the work makes obsolete (with deskops retire,
  closeout or drawer remove, never by hand).'
- 'Audit existing work before claiming anything is done: check git history for relevant
  commits, verify artifacts exist where specified, and run tests to confirm the current
  state.'
- Resolve contradictory end states between the desk and the repo.
- Bind the pills the task depends on (the task's pills field or deskops bind).
- Keep the Board current; deskops maintains it, so use deskops verbs instead of editing
  it.
- 'Execute with explicit boundaries: scope, touched files and validation targets stated
  in the task.'
- 'After each step, run the context audit: is every aspect of the task covered by
  a pill, are the bound pills still accurate, update or retire the stale ones, and
  bind new ones as needed.'
# e.g., layer:workflow, system:sldb
tags:
- workspace:desk
---

# Execution ritual

## Purpose

_Explain why this ritual exists._

Review the board, bind the relevant pills, keep scope tight, and implement only the active task for sldb.

## Trigger

_State when this ritual should start._

Before starting any task, and after each step while implementing it.

## Preconditions

_List the conditions that must hold before running the ritual._

- Pre-execution gate: ask whether any aspect of the task is ambiguous or not covered by its task file, pills and atoms. If not, proceed. If so, create or request the missing context first; do not proceed until the task is unambiguous.
- The Board (desk/tasks/Board.md) is the single entry point for active work: read it before starting any task.

## Validation

_List the checks that prove the ritual was performed correctly._

- Scope, touched files and validation targets are explicit in the task.
- Every desk reference points at durable repo context: task files, pills, atoms, drawer notes, inbox messages, source files, tests, docs and commits.

## Failure Modes

_List common mistakes this ritual prevents._

- Proceeding with an ambiguous task without creating or requesting the missing context.
- Creating implementation artifacts instead of referencing existing pills.
- Referencing surfaces below the current layer.
- Desk documents pointing at chat memory or other non-durable context.
- Trusting the task file over the code: the task file describes intent; git history is truth.

## Completion

_Describe what completion looks like._

The task's change is implemented within its stated scope and the testing ritual can start.

FILE:desk/rituals/testing.md
---
# ritual-xxx
id: ritual-testing
# Ordered prose steps; not document references
steps:
- 'Invalidate: check whether existing tests are broken by the change; update or delete
  the ones that no longer describe the behavior.'
- 'Verify: add new tests where the change needs them.'
- 'Test: run the relevant test or validation suite, smallest first, then the full
  suite when shared behavior changed. All required checks must pass.'
# e.g., layer:workflow, system:sldb
tags:
- workspace:desk
---

# Testing ritual

## Purpose

_Explain why this ritual exists._

No task is complete without testing. Run the smallest relevant validation first, then broaden coverage when sldb changes shared behavior.

## Trigger

_State when this ritual should start._

When the implementation of a task is done, before closeout.

## Preconditions

_List the conditions that must hold before running the ritual._

- 

## Validation

_List the checks that prove the ritual was performed correctly._

- All required checks pass: the test suite, plus stores check, tools/check.sh and tools/check_claims.py when the change touches the store, the gates or documented claims.

## Failure Modes

_List common mistakes this ritual prevents._

- Skipping tests to get it done.
- Declaring a check green from truncated output (a pipe through tail hides the exit status).

## Completion

_Describe what completion looks like._

Every required check passes on the final change.

FILE:desk/rituals/closeout.md
---
# ritual-xxx
id: ritual-closeout
# Ordered prose steps; not document references
steps:
- Update the CHANGELOG when the change is user-visible or release-relevant.
- 'Run the context audit: check the task''s pills, update stale ones, and retire the
  ones whose knowledge now lives in code or docs.'
- 'Close the task with deskops closeout (commit, or supersede/retire when it was already
  resolved): the task leaves the Board in the same atomic commit as its evidence.
  Completed tasks are not kept on the Board.'
- 'Commit atomically, only when the execution ritual is complete. Commit when a phase
  or slice objective is fully checked (a concise scoped message), for a critical bug
  fix mid-phase (fix(<scope>): <description>), or for chores such as dependencies
  or config (chore(<scope>): <description>). A slice that is not done is not a commit:
  work in progress is not committed.'
- 'Write commit messages as <type>(<scope>): <description>, with type one of feat,
  fix, docs, refactor, chore, test, perf, and scope the smallest accurate repo area,
  component, command or workflow surface.'
# e.g., layer:workflow, system:sldb
tags:
- workspace:desk
---

# Closeout ritual

## Purpose

_Explain why this ritual exists._

Close a sldb task only after validation passes, the board is updated, and the final change is ready to commit.

## Trigger

_State when this ritual should start._

When the testing ritual passes for a task.

## Preconditions

_List the conditions that must hold before running the ritual._

- Pre-completion audit, git history: the commits match the completed work; on a mismatch, correct the commit history or update the task state to reflect reality.
- Pre-completion audit, artifacts: every specified output exists at the specified location; implement the missing ones.
- Pre-completion audit, tests: all pass; fix failing tests first.
- Pre-completion audit, clean tree: every untracked file is either gitignored or tracked; clean up a dirty tree before declaring done.
- Trust the code, not the task file: the task file describes intent, git history is truth.

## Validation

_List the checks that prove the ritual was performed correctly._

- deskops closeout verify reports the tests, commit and atom gates as passing, and the tree is clean.

## Failure Modes

_List common mistakes this ritual prevents._

- Marking a task complete without auditing git history.
- Committing with untracked files (gitignore or track them first).
- Force-pushing to hide failures.
- Committing work in progress.

## Completion

_Describe what completion looks like._

The closing commit exists, the task is off the Board, and the tree is clean.

FILE:desk/rituals/phase.md
---
# ritual-xxx
id: ritual-phase
# Ordered prose steps; not document references
steps:
- 'Compile: rebuild when applicable (bundles, dist).'
- 'Audit: run the relevant tests and quality checks.'
- 'Regress: fix any test failure.'
- 'Flow: move the pill knowledge that is still needed into code or docs, capture phase-level
  learning into an atom, and retire the redundant pills.'
- 'Advance: clear the Board for the next phase and move on.'
# e.g., layer:workflow, system:sldb
tags:
- workspace:desk
---

# Phase ritual

## Purpose

_Explain why this ritual exists._

Close the active phase only when every task on the sldb board is complete, capture any phase-level learning into an atom, and clear the board for the next phase.

## Trigger

_State when this ritual should start._

When every task in a phase or delivery slice is done.

## Preconditions

_List the conditions that must hold before running the ritual._

- 

## Validation

_List the checks that prove the ritual was performed correctly._

- Tests and quality checks pass and no pill repeats what code or docs already say.

## Failure Modes

_List common mistakes this ritual prevents._

- 

## Completion

_Describe what completion looks like._

The Board holds only the next phase's tasks.

FILE:docs/architecture/model-authoring.md
# Model Authoring and Draft Evolution

This document specifies the declarative model authoring and contract evolution in SLDB (`StructuredNLDoc`).

## 1. Declarative Model Attributes

Every `StructuredNLDoc` subclass may declare:

- `__authority__`: String representing document authority (`source_raw`, `authored`, `theorem`, `generated`, `cache`). Defaults to `"generated"`.
- `__semantics__`: Dictionary defining semantic dimensions (e.g., `{"representation": ["markdown"], "source": ["document", "markdown"]}`).
- `__containment__`: Mapping of `field_name -> list[target_model_names]`, establishing visual containment relations in the knowledge graph.
- `__references__`: List of field names holding document identifiers that represent non-containment graph references.
- `__compositions__`: Mapping of `comp_name -> spec_dict` where `spec_dict` defines `source_field`, `model`, `template`, and `separator`. Each composition must be rendered via a non-reversible `⸢render•<comp_name>⸥` marker in `__template__`.

## 2. Programmatic Creation (`sldb.api.create_model`)

`create_model` generates a `StructuredNLDoc` class module, validates it via roundtrip check, registers it in the store index, and creates its model and document indexes.

Parameters:
- `name`: Model class name (CamelCase identifier).
- `fields`: Field declarations (`[{name, type, description, required?, default?, enum?}]`).
- `template`: Optional markdown template. When omitted, `default_template` generates headings and slots for every field plus `⸢render•<name>⸥` for each composition.
- `containment`: Optional mapping `dict[str, list[str]]`.
- `references`: Optional list `list[str]`.
- `compositions`: Optional mapping `dict[str, dict]`.
- `semantics`: Optional mapping `dict[str, list[str]]`.
- `authority`: Optional authority string.

Validation rules:
- Every field named in `containment` or `references` must exist among the model's declared (or inherited) fields.
- Every `compositions[k].source_field` must exist among the declared (or inherited) fields.
- Every composition key must have its corresponding `⸢render•<comp_name>⸥` marker present in `__template__`.
Violations raise `SLDBModelError`.

## 3. Inspection (`sldb.api.describe_model` & `GET /models/detail`)

`describe_model` returns a `ModelDescription` containing:
- `name`, `model_ref`, `path`, `version`, `canonical`, `family`, `semantics`, `base_models`, `fields`, `documents`.
- `containment`: Dictionary of containment targets.
- `references`: List of reference fields.
- `compositions`: Dictionary of composition specifications.
- `semantics_map`: Declared `__semantics__` dictionary.
- `authority`: Declared `__authority__`.
- `template`: Model's active markdown template.
- `has_draft`: Boolean indicating whether a `.draft.py` (`.py.temp`) exists.
- `draft_path`: Path string to the draft file if present, otherwise `None`.

## 4. Draft Metadata Editing (`sldb.api.edit_model_metadata`)

Pending changes to model metadata are written to the draft sibling file (`<module>.py.temp`) using AST rewriting (`metadata_literals.py`), leaving the active model source completely untouched until promotion.

- `edit_model_metadata(store, model_name, *, containment=None, references=None, compositions=None, semantics=None, authority=None, pythonpath=None) -> ModelDraft`:
  - Inserts or replaces `__containment__`, `__references__`, `__compositions__`, `__semantics__`, `__authority__` via AST manipulation.
  - Synchronizes `⸢render•<name>⸥` sections in `__template__` when compositions are added or removed.

## 5. Contract Validation & Backfill Promotion

- `validate_model_draft(store, model_name, pythonpath)` verifies that:
  - Reversible template markers reference valid declared fields.
  - `__references__`, `__containment__`, and `__compositions__` only reference declared fields.
  - Every composition has a `⸢render•<name>⸥` marker in `__template__`.
  - Violations raise actionable `SLDBModelEditError`.

- `promote_model_draft(store, model_name, pythonpath, backfill=False)`:
  - Validates the draft.
  - With `backfill=True`, updates documents that need re-rendering under new defaults, template changes, or composition changes.
  - Atomically replaces the active model file with the draft.
  - Removes the draft file.
  - Reindexes the model, bumps contract version, and triggers derived rebuilds for semantic, section, and edge indexes.

## 6. CLI & HTTP Surface

CLI:
- `sldb models metadata edit <model> [--containment ...] [--references ...] [--compositions ...] [--semantics ...] [--authority ...]`: Creates or updates a metadata draft.
- `sldb models validate <model> --promote --backfill`: Validates, promotes the draft, and backfills tracked documents.
- `sldb models create <name> --template <tpl> --fields <spec> [--containment ...] [--references ...] [--compositions ...] [--semantics ...] [--authority ...]`.

HTTP Serve (`sldb serve`):
- `POST /models/create`: Generates and registers a new model.
- `GET /models/detail?model=<name>`: Returns complete model description including metadata and draft status.
- `POST /models/metadata-edit`: Updates draft metadata.
- `POST /models/promote`: Accepts `{"model": "<name>", "backfill": true}` to promote with document backfill and index rebuilds.

FILE:instruccion
Cold-bundle de la tarea task-decisión-de-jp-si-sldb-agrega-un-ast-intermedio-entre-marcador-y-campo-y-clases-anidadas-en-un-docum: con el TaskDoc, los rituales enrutados por el Board, las pills ligadas, los átomos ligados y los archivos que el TaskDoc nombra, reformula el encargo, lista ambigüedades con cita textual del input y da el DRY-RUN sin ejecutar nada. No ejecutes nada.

Sección de validación del TaskDoc:
- grep -n 'AST intermedio y clases anidadas' docs/architecture/model-authoring.md

