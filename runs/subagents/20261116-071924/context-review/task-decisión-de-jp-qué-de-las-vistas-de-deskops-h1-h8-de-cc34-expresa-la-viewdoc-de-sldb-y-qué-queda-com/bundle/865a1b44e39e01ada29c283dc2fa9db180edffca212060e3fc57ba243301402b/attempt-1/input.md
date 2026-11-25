FILE:desk/tasks/task-decisión-de-jp-qué-de-las-vistas-de-deskops-h1-h8-de-cc34-expresa-la-viewdoc-de-sldb-y-qué-queda-com.md
---
sldb:
  by: agent
  at: '2026-11-16T05:22:00Z'
  authority: generated
  via: save_document_payload
id: task-decisión-de-jp-qué-de-las-vistas-de-deskops-h1-h8-de-cc34-expresa-la-viewdoc-de-sldb-y-qué-queda-com
status: draft
summary: ''
tags:
- workspace:desk
- artifact:task
- host:robocop2
current_node: ritual-execution
history: []
references:
- desk/inbox/inbox-note-viewdoc-run-view-lo-que-el-modelo-no-expresa-para-las-vistas-de-deskops-h1-h8-y-huecos-de-run-view-h.md
depends_on: []
pills: []
files:
- docs/architecture/views.md
task_type: task.decision
inherits_from: []
inherit_acceptance_context: false
atoms:
- atom-sldb-evaluates-declared-rules-consumers-author-them
- atom-una-vista-es-un-documento-que-declara-qué-leer-y-sldb-la-ejecuta
---

# Decisión de JP: qué de las vistas de deskops (H1-H8 de CC34) expresa la ViewDoc de sldb y qué queda como agregado del consumidor

## Rationale

_Explain why this task exists or the business driver behind it._

deskops view board|task salen de sldb.api.run_view proyectado al contrato de el doc deskops-ui.md del repo deskops. Lo que la ViewDoc no expresa lo completa el CLI de deskops con lecturas existentes, marcadas "pendiente de sldb Hn". CC34 listó ocho cosas: (H1) transitions.from_field necesita export id; (H2) transitions admite una sola relation y el ciclo tiene tres; (H3) gates con holds=false no aparecen; (H4) closeout no tiene fuente sin recibos evidence; (H5) next sale del spec yaml del paquete; (H6) pills/atoms/validation efectivos por herencia no están en el índice; (H7) el texto crudo del drawer no está en las filas; (H8) no hay revision por nota del inbox. La nota pide que la ViewDoc las exprese o una decisión explícita de que quedan del lado del consumidor. Es una decisión de alcance del modelo ViewDoc (sldb) frente a deskops, por eso es del dueño. Origen: desk/inbox/inbox-note-viewdoc-run-view-lo-que-el-modelo-no-expresa-para-las-vistas-de-deskops-h1-h8-y-huecos-de-run-view-h.md.

## Goal

_Describe the concrete result this task must produce._

JP decide, para cada una de H1-H8, "sldb" (la ViewDoc lo expresa y se crea una tarea de código en sldb) o "consumidor" (deskops lo agrega fuera de run_view y quita la marca "pendiente de sldb Hn"); la decisión queda escrita en docs/architecture/views.md, sección "Decisión H1-H8 (CC34)", con la fecha y una línea por hipótesis.

## Scope

_State what is in scope and what is out of scope._

Entra: presentar a JP las ocho hipótesis con esta recomendación del coordinador: H1, H2 y H3 a sldb (son del modelo de transiciones que ya vive en sldb: export id en from_field, varias relations, gates no sostenidos); H4-H8 al consumidor (dependen de recibos, specs de paquete, herencia y archivos no trackeados que son de deskops, en línea con el atom atom-sldb-evaluates-declared-rules-consumers-author-them). Registrar su respuesta en docs/architecture/views.md, crear con deskops add task una tarea de código en sldb por cada H que quede en "sldb", y mandar a deskops con deskops message send --to deskops la lista de las que quedan del consumidor. No entra: implementar nada; H9-H13 (resueltas o en otra tarea).

Precisiones (preflight-1): la sección "Decisión H1-H8 (CC34)" de docs/architecture/views.md lleva una línea por hipótesis con la forma "- H<n> (<resumen de una línea>): sldb | consumidor — <motivo>". H9 a H13 no se deciden aquí y no se mencionan en la sección (H9 y H11 están resueltas en 04a0e94e y 47b75674; H12 y H13 son la tarea task-run-view-dice-que-el-store-no-está-construido-en-vez-de-unknown-view-h12-y-se-reproduce-si-la-revisi). El mensaje a deskops lleva como título "ViewDoc: H1-H8 decididas" y como cuerpo la lista de las H que quedan del consumidor con su línea de la sección.
Protocolo de decisión (vale para todo el contrato): el coordinador del desk de sldb le pregunta a JP por el canal de coordinación (herdr o el supervisor), con las opciones, costos y recomendación de este contrato copiados tal cual. La respuesta se registra con `deskops review record <esta tarea> --kind owner --reason "JP <AAAA-MM-DD>: <opción y motivo>" --root sldb`; el dispose accepted lo hace JP con `deskops review dispose <id del recibo> --verdict accepted --reason ... --root sldb`; nada se ejecuta ni se cierra sin ese recibo aceptado. "La fecha" es la de la respuesta de JP, en ISO (AAAA-MM-DD). La sección del documento tiene esta forma: un encabezado "## <nombre de la sección>", una línea "Decisión (AAAA-MM-DD, JP): <opción>", una línea "Motivo: <motivo>" y la lista de las opciones consideradas con su costo. Una tarea que la decisión crea se escribe con deskops add task --root sldb con el contrato completo (title, why, goal, scope, implementation_path, files, validation, done_when) y references a la nota o ítem de origen de esta tarea. El commit del documento lo hace el coordinador con deskops closeout commit; nadie hace push salvo el integrador.

## Implementation Path

_Outline the expected implementation route or affected surface._

1) Leer docs/architecture/views.md y la nota de origen. 2) Pedir la decisión a JP (registrar el recibo owner con deskops review record <tarea> --kind owner; el dispose accepted lo hace JP). 3) Escribir la sección en views.md. 4) Crear las tareas resultantes y mandar el mensaje a deskops. 5) Commit del doc.

## Validation

_List the checks required before this task can close._

- grep -n 'Decisión H1-H8 (CC34)' docs/architecture/views.md

## Done When

_Name the observable condition that makes the task complete._

views.md tiene la sección con las ocho líneas; existe una tarea en desk/tasks por cada H decidida "sldb"; deskops recibió el mensaje; recibo owner aceptado por JP; commit con el doc.

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

FILE:desk/atoms/atom-sldb-evaluates-declared-rules-consumers-author-them.md
---
id: atom-sldb-evaluates-declared-rules-consumers-author-them
title: sldb evaluates declared rules; consumers author them
five_wh_one_plus: what
tags:
- system:sldb
- system:deskops
- topic:boundary
- topic:rules
---

# sldb evaluates declared rules; consumers author them

## Answer

sldb evaluates declared rules over documents, edges and content hashes: a predicate language with quantifiers over relations, RuleDoc documents with a subject family, a severity and a moment, doc: anchors pinned to a contract hash, and transitions carried as edge data. Which rules exist, what a task type is and what a workflow gate means is authored by consumers such as deskops, as documents in their own desks; sldb only evaluates them, with an explanation, incrementally, and never persists a derived result. Owner decision D1 of 2026-11-04 (desk/drawer/plans/grafo-operable/decisiones.md); the generic evaluator lives in sldb, the specific rules outside it.

FILE:desk/atoms/atom-una-vista-es-un-documento-que-declara-qué-leer-y-sldb-la-ejecuta.md
---
id: atom-una-vista-es-un-documento-que-declara-qué-leer-y-sldb-la-ejecuta
title: Una vista es un documento que declara qué leer y sldb la ejecuta
five_wh_one_plus: what
tags:
- system:sldb
- topic:views
provenance: docs/architecture/views.md
---

# Una vista es un documento que declara qué leer y sldb la ejecuta

## Answer

Una vista de sldb es un ViewDoc (el de SV01) con params y sections, sin código: cada sección declara select (un selector de GD23, con sustitución {param}), fields, edges (vecinos por relación y dirección), group_by y group_order, rules (RuleDocs de GO06 cuyos findings se agregan a cada fila) y transitions (aristas que se cumplen y bloqueadas, de GO08/GO09). sldb.api.run_view(store, name, params) devuelve las secciones con una revision (sha256 de lo leído) y sldb serve la expone en GET /views/<name> con ETag y 304. Un hecho que sldb no calcula entra como documento que la vista lee, nunca como proveedor computed en Python (DA1). El nombre projection queda reservado para las rutas de SV02. Implementado en GD25 (plan generalizar-desde-deskops).

FILE:docs/architecture/views.md
# Composed views: a `ViewDoc` with sections, evaluated by `run_view`

`sldb.api.run_view(store, name, params)` evaluates a composed view: a `ViewDoc` (the model of
`sldb.models.notation_models`, SV01) whose `sections` say which documents to read and what each
row carries. It is node GD25 of the plan `generalizar-desde-deskops`: a status view, a list or a
report that a consumer used to assemble in its own code is now a document of the store that
sldb evaluates, serves and revisions. A `ViewDoc` without `sections` is a projection view of
the graph (SV02, `/views/projection*`), untouched.

There is no extension point in Python (decision DA1): no view provider, no `computed` field.
A fact sldb does not derive (the result of a build, a review that happened outside) is a
document the consumer writes to the store, linked to the document it is about; the view reads
it through `select`, `edges` or `rules` like any other document.

## The document

```yaml
id: tablero
name: tablero            # the view's name; `projection` is reserved and refused on write
title: Tablero
params:                # list of {name, required, default}; every value is a string
  - {name: owner, default: ana}
sections:              # ordered; each key is a key of the result
  - key: cards
    select: {model: Item}                 # a selector of `select_documents` (selectors.md)
    fields: [title, status, owner]        # projected fields of each row; `*` = all (default)
    group_by: status                      # groups the rows by this field...
    group_order: [open, review, done]     # ...in this order (a value without rows still appears)
    edges:                                # neighbour ids added to each row, one key per entry
      - {relation: depends_on, direction: out, as: depends_on}
      - {relation: depends_on, direction: in, as: blocked_by}
      - {relation: item, direction: in, as: receipts}
    rules: [owned]                        # RuleDocs evaluated on each row (`findings`)
    transitions: {from_field: stage, relation: moves_to}   # `holding` and `blocked` per row
  - key: mine
    select: {model: Item, where: "owner = {owner}"}
    fields: [title]
```

What one document must say on its own is checked by the model's validators when it is
written (`create_document`, `save_document_payload`, `sldb docs ...`): `params` is a list of
`{name, required, default}` with unique identifier names (a required param has no default);
section keys are unique; `select` is a non-empty mapping of selector keys (`ref`, `prefix`,
`path_glob`, `model`, `where`, `include_linked`) whose strings are not blank and whose
`where` parses; every `{param}` a selector value references is declared; `edges` entries have
a `relation` and a `direction` (`out` | `in`); `transitions` is exactly `{from_field,
relation}`; the name `projection` is refused. A rejected document is not written.

Whether a rule names a RuleDoc the store has depends on the store, so `run_view` checks it:
an unknown rule is `SLDBDocumentTargetError` naming the view, the section and the rule.

## Params

`{name}` in a selector value is filled when the view runs. In `where` the value enters as a
string literal of the predicate (`owner = {owner}` runs as `owner = "ana"`; a value holding a
double quote is refused); in any other key it enters as text (`prefix: "{team}-"`). Values
are strings by every route: `--param k=v` (repeatable; a repeated key is a usage error),
`?k=v` on HTTP, a `dict[str, str]` in Python. A param not declared is an error naming it; a
required one that is absent is an error naming it; a default applies when the param is absent.
The result's `params` are the values the view ran with.

## The result

```json
{"view": "tablero", "params": {"owner": "ana"}, "revision": "<sha256>",
 "sections": {"cards": {"groups": [{"value": "open", "rows": [...]}, ...]},
              "mine": {"rows": [...]}}}
```

A section without `group_by` is `{"rows": [...]}`, in selection order (by path, the local
store's rows first). With `group_by` it is `{"groups": [{"value", "rows"}]}`: first the
values of `group_order`, each present even with no rows (the columns of a status view do not disappear),
then the other values sorted, then, only when there are such rows, the rows without the field
under `"value": null`.

Each row is `{export_id, model, name, path, fields}`, `fields` being the projected fields the
section asked for (the edge index's payload projection: top-level scalars and lists of
scalars, never a re-extraction; `*` = all of them; a field the document lacks is `null`), plus,
only when the section declares them:

| Key | Declared by | Value |
|---|---|---|
| one per `edges` entry, named by its `as` (default `<direction>:<relation>`) | `edges` | the sorted ids reached along that relation in that direction: the index's neighbours (a relation type, or a declaring field of a references or contains (containment) edge) first, then, when the store declares a `project_graph` (GD21), the project graph's for the same relation, each as the document's export id when the index tracks it and as its project node id otherwise, without duplicates |
| `findings` | `rules` | the findings (`Finding.as_dict()`: level, code `rules/<name>`, subject, what, fix, document) of the named rules that apply to the row's document and do not hold, as `sldb rules check` reports them; `what` carries the clause that decided it |
| `holding`, `blocked` | `transitions` | what `edges_holding` and `edges_blocked` answer for the node whose id is the row's `from_field` value (`Model:name`), with the row's projected payload as subject and the row's document for its `on_transition` rules: each edge with its `effects` and, in a store with RuleDocs, its `findings`; an `error` finding moves every edge to `blocked`. Both empty when the row has no `from_field` value |

## The revision

`revision` is the sha256 of: the `source_hash` of every document in the rows (sorted), the
`content_hash` of the ViewDoc and of every RuleDoc a section used, and the store's shards
signature. The shards signature is always in, because a new edge reaching a row (another
document that starts pointing at it) moves the shards and not the row's own document; so
edges, rules and transitions are covered. Writing a document of the rows, editing the ViewDoc
or a RuleDoc, or writing any document that moves the shards changes it; two evaluations with
nothing written in between give the same value. A surface no document models (a file the
project graph reads, say) does not move it.

## A view from a linked store

A `ViewDoc` need not live in the store that runs it (H9; deskops ships its views only in its
package store, decision DA4, and a desk reaches them through the link). `run_view`, `list_views`
and therefore `views run|list` and `GET /views[/<name>]` read the composed index (the store and
the stores it links to, where a linked document is `<link>:ViewDoc:<name>`):

- **Which one a name means.** The local `ViewDoc:<name>` first; else the only linked ViewDoc with
  that name; `<link>:<name>` names a linked one directly. Two or more linked ViewDocs with the
  name and no local one is `SLDBDocumentTargetError('Ambiguous view: <name> (linked in <s1>, <s2>)')`
  (`docs/missing`, 404): sldb does not pick one.
- **Where its file is read.** From the root of the store that tracks it (the linked one), which
  the index records in the node's `facets.source.store_path`, through the read guard of
  `sldb.store.source_read`: a path that resolves outside that root or is a symlink is not read
  (`SLDBDocumentTargetError` naming `outside-root` or `symlink`).
- **What it reads.** The sections select, project and join over the store that calls, never over
  the store the ViewDoc comes from: the view is a definition, the calling store is the data.
- **The catalogue.** `list_views` lists local and linked views by name; a linked view whose name
  another view also has (local or linked) is listed `<link>:<name>`, which `run_view` accepts.
- **The revision** takes the ViewDoc's `content_hash` from the shard of the store that tracks it,
  so editing a linked view moves it too.

## What a run reads (H11)

`run_view` composes the edge index of the calling store alone; it reads the linked stores too
only when something the view evaluates can name one: a section whose `select` has
`include_linked` true or a `ref` or `prefix` behind a link's alias (after the params are filled),
a section with `edges` or `transitions` when a declared reference of the calling store's own
documents names a document behind a link alias, or a ViewDoc that only a linked store tracks
(H9). The criterion reads the definition, never a fixed list, and is conservative: when any
section needs the linked stores, all of them are read. The result does not change: the
revision's shards signature is the calling store's, and a change in a linked store moves the
revision of a view that selects from it (through the rows it reads) and no other.

The composed index outlives the process: `.sldb_cache/composed/<request>.json` of the calling
store holds it (plain JSON, never executed) with the key it was composed under: every federated
store's shard and document-shard state, the models' contracts and this sldb's index version.
Another key, a missing or unreadable file is a miss: the shards are read as before and the file
rewritten. The files a document moved to from outside sldb (`stale`) are checked on every read
against the files on disk, as before.

## CLI and HTTP

- `sldb views run NAME [--param k=v ...] [--store] [--pythonpath] [--format]`: the result
  (`--format json` emits it exactly; the text form lists each section's groups and ids).
- `sldb views list`: `{"views": [{name, title, params, sections: [key...]}]}` of the ViewDocs
  with sections, by name. The projection views stay in `sldb notations` / `GET /views/projection`.
- Both take the standard envelope (`--envelope`): `ok`, `command`, `store`, `data` (the JSON
  above), `warnings`; on failure `error: {type, message}` (`docs/missing` for an unknown view
  or rule, `validate/rejected` for a param or a projection view, `cli/usage` for a malformed
  or repeated `--param`).
- `GET /views` answers what `views list --format json` prints. `GET /views/<name>?k=v` answers
  what `views run` prints, with `ETag: "<revision>"`; a request whose `If-None-Match` names it
  (weak or strong, or `*`) gets `304 Not Modified` with the `ETag` and no body. 404 for an
  unknown view, 400 for a projection view or a param the view rejects. `/views/projection*`
  (SV02) keeps answering as before.

## Reading cost

One evaluation loads the edge index once, builds the rule graph once (only when a section has
`rules` or `transitions`) and reads it over one view of the index shared by every row, and
builds the project graph once (only when `store.yaml` declares one and a section has `edges`).
The tablero above over 200 items evaluates warm in well under a second (q12, measured in
`tests/api/test_views.py`).

FILE:instruccion
Cold-bundle de la tarea task-decisión-de-jp-qué-de-las-vistas-de-deskops-h1-h8-de-cc34-expresa-la-viewdoc-de-sldb-y-qué-queda-com: con el TaskDoc, los rituales enrutados por el Board, las pills ligadas, los átomos ligados y los archivos que el TaskDoc nombra, reformula el encargo, lista ambigüedades con cita textual del input y da el DRY-RUN sin ejecutar nada. No ejecutes nada.

Sección de validación del TaskDoc:
- grep -n 'Decisión H1-H8 (CC34)' docs/architecture/views.md

