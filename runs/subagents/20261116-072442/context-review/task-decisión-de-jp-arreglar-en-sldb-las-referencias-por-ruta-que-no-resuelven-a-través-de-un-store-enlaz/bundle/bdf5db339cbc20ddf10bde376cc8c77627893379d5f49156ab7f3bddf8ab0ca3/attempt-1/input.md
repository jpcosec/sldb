FILE:desk/tasks/task-decisión-de-jp-arreglar-en-sldb-las-referencias-por-ruta-que-no-resuelven-a-través-de-un-store-enlaz.md
---
sldb:
  by: agent
  at: '2026-11-16T06:21:52Z'
  authority: generated
  via: save_document_payload
id: task-decisión-de-jp-arreglar-en-sldb-las-referencias-por-ruta-que-no-resuelven-a-través-de-un-store-enlaz
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
- docs/architecture/references.md
task_type: task.decision
inherits_from: []
inherit_acceptance_context: false
atoms: []
from_drawer: desk/drawer/tasks/task-linked-store-path-references-cannot-resolve-despite-tracked-targets.md
---

# Decisión de JP: arreglar en sldb las referencias por ruta que no resuelven a través de un store enlazado, o cerrarlo como wontfix

## Rationale

_Explain why this task exists or the business driver behind it._

Resolviendo reportes de MEPU en deskops se reprodujo que `sldb edges unresolved` muestra como unknown_path 11 rutas de pills y rituales del Board solo cuando se lee a través de un store enlazado; todas existen y están trackeadas, y el edges unresolved local está vacío. Causa: _resolve (src/sldb/store/edge_index/declared_resolution.py:57-58) solo usa los dueños de ruta cuando store es None, y _owners_by_path (src/sldb/store/edge_index/composition_targets.py:37-49) deja fuera a propósito los documentos de stores enlazados. deskops ya lo esquiva y la nota dice que no hay plan de workaround en sldb. Arreglarlo (resolver la ruta en el espacio del store fuente, con dueños por (store, ruta)) cambia la regla de aislamiento entre stores, por eso es decisión del dueño. Origen: drawer desk/drawer/tasks/task-linked-store-path-references-cannot-resolve-despite-tracked-targets.md.

## Goal

_Describe the concrete result this task must produce._

JP decide (a) arreglar: se crea la tarea de código con test en tests/api/test_unresolved_references.py; o (b) wontfix: queda escrito en docs/architecture/references.md, sección "Rutas a través de un store enlazado", que una ruta relativa se resuelve solo en su store local y por qué.

## Scope

_State what is in scope and what is out of scope._

Entra: presentar a JP las dos opciones; recomendación del coordinador: (a), porque el reporte es un falso unknown_path que confunde a quien lee edges unresolved por la federación, y el arreglo mantiene el aislamiento si la clave es (store, ruta). Registrar el recibo owner (dispose accepted de JP) y ejecutar la consecuencia (crear la tarea o escribir la sección). No entra: implementar el arreglo.

Protocolo de decisión (vale para todo el contrato): el coordinador del desk de sldb le pregunta a JP por el canal de coordinación (herdr o el supervisor), con las opciones, costos y recomendación de este contrato copiados tal cual. La respuesta se registra con `deskops review record <esta tarea> --kind owner --reason "JP <AAAA-MM-DD>: <opción y motivo>" --root sldb`; el dispose accepted lo hace JP con `deskops review dispose <id del recibo> --verdict accepted --reason ... --root sldb`; nada se ejecuta ni se cierra sin ese recibo aceptado. "La fecha" es la de la respuesta de JP, en ISO (AAAA-MM-DD). La sección del documento tiene esta forma: un encabezado "## <nombre de la sección>", una línea "Decisión (AAAA-MM-DD, JP): <opción>", una línea "Motivo: <motivo>" y la lista de las opciones consideradas con su costo. Una tarea que la decisión crea se escribe con deskops add task --root sldb con el contrato completo (title, why, goal, scope, implementation_path, files, validation, done_when) y references a la nota o ítem de origen de esta tarea. El commit del documento lo hace el coordinador con deskops closeout commit; nadie hace push salvo el integrador.
Precisiones (preflight-1): con (a), la tarea creada agrega en tests/api/test_unresolved_references.py un test con dos stores enlazados donde una ruta relativa del store fuente nombra un documento trackeado de ese mismo store y edges unresolved por la federación no lo reporta. Con (b), la sección dice en un párrafo la regla (una ruta relativa se resuelve solo en el store local) y el motivo (aislamiento entre stores). Validation: con (a) basta que exista la tarea; con (b), el grep de la sección.

Referencia kimun (solo lectura, github jpcosec/kimun main b14a30f): el grafo federado arma la parte de cada store enlazado con los dueños de ruta de ESE store (src/kimun/surface/edges.cljc:436, store-parts) y después califica sus ids con el nombre del enlace (qualify-node-id, edges.cljc:396-410); una ruta que no resuelve queda como nodo unresolved_path explícito (edges.cljc:344). Los enlaces guardan la ruta relativa al store (doc v2 de kimun 06-superficies-y-cli.md:71). Recomendación para que JP confirme: (a) arreglar. Resolver la ruta relativa de un documento de B con los dueños de B, calificar el id por el enlace como ya hace sldb (store:Model:name) y conservar el aislamiento, porque la clave es (store, ruta).

## Implementation Path

_Outline the expected implementation route or affected surface._

1) Leer el ítem del drawer, declared_resolution.py y composition_targets.py. 2) Pedir la decisión. 3) Crear la tarea o escribir la sección en docs/architecture/references.md.

## Validation

_List the checks required before this task can close._

- grep -n 'Rutas a través de un store enlazado' docs/architecture/references.md || ls desk/tasks | grep -i enlazado

## Done When

_Name the observable condition that makes the task complete._

Recibo owner aceptado por JP; existe la tarea de código (a) o la sección del doc (b) commiteada.

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

FILE:docs/architecture/references.md
# Incoming references: find them and rewrite them

`sldb.api.referrers(store, target)` lists every place that refers to a document or to a project
graph node; `sldb.api.rewrite_references(store, target, replacement)` rewrites them all to name
something else, or removes them, in one transaction. This is node GD22 of the plan
`generalizar-desde-deskops`: the "find inbound references and rewrite them" that deskops kept
as a walk over `desk/` with a regex (atom merges, retire checks) becomes a read of the two
indexes sldb already keeps, the edge index (GD21 reads it too) and the project graph (GD21),
written through the transaction of GD24.

## What a reference is

Two kinds, told apart by `origin`:

| `origin` | Where it comes from | What it is |
|---|---|---|
| `schema` | The store's composed edge index (`edges_to`): every references or contains (containment) edge a declared field produces (`__references__`, `__reference_models__`, `__containment__`, and the `__doc_anchors__` fields of GO07). | A value of a tracked document's field: a scalar, or one element of a list (`index` is its position). The value is read as it was written (`metadata.declared`). |
| `mention` | The project graph of GD21 (`ProjectGraph.edges_to`): every edge a `MentionPattern` of `line_mentions` or `section_mentions` declared, located `line:N:<label>`. | A text a pattern captured on line `N` of a project file (tracked or not). `location` is `path:N`. |

Not references, by this node: the frontmatter declarations of untracked documents the project
graph reads through `reference_fields` and `fields_by_kind` (locator `frontmatter`), and the
YAML blocks of a body (`line:N:yaml`). They are declared fields of files sldb does not model,
so neither the index nor a line rewrite can change them safely; they stay in `graph edges --to`.

A `Referrer` is `{source, field, index, location, origin}`:

- `source`: the export id `Model:name` of the referring document (`schema`), or the
  project-relative path of the mentioning file (`mention`);
- `field`: the declared field (`schema`) or `null`;
- `index`: the position in a list field, `null` for a scalar or a mention;
- `location`: `path:line` of a mention, `null` for a field.

Fields come first, sorted by source, field and position; then mentions, by path and line.

## Naming the target

`target` (and `replacement`) is resolved in this order (q6):

1. a tracked document, by `name`, `Model/name`, `Model:name` or its tracked path (the rule of
   `doc_status` plus the export id form); several candidates are
   `SLDBDocumentTargetError` naming them (`Ambiguous document target: card-a (candidates:
   Card:card-a, Review:card-a)`);
2. a project graph node id, `kind:identity`, as `graph project nodes` prints it;
3. anything else is `SLDBDocumentTargetError` (`Unknown document target: ...`).

A document whose file sits on a document surface of the project graph is both: its mentions
are found through its node. A node id that is no document (a `source_file:src/app.py`, a card
that is not tracked) has only mentions. A store that declares no `project_graph` has only
fields.

## Rewriting

```python
from sldb import api

report = api.rewrite_references(store, "card-a", "card-a2")          # every reference now names card-a2
report = api.rewrite_references(store, "card-a", None)               # removed where a field allows it
report = api.rewrite_references(store, "card-a", "card-a2", dry_run=True)
with api.transaction(store) as tx:
    api.rewrite_references(store, "card-a", "card-a2", transaction=tx)  # joins; the block decides
```

| Reference | `replacement` given | `replacement` is `None` (remove) |
|---|---|---|
| scalar field | the field takes the new value | the field becomes `null`; the model decides whether it may (q7): a field that does not admit it fails validation, named in the error, and nothing of the batch is written |
| list field | the element is replaced in place; if the list already holds the new value, the replaced element is dropped instead (never a duplicate) | the element is dropped, no hole is left |
| mention | the captured text is replaced on its line, as a whole token (below) | the mention is kept and reported in `skipped`: prose is never deleted |

**The form of the value is kept (q15).** `replacement` is resolved like `target`. When it is a
tracked document, each value is written the way the original named the target: a bare `name`
becomes the replacement's name, `Model:name` its export id, a tracked path its path, and a
document anchor `doc:Model:name@sha256:...` becomes `doc:Model:name` of the replacement
*without* the hash, so the save pins it to the replacement's contract hash (GO07, q2). A
replacement that resolves to no document (a project node id, or anything else) is written as
given; a `__doc_anchors__` field then refuses it, as its validator refuses any non-anchor.

**Mentions are whole tokens (q16, q18).** A mention token is a run of `[A-Za-z0-9_:./-]`. The
text a `MentionPattern` captured is replaced only where the character before it is outside
that set (or the line starts) and what follows is outside it (or the line ends), so
`card:card-a` rewrites neither `card:card-ab` nor `card:card-a.b`. Dots that end the token and
are followed by a space or the end of the line are sentence punctuation, not part of it:
`Ver card:card-a.` and `card:card-a...` are rewritten and keep their dots. A line whose text is
no longer there, or where the text is not a whole token, goes to `skipped` with the reason. The
new text keeps the form of the mention too: the node id (`card:card-a` → `card:card-a2`), the
node's identity, its path, or the document's name or export id.

**All or nothing (GD24, q3, q9).** The writes run inside `sldb.api.transaction`: the one passed
in, or one the call opens. A document's payload is written with `transaction.update`, so it
goes through `save_document_payload`: the anchors are pinned, the `on_write` rules of GO08 and
the builtin tag family of GD27 run, the document is rendered and tracked again. A mentioning
file is rewritten with `replace_text` (GD27): a tracked document is validated under its model
and tracked again with the same model and name, a plain file is written with its sha256 as
guard. A failure anywhere (a model that refuses a payload, a rule, an I/O error) restores every
document written before it: bytes, index entries and shards.

**Validated before anything is written (q14).** Every new payload is validated and
round-tripped under its model in memory (`validate_model_data_roundtrip`), and the new text of
a tracked mentioning document under its model, before the transaction opens. With `dry_run`
that is all: the `RewriteReport` is computed, nothing is opened for writing, no file changes
(the test hashes every file before and after) and **the `on_write` rules do not run**: they
only run when a document is written.

**Nothing walks the project (q8, q17).** The index is the composed one sldb keeps per process
and the graph the memoized one of GD21; with both warm, `referrers` and a dry run make no
`os.walk`, no `Path.rglob` and no `os.scandir` outside the store's own directories (the shards
signature of the index stat-scans `.sldb_cache/edges`). A real write opens the transaction,
which records the store's signatures (`rglob` under `.sldb/`).

### The report

`RewriteReport` is `{changed, skipped}`:

- `changed`: `{source, field, index, location, before, after}` per reference, in the order of
  `referrers`; `after` is `null` for a removal; a mention's `before`/`after` are the token;
- `skipped`: `{source, location, reason}` per mention left alone.

## CLI and HTTP

```
sldb edges referrers TARGET [--store] [--pythonpath] [--format text|json|yaml]
sldb edges rewrite TARGET --to NEW | --remove [--dry-run] [--store] [--pythonpath] [--format]
GET  /edges/referrers?target=TARGET
POST /edges/rewrite {"target": TARGET, "replacement": NEW | null, "dry_run": false}
```

`--to` and `--remove` exclude each other and one is required (argparse: exit 2, `cli/usage`
under `--envelope`). With `--format json` the commands print the data object itself: the list
of `Referrer`, the `RewriteReport` (q13); `--envelope` wraps it in `data`, and an unknown or
ambiguous target, a refused payload or a rule are the envelope's typed errors (`docs/missing`,
`docs/ambiguous`, `validate/rejected`, `rules/violation`). The HTTP bodies are exactly those
objects (q10): the referrers list, the report. In `POST /edges/rewrite`, `replacement` is
required (`null` removes; absent is 400) and `dry_run` optional (a boolean); a missing or
invalid parameter is 400, an unknown target 404, an ambiguous one 409, a refused write 400
with nothing written (q11).

## Where it lives

- `src/sldb/api/edges/referrers.py`: `referrers`, the target resolution and the search;
  `referrer.py` the `Referrer` model.
- `src/sldb/api/edges/rewrite_values.py`: the field hits read from the index and the payload
  rewritten in the value's form; `rewrite_mentions.py`: the mention hits read from the graph
  and the line rewritten as whole tokens; `rewrite_references.py`: the plan, the in-memory
  validation, the dry run and the transaction; `rewrite_report.py` the `RewriteReport`.
- `src/sldb/cli/commands/edges_rewrite.py`, `src/sldb/cli/parsers/edges.py`,
  `src/sldb/cli/serve/edges_rewrite_routes.py`.
- Tests: `tests/api/test_referrers.py`, `tests/api/test_rewrite_references.py`,
  `tests/test_serve.py` (the HTTP routes against the CLI).

What deskops keeps without reason once it reads this: `_find_inbound_atom_references` and
`_rewrite_inbound_atom_references` (`services/atoms.py`, through `operations.py`), the regex
walk over `desk/` they share, and the inbound check of `services/retire.py`.

FILE:instruccion
Cold-bundle de la tarea task-decisión-de-jp-arreglar-en-sldb-las-referencias-por-ruta-que-no-resuelven-a-través-de-un-store-enlaz: con el TaskDoc, los rituales enrutados por el Board, las pills ligadas, los átomos ligados y los archivos que el TaskDoc nombra, reformula el encargo, lista ambigüedades con cita textual del input y da el DRY-RUN sin ejecutar nada. No ejecutes nada.

Sección de validación del TaskDoc:
- grep -n 'Rutas a través de un store enlazado' docs/architecture/references.md || ls desk/tasks | grep -i enlazado

