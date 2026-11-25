FILE:desk/tasks/task-decisión-de-jp-python-sync-o-stores-build-destrackean-los-pythonsymboldoc-cuyo-símbolo-desapareció.md
---
sldb:
  by: agent
  at: '2026-11-16T06:22:34Z'
  authority: generated
  via: save_document_payload
id: task-decisión-de-jp-python-sync-o-stores-build-destrackean-los-pythonsymboldoc-cuyo-símbolo-desapareció
status: draft
summary: ''
tags:
- workspace:desk
- artifact:task
- host:robocop2
current_node: ritual-execution
history: []
references: []
depends_on: []
pills: []
files:
- docs/self-documentation.md
task_type: task.decision
inherits_from: []
inherit_acceptance_context: false
atoms: []
from_drawer: desk/drawer/tasks/task-python-sync-no-destrackea-un-pythonsymboldoc-cuyo-s-mbolo-desapareci.md
---

# Decisión de JP: python-sync o stores build destrackean los PythonSymbolDoc cuyo símbolo desapareció

## Rationale

_Explain why this task exists or the business driver behind it._

selfdoc python-sync escribe PythonSymbolDoc pero nunca destrackea (write_python_plans, src/sldb/cli/commands/selfdoc_python.py:69; no hay untrack en src/sldb/selfdoc). El contrato actual los conserva a propósito: src/sldb/selfdoc/report.py:32 "Removed documents are retained" y el test tests/selfdoc/test_sync.py::test_removed_commands_are_reported_and_retained. Resultado: cuando c420809c borró el journal quedaron 108 PythonSymbolDoc huérfanos (stores build en sitio: undeclared 108), limpiados a mano con sldb docs untrack (dfa5c504; otro en 641ecdfa). Destrackear cambia la semántica (borra documentos trackeados derivados), por eso es del dueño. Origen: drawer desk/drawer/tasks/task-python-sync-no-destrackea-un-pythonsymboldoc-cuyo-s-mbolo-desapareci.md.

## Goal

_Describe the concrete result this task must produce._

JP decide (a) python-sync destrackea los PythonSymbolDoc de su system cuyo símbolo ya no existe y conserva los documentos de comandos y superficies escritos por personas; (b) también destrackea los de comandos y superficies; o (c) se mantiene la retención y solo se reportan. La decisión queda en docs/self-documentation.md, sección "Símbolos que desaparecen", y si es (a) o (b) se crea la tarea de código que cambia report.py y test_sync.py.

## Scope

_State what is in scope and what is out of scope._

Entra: presentar las tres opciones; recomendación del coordinador: (a), porque los PythonSymbolDoc son generados (knowledge/symbols/ está en derived) y los de comandos y superficies los escriben personas. Registrar el recibo owner (dispose accepted de JP), escribir la sección, crear la tarea de código si corresponde. No entra: implementar; la alerta de stores check sobre documentos derivados ausentes es otra tarea.

Protocolo de decisión (vale para todo el contrato): el coordinador del desk de sldb le pregunta a JP por el canal de coordinación (herdr o el supervisor), con las opciones, costos y recomendación de este contrato copiados tal cual. La respuesta se registra con `deskops review record <esta tarea> --kind owner --reason "JP <AAAA-MM-DD>: <opción y motivo>" --root sldb`; el dispose accepted lo hace JP con `deskops review dispose <id del recibo> --verdict accepted --reason ... --root sldb`; nada se ejecuta ni se cierra sin ese recibo aceptado. "La fecha" es la de la respuesta de JP, en ISO (AAAA-MM-DD). La sección del documento tiene esta forma: un encabezado "## <nombre de la sección>", una línea "Decisión (AAAA-MM-DD, JP): <opción>", una línea "Motivo: <motivo>" y la lista de las opciones consideradas con su costo. Una tarea que la decisión crea se escribe con deskops add task --root sldb con el contrato completo (title, why, goal, scope, implementation_path, files, validation, done_when) y references a la nota o ítem de origen de esta tarea. El commit del documento lo hace el coordinador con deskops closeout commit; nadie hace push salvo el integrador.
Precisiones (preflight-1): generado = PythonSymbolDoc (el modelo que escribe python-sync bajo knowledge/symbols/, ruta declarada derived); escritos por personas = los documentos de comandos y superficies que selfdoc reporta como removed pero que no están bajo una ruta derived. El recibo se verifica con `deskops review status <esta tarea> --root sldb`.

Referencia kimun (solo lectura, github jpcosec/kimun main b14a30f): "Regla de untrack. Un símbolo que desaparece del código no borra su documento: sync hace docs untrack y el archivo queda en disco" (doc v2 de kimun 11-adaptadores.md:217-218). Es un cambio explícito sobre v1, que "solo informaba removed": check informa orphan con exit 1 (11:449-450). Si el símbolo vuelve, "su archivo retenido se adopta y sus campos autorados sobreviven" (11:222-230). El alcance es solo lo que el adaptador posee: etiqueta del adaptador, system y directorio de salida (11:189-198). Principio: "Si es borrado, no se mantiene el nodo ... si se borra un ID estructural que soporta un claim de conocimiento, se declara" (14-juego-del-lenguaje.md:513-515). Recomendación para que JP confirme: (a). python-sync destrackea los PythonSymbolDoc de su system cuyo símbolo desapareció y deja el archivo en disco; selfdoc check los informa como orphan; si el símbolo vuelve, el documento se re-adopta. Los documentos de comandos y superficies escritos por personas no se tocan.

## Implementation Path

_Outline the expected implementation route or affected surface._

1) Leer report.py, selfdoc_python.py, tests/selfdoc/test_sync.py y docs/self-documentation.md. 2) Pedir decisión. 3) Escribir la sección. 4) Crear la tarea de código con validación TMPDIR=/dev/shm pytest -q tests/selfdoc/test_sync.py.

## Validation

_List the checks required before this task can close._

- grep -n 'Símbolos que desaparecen' docs/self-documentation.md

## Done When

_Name the observable condition that makes the task complete._

La sección existe con la opción y la fecha; recibo owner aceptado por JP; tarea de código creada si es (a) o (b); commit del doc.

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

FILE:docs/self-documentation.md
# CLI Self-Documentation

The first self-documentation slice derives CLI reference records from an assembled argparse parser and tracks them with SLDB's existing `CliCommandDoc` and `SurfaceDoc` models.

`sldb selfdoc python-scan --source-root src` is the read-only Python inventory. `python-sync` materializes it under `knowledge/symbols/` and persists the regenerable source facts through sldb's graph layer; `python-check` reports documentation or source-graph drift without writing. They use the standard-library AST and never import scanned modules. Each record has a qualified `python:<module>:<qualname>` identity (not stable across moves or renames), source span, syntactic signature, declared docstring, module imports, and a file hash. Regeneration owns those facts and preserves authored `purpose`, `architecture`, and tags. Roles, architecture boundaries, rename equivalence, and spec2viz grouping still require declared or reviewed metadata.

The [docstring indexing contract](architecture/code-docstring-indexing.spec.md) specifies source-owned metadata and explanations, AST-derived relationships, selective tag inheritance, and graph-backed projections. `python-sync` projects module/symbol containment, import bindings (through explicit re-export chains), and annotation references, with source span and hash evidence, validates docstring metadata strictly, and gives every graph node its local and inherited tags with their origin. These are store facts for any consumer; the adapter does not prescribe a consumer query language or read the artifact back through another runtime. The generated Markdown records keep their qualified-name document IDs and do not carry the inherited tags (spec section 7).

All tracked records are rendered as Markdown, but the semantic index distinguishes their source format. Ordinary models inherit `representation.markdown` and `source.document.markdown`; `PythonSymbolDoc` has `representation.markdown` and `source.code.python`. Consumers must use those tags rather than infer source format from a path or model name.

For this repository, bind records to the current structural evidence:

```bash
sldb selfdoc python-sync --source-root src --system sldb \
  --architecture-spec docs/architecture/spec2viz/python-ast.yml
sldb selfdoc python-check --source-root src --system sldb \
  --architecture-spec docs/architecture/spec2viz/python-ast.yml
```

`python-sync` writes the source graph itself with sldb's graph IO (`sldb.selfdoc.source_graph_file.write_source_graph`); no external tool is invoked. The default location is `.sldb_cache/graphs/python-source.graph.json`; override it with `--graph-output path`. Paths are rooted at the store's project and cannot escape it. The graph is generated local state. A missing or source-stale graph appears as `graph_stale` and makes `python-check` return 1, just like source-document drift.

For example, the graph distinguishes `command` **containing** `CommandRecord`, the module **importing** `ArgumentRecord`, and the field annotation **referencing** it. The projection proves containment, imports (following explicit re-export chains), and annotation references resolved against the binding active at that point — not runtime calls or star-imported names. Consumers query the published store facts through their own supported sldb integration; an agent does not treat the generated graph file as an ad-hoc source of truth. The consumer boundary is specified in [the docstring indexing contract, section 4.3](architecture/code-docstring-indexing.spec.md).

The `architecture_spec` field stores that relative path and its SHA-256. It identifies the referenced artifact; it does not prove review, source freshness, symbol-to-node membership, or semantic roles. Module names come from the path under `--source-root`: `src/sldb/cli/main.py` is `sldb.cli.main`. `--package` prefixes them, so it is for a source root that is the package itself (`--source-root src/sldb --package sldb`); with `--source-root src` it doubled the prefix into `sldb.sldb.*`, the identities this repository's inventory carried until the migration of 2026-10-18.

When a source inventory no longer contains a tracked Python symbol, `python-check` reports removed records without deleting them. A rename candidate now appears only for one unique fact match; an actual rename may change its signature, docstring, or source file hash and therefore produce no candidate. Candidates remain review hints, and SLDB never rewrites a symbol ID or authored context automatically. Complete-source removal and nondefault output paths need additional coverage.

`python-check` also reports `semantic_gaps`: the count of tracked symbols whose authored `purpose` or `architecture` is still `Not documented.`. This is a placeholder metric, not evidence of missing information in source docstrings, generated semantic classification, or an integrity failure. Both Python and CLI checks now return 1 whenever JSON reports `ok: false`.

## Workflow

From this project root or any subdirectory inside its store:

```bash
sldb selfdoc scan
sldb selfdoc sync
sldb selfdoc check
sldb fields show docs/cmd-sldb-selfdoc-sync/arguments
```

`scan` emits a JSON inventory without running command handlers. `sync` updates generated fields, registers missing models/documents, and updates tracking hashes and section indexes. `check` compares expected fields, files, and document tracking without writing them. A repeated sync of current inputs does not rewrite the documents.

The repository CI checks the generated reference on Python 3.13, the runtime used to materialize it. The normal test matrix covers Python 3.12 and 3.13, the supported versions (`requires-python >=3.12`); parser presentation can differ between Python versions.

`sync` and `check` resolve the nearest ancestor store or accept `--store PATH/ALIAS`. `--output knowledge` is relative to the selected store's project root, not the current subdirectory; destinations outside that project are rejected. The global registry is not modified by this workflow.

All project-relative interfaces use the same context rule: the nearest non-global ancestor store is selected, then its project root anchors paths. A relative `faq --faq-path`, `explore --docs-root`, and `explore --code-root` follow that root; pass an absolute path to opt out. Store aliases resolve from the closest registry outward and finally from `~/.sldb`. `stores init` explicitly catalogs stores below the user home directory in that global store; ordinary reads never perform a disk-wide discovery scan.

For existing stores, reconciliation is explicit: `sldb stores reconcile --path <subtree>` reports discovered, missing, and stale catalog paths; add `--apply` to replace that catalog with the discovered subtree. It is intentionally never performed by a read/query command.

For another trusted argparse application:

```bash
sldb selfdoc scan --factory myapp.cli:build_parser --pythonpath src
sldb selfdoc sync --factory myapp.cli:build_parser --pythonpath src --system myapp
sldb selfdoc check --factory myapp.cli:build_parser --pythonpath src --system myapp
```

The factory must return `argparse.ArgumentParser`. Importing it and building the parser executes Python, so the factory must be trusted and side-effect-free. Relative `--pythonpath` resolves from the selected project root. The default factory and system identifier describe SLDB itself.

## Ownership and Freshness

| Fields | Owner during regeneration |
|---|---|
| Command identity/path, synopsis, arguments, provenance | Assembled parser |
| Surface identity, command inventory, provenance | Assembled parser |
| Purpose, how_it_works, usage examples, tags | Documentation author; preserved |

New explanations are marked `Not documented.` rather than inferred from option names. New command usage starts with argparse's usage string; existing examples remain authored. Arguments are represented as JSON inside the Markdown field, including required flags, defaults, choices, converters, cardinality, action type, and mutually exclusive groups.

The `provenance` field identifies the parser factory and command path and includes `contract-sha256`. This is a fingerprint of parser facts, not a claim that handler logic was analyzed. A handler-only change may require updating authored explanations without changing the parser contract.

Hidden commands/options are omitted by default; `--include-hidden` includes them. SLDB's `init` and `example` now carry public parser help because they are supported bootstrap commands. Alias paths are represented separately. Filename collisions are rejected before sync writes documents.

## Findings and Limits

JSON reports distinguish missing files, changed generated fields, missing tracking, stale document hashes, and removed commands. `check` exits 0 when current and 1 when findings remain. Invalid inputs fail without starting document writes. `sync` retains obsolete documents and exits 1 while removed-command findings remain; removal/untracking is a separate explicit operation.

All expected payloads are validated before writes and original file contents are checked before applying a plan. Persistence uses existing SLDB operations, not a transaction spanning all documents; an I/O failure can require rerunning sync. Custom parser defaults must have deterministic JSON representations. Automatic rename equivalence and a general call graph are follow-up work.

See [tests](../tests/selfdoc/) and [remaining findings](documentation-review.md); the self-documentation task closed in aca36681.

## Structural Architecture Evidence

The Python inventory makes source symbols trackable; [the spec2viz AST view](architecture/spec2viz/python-ast.md) adds a reproducible module/import projection. It is deliberately adjacent to, rather than a replacement for, curated semantic architecture specs.

FILE:instruccion
Cold-bundle de la tarea task-decisión-de-jp-python-sync-o-stores-build-destrackean-los-pythonsymboldoc-cuyo-símbolo-desapareció: con el TaskDoc, los rituales enrutados por el Board, las pills ligadas, los átomos ligados y los archivos que el TaskDoc nombra, reformula el encargo, lista ambigüedades con cita textual del input y da el DRY-RUN sin ejecutar nada. No ejecutes nada.

Sección de validación del TaskDoc:
- grep -n 'Símbolos que desaparecen' docs/self-documentation.md

