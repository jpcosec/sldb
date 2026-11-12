FILE:desk/tasks/task-run-view-no-compone-en-cada-proceso-el-índice-de-aristas-de-todos-los-stores-enlazados-sldb-views-ru.md
---
sldb:
  by: agent
  at: '2026-11-12T02:26:09Z'
  authority: generated
  via: create_document
id: task-run-view-no-compone-en-cada-proceso-el-índice-de-aristas-de-todos-los-stores-enlazados-sldb-views-ru
status: draft
summary: ''
tags:
- workspace:desk
- artifact:task
current_node: ritual-execution
history: []
references: []
depends_on: []
pills: []
files:
- src/sldb/api/views/
- src/sldb/api/edges/
- src/sldb/store/edge_index/
- src/sldb/store/io/
- tests/
- docs/architecture/views.md
- CHANGELOG.md
- contracts/layers.toml
task_type: task.debug
inherits_from: []
inherit_acceptance_context: false
atoms: []
---

# run_view no compone en cada proceso el índice de aristas de todos los stores enlazados: sldb views run board y deskops view board en menos de 1 s con el store construido (H11)

## Rationale

_Explain why this task exists or the business driver behind it._

H11 de la nota de sldb 9c08039a (hallada por CC34 de deskops), meta de CC52 de deskops. run_view carga el índice de aristas con todos los stores enlazados en cada proceso aunque las secciones del board solo seleccionen documentos locales, y ese índice no persiste entre procesos. En el desk real de deskops, deskops view board tardó 38,4 s, el 95 % en run_view.

## Goal

_Describe the concrete result this task must produce._

Con el store construido, sldb views run board y deskops view board, en un proceso nuevo cada vez, tardan menos de 1 s sobre el desk de deskops con sus stores enlazados; en frío (sin caché de disco) no tardan más que hoy; el resultado y la revision de la vista no cambian.

## Scope

_State what is in scope and what is out of scope._

En alcance: cómo run_view y load_edge_index obtienen el índice de aristas (qué stores y qué shards lee, y si algo de ese trabajo persiste entre procesos), el costo por shard, tests, docs de vistas y CHANGELOG. Fuera: H12 (el mensaje cuando el store no está construido), H13 (la revision depende de cachés del proceso), la ViewDoc de deskops y el contrato de la vista; cualquier cambio en el resultado de una vista.

## Implementation Path

_Outline the expected implementation route or affected surface._

Origen: nota de inbox 9c08039a (H11). Corre después de la tarea de H1-H3 (stores check no aborta), que toca el mismo índice de aristas en sldb.

REPRODUCCIÓN (coordinador, con caché frío y con el store construido; runs/subagents/20261112-repro-h11/repro.log). Layout en /dev/shm: deskops origin/main d120766d y sus stores enlazados (sldb b965c62d, spec2viz, scion; pron no tiene store), cada uno en un worktree; sldb stores build del store de deskops rc 0; XDG_CACHE_HOME vacío. deskops view board, proceso nuevo cada vez: 9,4 s y 9,7 s. Perfil de sldb.api.run_view en un proceso nuevo: 10,89 s, de los cuales 8,90 s en load_edge_index (run_view.py:72, edge_reading.py:14), 8,86 s en compose_edge_index, cuatro _merge_store, 5067 llamadas a _cached_shard (7,49 s) y 4606 yaml.load (6,06 s). El loader ya es libyaml: lo caro es construir los objetos de miles de shards en cada proceso. A la escala real (~10 000 shards) el informe de CC34 midió 38,4 s.

CAUSA (a confirmar): run_view arma su estado con load_edge_index con los stores enlazados incluidos, sin mirar qué documentos pueden seleccionar las secciones de la vista, y el índice compuesto vive solo en la memoria del proceso.

CAMBIO (h1-h5), el worker mide cada opción antes de elegir y lo dice en el informe:
h1: un benchmark reproducible (script que arma el layout y mide cada corrida), commiteado, que da los números de esta tarea con caché frío y caliente.
h2 (menos trabajo): run_view solo lee los shards de los stores que alguna sección puede seleccionar; un store enlazado se lee solo si una sección o un filtro de la vista necesita sus documentos. El criterio sale de la definición de la vista, no de una lista fija.
h3 (persistir): si h2 no alcanza para menos de 1 s, el índice compuesto (o las contribuciones por store) se guarda en disco, con clave por los hashes de los índices de cada store, y el proceso siguiente lo lee entero. Un store que cambió invalida solo lo suyo. No hay estado compartido nuevo entre procesos que pueda quedar viejo: la clave lo evita.
h4 (costo por shard): solo si h2 y h3 no alcanzan, bajar el costo de construir los objetos de cada shard.
h5: el resultado y la revision de una vista salen iguales antes y después, con los mismos datos; un test lo fija. Un store enlazado cambiado se nota en la siguiente corrida. tests/test_clean_code_rules.py es obligatorio (80 líneas efectivas por archivo, 10 de lógica por función, sin subir límites; un archivo nuevo fuera de una carpeta con eje necesita eje en contracts/layers.toml, y los grados medidos salen de tools/check.sh --fast, no de mezclar números). Docs de vistas y CHANGELOG.

VALIDACIÓN: el worker corre de a uno los tests que toca; antes de entregar, la suite completa de sldb de a un archivo desde /dev/shm, test_clean_code_rules y tools/check.sh --fast. Los 7 pasos del workflow de sldb los corre el coordinador. Las reproducciones y las mediciones van siempre con caché frío además del caliente.

## Validation

_List the checks required before this task can close._

- Benchmark commiteado: sldb views run board y deskops view board en proceso nuevo, con el store construido, menos de 1 s sobre el layout de la reproducción
- En frío (sin caché de disco) no más lento que hoy, con el número en el informe
- Test: el resultado y la revision de la vista salen iguales antes y después con los mismos datos; un store enlazado cambiado se nota en la siguiente corrida
- test_clean_code_rules (obligatorio) y tools/check.sh --fast
- suite completa de sldb de a un archivo desde /dev/shm en verde
- 7 pasos del workflow de sldb en clon limpio

## Done When

_Name the observable condition that makes the task complete._

h1-h5 hechos, con las mediciones antes y después en el informe, tests verdes y la suite completa en verde; docs y CHANGELOG actualizados.

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

FILE:contracts/layers.toml
# Contrato de capas
#
# El orden de dependencia entre paquetes, declarado donde se puede leer sin abrir
# código. `tools/check_layers.py` lo verifica y rechaza lo que lo viole.
#
# Regla: un paquete puede importar de su propia capa o de cualquiera MÁS BAJA.
# Nunca hacia arriba. La capa 0 no importa nada del sistema, y por eso es la
# única que se puede extraer y usar sola.
#
# El orden no es una preferencia de estilo: es lo que decide si una pieza se
# puede probar aislada y si alguien puede entender una parte sin cargar el resto.

[[layers]]
level = 0
name = "núcleo"
packages = ["core", "models", "runtime", "code", "notations"]
rationale = """
Convierte texto en estructura y estructura en texto, junto con los tipos de
documento y la configuración que decide qué se permite al renderizar.

Los tres están en la misma capa porque están entrelazados: el renderizador
necesita el tipo base de documento, el tipo base necesita la extracción, y la
extracción necesita el renderizador. Separarlos en capas distintas produciría
tres ciclos en vez de describir el sistema.

Declararlos juntos no disuelve el problema: lo nombra. Mientras esta capa tenga
tres paquetes mutuamente dependientes, ninguno se puede extraer solo. Partirla
es trabajo futuro con diseño propio, no una excepción que se tacha.
"""

[[layers]]
level = 2
name = "persistencia"
packages = ["store", "links"]
rationale = """
Guarda, indexa y consulta. Conoce los contratos, no conoce la interfaz ni la
forma en que un humano pide las cosas.
"""

[[layers]]
level = 3
name = "operaciones"
packages = ["api"]
rationale = """
Las operaciones compuestas sobre el almacén: lo que un programa querría llamar.
Es la frontera pública para quien integra sin pasar por la línea de comandos.
"""

# La capa de transporte traduce entre un humano o un proceso y las operaciones.
# No debe contener lógica que un programa necesite: si algo ahí hace falta sin la
# terminal, va en la capa 3.

[[layers]]
level = 4
name = "transporte"
packages = ["cli", "selfdoc"]
rationale = """
`selfdoc` está acá y no más arriba porque la interfaz lo importa en 14 sitios: no
es un derivado del sistema, es parte de lo que el sistema expone. Clasificarlo
como derivado fue el primer error que esta puerta encontró en su propio contrato.
"""

[[layers]]
level = 5
name = "derivados"
packages = ["examples", "assets", "templates"]
rationale = """
Se derivan del sistema: ejemplos y plantillas. Pueden mirar todo porque nada
depende de ellos.
"""

# ---------------------------------------------------------------------------
# Excepciones vigentes
#
# Cada una es un import que viola el orden de arriba. Están acá para que la
# puerta pase hoy y la deuda quede contada, no escondida: mientras esta lista
# tenga entradas, el orden de capas es aspiracional, no bloqueable.
#
# Las cinco son la arista minoritaria de un ciclo. En cada caso la dirección
# mayoritaria tiene decenas o cientos de aristas y la culpable tiene una sola,
# así que el ciclo es un accidente reparable y no un diseño fusionado.
#
# Retirar una entrada de esta lista es el criterio de terminado de su reparación.
# ---------------------------------------------------------------------------

[allow]
upward = [
  ["selfdoc", "cli"],      # R5
  ["models", "store"],     # R6
]

# R2 (core→store) se reparó: `StoreError` bajó a `core/exceptions/store_error.py`
# y el almacén ahora la reexporta. Importar el núcleo pasó de 103 a 58 módulos.
# La entrada sale de esta lista porque la puerta avisa de excepciones vencidas:
# dejarla autorizaría algo que ya no ocurre.

# R1 (core→runtime) y R3 (models→runtime) ya no figuran acá: al poner los tres
# paquetes del núcleo en la misma capa dejaron de violar el orden. El ciclo
# sigue existiendo y está declarado arriba como lo que impide extraer el núcleo.
# Esto es la diferencia entre resolver y reclasificar, y conviene no confundirlas.

[[pending]]
id = "R1"
edge = "core → runtime"
at = "src/sldb/core/renderer_engine/python_expr.py#L5"
imports = "runtime.config.python_expression_is_allowed"
cycle_weight = "core→runtime: 1 arista · runtime→core: 4 aristas"
repair = """
El núcleo pregunta a la configuración si puede evaluar una expresión. Invertir:
que quien llama pase el permiso como argumento. El núcleo no debe consultar
estado global para decidir qué le está permitido.
"""

[[done]]
id = "R2"
edge = "core → store"
at = "src/sldb/core/exceptions/sldb_store_error.py#L2"
imports = "store.exceptions.StoreError"
cycle_weight = "core→store: 1 arista · store→core: 8 aristas"
repaired = """
Hecho. `StoreError` vive en `core/exceptions/store_error.py` y
`store/exceptions.py` la reexporta. Efecto medido: importar `core.renderer` pasó
de 103 a 58 módulos y de 149 ms a 131 ms, y `tools/check.sh` tiene una puerta que
rechaza la reaparición de la fuga.
"""

[[pending]]
id = "R3"
edge = "models → runtime"
at = "src/sldb/models/structured_doc.py#L67"
imports = "runtime.validation.extract_model_data"
cycle_weight = "models→runtime: 1 arista diferida · runtime→models: 1 arista"
repair = """
Escrito dentro de un método para esquivar el ciclo en tiempo de importación.
El import diferido es la evidencia: alguien ya sabía que el ciclo estaba ahí.
Mover la extracción a la capa que ya depende de ambos, o inyectarla.
"""

[[done]]
id = "R4"
edge = "store → api"
at = "src/sldb/store/edge_index/model_contribution.py#L41"
imports = "api.schema.describe_field.describe_field"
cycle_weight = "store→api: 1 arista diferida · api→store: 195 aristas"
repaired = """
Hecho (2026-10-18). `describe_field` y sus piezas (kinds, descriptor, description) bajaron a
`models/field_schema/`, que el almacén y las operaciones ven; `api/schema` las reexporta. El
almacén las lee por su costura `store/model_contract.py`, y `tests/test_store_seams.py`
rechaza cualquier import del almacén hacia `api`, `cli` o `selfdoc`.
"""

[[pending]]
id = "R5"
edge = "selfdoc → cli"
at = "src/sldb/selfdoc/python_relation_registry.py#L7"
imports = "cli.model_utils.resolve_model_ref"
cycle_weight = "selfdoc→cli: 1 arista · cli→selfdoc: 14 aristas"
repair = """
Resolver una referencia a un modelo no es trabajo de la interfaz: es una
operación. Subirla a la capa 3 y que ambos la llamen desde ahí.
"""

[[pending]]
id = "R6"
edge = "models → store"
at = "src/sldb/models/rule_doc.py#L62"
imports = "store.graph.language.predicate_parser.parse_predicate"
cycle_weight = "models→store: 1 arista diferida · store→models: las costuras del almacén"
repair = """
GO06: `RuleDoc` valida con sus validadores pydantic que `condition`, `where` y `subject`
parseen en el lenguaje de reglas (principio del dueño: las invariantes de un documento son
del modelo), y el parser vive en el almacén. Diferido dentro de la función para no cerrar el
ciclo al importar. Reparación: bajar el tokenizador y el parser del lenguaje (sin el
evaluador ni la vista de grafo) a la capa 0, junto con `WherePredicateError`, y que el
almacén los reexporte, como se hizo con `StoreError` en R2.
"""

# ---------------------------------------------------------------------------
# Ejes de capacidad
#
# Las capas de arriba responden «¿quién puede importar a quién?». Esto responde
# otra pregunta: «¿qué sabe hacer el sistema?».
#
# Son dimensiones ortogonales. Una capacidad puede repartirse entre capas, y dos
# paquetes de la misma capa pueden no tener nada que ver. El mapa completo, con
# el acoplamiento medido entre ejes, en propuesta/04-LOS-EJES.md.
#
# Cada eje declara su dependencia externa. Esa es la prueba más simple de que un
# eje es real: si una biblioteca de terceros está confinada a un eje, el eje
# tiene frontera.
#
# No todas se confinan. `pydantic` y `pyyaml` son transversales por diseño —el
# sistema entero está hecho de modelos validados— y vigilar su confinamiento
# produce decenas de falsos positivos que entierran los hallazgos reales. Se
# declaran acá como transversales para que la puerta no las persiga.
#
# Las que SÍ se confinan son las interesantes: `markdown-it-py` en superficie,
# `jinja2` en render, `networkx` en grafo y semántica. Cada una delimita un motor
# reemplazable.

[axis_external]
pervasive = ["pydantic", "pyyaml"]
confined = ["markdown-it-py", "jinja2", "networkx"]
# ---------------------------------------------------------------------------

[[axis]]
id = "superficie"
paths = ["core/ast", "core/segments", "core/handlers"]
external = ["markdown-it-py"]
does = "texto a árbol unificado; la puerta de entrada de cualquier superficie"
identity = true

[[axis]]
id = "representacion"
paths = ["core/ir", "core/contracts", "core/node.py", "core/node_handler.py"]
external = ["pydantic"]
does = "MeaningNode y SurfaceNode: significado y superficie como proyecciones ancladas"
identity = true
note = "es *la* idea del sistema; sin esto lo que queda es un conversor de formato"

[[axis]]
id = "render"
paths = ["core/renderer_engine", "core/renderer.py", "core/extractor", "core/template_extractor.py", "core/data_extractor.py"]
external = ["jinja2"]
does = "árbol a texto reversible; sin esto la representación es un volcado, no un lugar donde trabajar"
identity = true

[[axis]]
id = "contrato"
paths = ["models"]
external = ["pydantic"]
does = "qué es un documento válido"
identity = true

[[axis]]
id = "runtime"
paths = ["runtime"]
external = []
does = "la configuración que decide qué se permite al renderizar, y la validación que une modelo con texto"
identity = true
note = """
Pequeño y de identidad: `extract_model_data` es la operación que convierte texto
en un modelo validado, que es la mitad del contrato del sistema. `config` decide
si una expresión puede evaluarse. Tres archivos que ningún eje puede absorber sin
volverse otra cosa.
"""

[[axis]]
id = "persistencia"
paths = ["store/io", "store/models", "store/layout.py"]
external = []
does = "guardar, indexar, fragmentar, hashear"
identity = false

[[axis]]
id = "consulta"
paths = ["store/query_engine", "api/search.py", "api/where.py"]
external = []
does = "buscar y filtrar por campo"
identity = false

[[axis]]
id = "grafo"
paths = ["store/graph"]
external = ["networkx"]
does = "recorrer, ciclos, orden, centralidad, similitud estructural"
identity = false
extractable = false
note = """
Casi extraíble, y la puerta lo precisó mejor que yo.

Afirmé que no importaba nada fuera de sí mismo. Falso: cinco archivos lo hacen
—`convert.py`, `node_view.py`, `traversal.py`, `analysis/relations.py`— y traen
`edge_index`, `store.models` y `contrato`. Mi comprobación había truncado las
rutas y vi solo los imports internos.

Lo que sí es cierto: 28 de 33 archivos son autónomos, y las cinco aristas se
concentran en la conversión entre el formato del índice de aristas y el del
motor. Eso es una frontera de adaptación, no una fusión — pero hay que cortarla
antes de llamar al eje extraíble.

Aparte: importarlo arrastra 125 módulos porque `store/__init__.py` se ejecuta
antes. Mismo defecto que R2, otra escala.
"""

[[axis_boundary_debt]]
axis = "grafo"
files = ["store/graph/convert.py", "store/graph/node_view.py", "store/graph/traversal.py", "store/graph/analysis/relations.py"]
imports = ["store/edge_index", "store/models", "models"]
repair = """
El motor debería recibir nodos y aristas en su propio formato. Hoy sabe leer el
del índice. Mover la conversión al índice —que ya depende del motor— deja el
motor sin dependencias y lo vuelve extraíble de verdad.
"""

[[axis]]
id = "indice_de_aristas"
paths = ["store/edge_index"]
external = []
does = "derivar aristas de documentos; el constructor, no el motor"
identity = false
note = "contado junto al grafo en el primer mapa, y es un error: el motor no sabe de documentos"

[[axis]]
id = "recuperacion"
paths = ["api/matching", "api/corpus"]
external = []
does = "similitud aproximada por coseno, con caché de vectores y auditoría del índice"
identity = false
note = """
Sin dependencia externa declarada porque es un PUERTO: la aplicación inyecta un
`Embedder` y sin uno degrada a `difflib`. El eje mejor diseñado del sistema, e
invisible desde las dependencias del proyecto — su diseño consiste en no tenerlas.
"""

[[axis]]
id = "bitacora"
paths = ["store/journal", "api/journal.py"]
external = []
does = "una entrada encadenada por hash por cada escritura, con verificación de la cadena"
identity = false

[[axis]]
id = "adaptadores"
paths = ["selfdoc"]
external = ["ast", "argparse", "click"]
does = "derivar documentos de código y de interfaces"
identity = false
note = "tres adaptadores derivados frente a una sola superficie autorada"

[[axis]]
id = "semantica"
paths = ["store/semantic_parents.py", "store/semantic_dag_sync.py", "store/semantic_doc_contribution.py", "store/semantic_dag_graph.py", "store/semantic.py", "store/semantic_tags.py", "store/semantic_doc_tags.py", "api/semantic"]
external = ["networkx"]
does = "jerarquía de tipos como DAG"
identity = false

[[axis]]
id = "enlaces"
paths = ["links"]
external = []
does = "relaciones declaradas entre documentos"
identity = false

# ---------------------------------------------------------------------------
# Deuda de ejes
# ---------------------------------------------------------------------------

# ---------------------------------------------------------------------------
# Ejes de operación
#
# Los de arriba son motores: saben hacer una cosa con una técnica. Estos son las
# operaciones compuestas que un programa llama, y sin ellos el mapa cubría el
# 40% del sistema.
#
# Mi primer mapa los omitió porque excluí `api/` y `store/` enteros del recuento,
# y ahí vive casi todo el código. Un mapa que ignora el 60% de lo que describe no
# es un mapa.
# ---------------------------------------------------------------------------

[[axis]]
id = "op_documentos"
paths = ["api/documents", "api/actor.py", "api/segments", "store/section_doc_contribution.py", "store/section_paths.py", "store/section_rebuild.py", "store/section_sync.py", "store/documents_dirty.py"]
external = ["markdown-it-py"]
note = """
`section_rebuild.py` usa `markdown-it-py` directamente, fuera del eje de
superficie. Es la única fuga de esa dependencia y vale mirarla: reconstruir las
secciones de un documento debería pedírselo al analizador, no reanalizar.
"""
does = "seguir, dejar de seguir, guardar y navegar documentos y sus tramos editables"
identity = false

[[axis]]
id = "op_modelos"
paths = ["api/model_drafts", "api/model_registry", "api/model_create", "api/schema", "store/model_origin.py", "store/model_import_root.py"]
external = ["ast"]
note = """
Usa `ast` igual que `adaptadores`, y para otra cosa: aquél LEE código para
derivar documentos, éste lo EDITA para modificar un contrato en borrador.

La puerta lo marcó como fuga y no lo es: es la misma herramienta en dos oficios.
Vale declararlo porque la próxima lectura va a dudar igual.
"""
does = "resolver, registrar, describir y editar contratos de modelo en borrador"
identity = false

[[axis]]
id = "op_almacen"
paths = ["api/stores", "api/records", "store/ops.py", "store/export.py", "store/package_version.py", "store/catalog_reconcile.py", "store/runtime_cache.py", "store/diagnostics_models", "store/diagnostics.py", "store/field_set_drift.py"]
external = []
does = "abrir, enlazar, refrescar índices, exportar y diagnosticar un almacén"
identity = false

[[axis]]
id = "op_aristas"
paths = ["api/edges", "api/graph", "store/edge_sync.py", "store/edge_rebuild.py", "store/edge_doc_contribution.py", "store/model_node.py"]
external = []
does = "leer, reconstruir y verificar el índice de aristas; ejecutar consultas de grafo"
identity = false

[[axis]]
id = "codigo"
paths = ["code"]
external = ["ast", "tree-sitter", "tree-sitter-python"]
does = "leer código Python como símbolos con tree-sitter, y un fingerprint por nodo de cada definición (portado de kimun)"
identity = false
note = "no importa nada de sldb: es la superficie de entrada del código, como `core/ast` lo es del Markdown"

[[axis]]
id = "anclaje"
paths = ["api/anchors"]
external = []
does = "anclar una afirmación a un símbolo de código: grabar lo visto, comprobarlo, reconectar lo que se movió"
identity = false

[[axis]]
id = "cache"
paths = ["store/built_cache.py", "store/runtime_cache.py", "store/runtime_cache_disk.py", "store/runtime_cache_signature.py", "store/user_cache.py", "store/derived_rebuild.py"]
external = []
does = "memorizar lo derivado y saber cuándo invalidarlo"
identity = false

[[axis]]
id = "codec"
paths = ["store/codec.py", "store/runtime_codec.py", "store/model_contract.py"]
external = []
does = "serializar y deserializar el estado del almacén, y leer lo que una clase de modelo declara: las costuras del almacén hacia el resto de sldb"
identity = false

[[axis]]
id = "migracion"
paths = ["store/migration.py", "store/migration_hash_names.py", "store/migration_legacy_layout.py", "store/legacy_contract.py"]
external = []
does = "leer almacenes escritos por versiones anteriores"
identity = false
note = "aquí viven las decisiones que los diagnosticadores encontraron solo en comentarios"

[[axis]]
id = "federacion"
paths = ["store/catalog.py", "store/resolver.py", "store/facade.py", "store/query.py", "store/predicates.py"]
external = []
does = "encontrar almacenes, resolver entre varios y ofrecer la fachada de consulta"
identity = false

[[axis]]
id = "errores"
paths = ["core/exceptions", "store/exceptions.py", "core/finding.py", "core/finding_route.py"]
external = []
does = "la jerarquía de excepciones del sistema, y el hallazgo (error o alerta) que reporta un comando"
identity = false
note = "la capa más baja que todas las demás necesitan nombrar; por eso R2 importaba"

[[axis]]
id = "lectura_de_fuentes"
paths = ["store/source_read.py", "store/source_guard.py"]
external = []
does = "decidir si un documento trackeado se puede leer (dentro de la raíz, sin symlinks) y leerlo sin seguir symlinks"
identity = false
note = """
Separado de `identidad_y_hash` en la tarea de seguridad live_stale (inbox 9c9dac6b, 2026-11-11):
calcular una huella y decidir si un archivo se puede abrir son dos trabajos, y
`tests/test_clean_code_rules.py` limita el tamaño de `store/hashing.py`. Mismo nivel que
`identidad_y_hash` (unidad `nucleo`): no importa nada del almacén.
"""

[[axis]]
id = "identidad_y_hash"
paths = ["store/hashing.py", "store/documents_hash.py"]
external = []
does = "calcular y comparar las huellas que detectan deriva"
identity = true
note = """
De identidad porque es lo que hace que un documento derivado sea verificable
contra su origen. Sin esto el sistema produce documentación; con esto produce
proyecciones con detección de rancidez.
"""

[[axis_debt]]
id = "adaptador-sin-uso"
between = ["adaptadores"]
what = """
`selfdoc/click_scanner.py` está escrito completo y no se referencia desde `src/`
ni desde `tests/`. Ningún documento del almacén viene de él.

Y hay algo peor, verificado: **importa `click` en la línea 8, sin `try`, y `click`
no está en las dependencias del proyecto.**

No falla porque nadie lo carga: `sldb.selfdoc` se importa sin traer `click`, y
`click` está en el entorno local por dependencias ajenas (typer, langgraph-cli).
En un entorno limpio, cualquiera que importara este módulo obtendría
`ModuleNotFoundError`.

Es un fallo latente que solo existe porque el código está muerto. La prueba de
que no se ejercita es que el defecto sobrevivió.
"""
repair = """
Dos opciones honestas: declarar `click` como dependencia opcional y ejercitar el
adaptador con un caso real, o retirarlo. Lo que no sirve es dejarlo: parece una
capacidad y es un error de importación esperando.
"""

[[axis_debt]]
id = "superficie-autorada-unica"
between = ["superficie"]
what = """
`MarkdownASTHandler` es la única implementación concreta de `BaseASTHandler` tras
317 commits. La abstracción está ejercitada por tres adaptadores derivados y por
ninguna segunda superficie autorada.
"""
repair = """
Una segunda superficie autorada — o la declaración de que la abstracción es para
superficies derivadas y Markdown es la única autorada por diseño.
"""

# ---------------------------------------------------------------------------
# Unidades viables
#
# Los niveles de arriba son orden de dependencia. Esto es otra cosa: qué partes
# se pueden sostener por separado.
#
# La diferencia importa porque es el error natural al leer el grafo: los seis
# niveles del DAG NO son las unidades. Una unidad viable absorbe su propia
# variedad —cuando algo cambia dentro, se repara dentro— y un nivel no tiene por
# qué.
#
# La prueba: ¿tiene esta pieza sus propias siete funciones? El razonamiento
# completo en propuesta/06-NIVELES-NO-SON-UNIDADES.md.
# ---------------------------------------------------------------------------

[[axis]]
id = "vocabulario_visual"
paths = ["notations", "models/notation", "models/notation_models.py"]
external = ["pydantic", "pyyaml"]
does = "notaciones, glifos, enlaces, paletas y vistas como modelos y catálogos builtin; absorbido de spec2viz (SV01)"
identity = false
note = """
Capa 0 a propósito: es vocabulario, no operación. La comprobación de que un `where`
parsea es un PUERTO (`where_check.connect_where_check`) que `api/notations` conecta al
parser del almacén; sin él no se comprueba, igual que cuando vivía fuera de sldb.
"""

[[axis]]
id = "vistas"
paths = ["api/notations"]
external = []
does = "resolver una notación sobre documentos del almacén y evaluar vistas de proyección; sincronizar notaciones y paletas (SV02)"
identity = false

[[axis]]
id = "reglas"
paths = ["api/rules", "api/tags"]
external = []
does = "evaluar RuleDoc con el lenguaje de predicados en escritura, transición y check, incremental y a punto fijo; los espacios de etiquetas como familia de reglas (GO06, GO08, GD27)"
identity = false
note = """
`api/tags` va acá y no en `semantica`: un espacio de etiquetas se verifica como una familia de
reglas (`builtin_tag_rules.py`, docs/architecture/tags.md), y `tag_check` es `rules check`
filtrado a esa familia. Clasificado en main-de-sldb-en-verde (2026-11-10), decisión revisable
del coordinador; alternativas descartadas en runs/subagents/sldb-ci-worker-report.md.
"""

[[axis]]
id = "vistas_compuestas"
paths = ["api/views"]
external = []
does = "evaluar un ViewDoc con sections sobre un almacén, y el catálogo de vistas (GD25)"
identity = false
note = """
No va en `vistas` (unidad `notacion`): consume grafo, índice de aristas y persistencia, y
sumarlo a `notacion` la llevaba de necesitar 4 a 12, una consumidora neta como `operacion`.
Clasificado en main-de-sldb-en-verde (2026-11-10), decisión revisable del coordinador.
"""

[[unit]]
id = "nucleo"
axes = ["superficie", "representacion", "render", "contrato", "runtime", "identidad_y_hash", "lectura_de_fuentes", "errores", "codigo"]
needs = 5  # medido 2026-11-10 (main-de-sldb-en-verde): GO06 suma contrato → grafo (models/rule_doc.py:62); antes 4/39
needed_by = 54  # medido 2026-11-11 (secrest2): enlaces, adaptadores (selfdoc), op_aristas y op_modelos leen y escriben por la guarda lectura_de_fuentes (store/source_guard.py); antes 50. medido 2026-11-11 (secrest, rebasada sobre H9): las lecturas guardadas de consulta, secciones, semántica y aristas suman aristas hacia lectura_de_fuentes; antes 47. 2026-11-11 (H9): vistas_compuestas lee la ViewDoc enlazada por lectura_de_fuentes (api/views/view_source.py); antes 46. 2026-11-11 (seguridad live_stale): eje nuevo lectura_de_fuentes en nucleo; antes 43. 2026-11-10: GD26 op_almacen → runtime, y los ejes reglas y vistas_compuestas (→ contrato, errores, runtime); antes 4/39
indivisible = false
why = """
Los cinco ejes de identidad forman un nudo de 11 aristas internas. Lo declaré
indivisible y es falso: el corte mínimo son 4 aristas de peso total 6, calculado
por fuerza bruta sobre las 11.

Primero afirmé que bastaba mover `runtime/validation.py`. Lo simulé y el nudo
seguía: mover un archivo cambia de sitio el problema sin resolverlo.
"""

[nucleo_min_cut]
edges = 4
total_weight = 6
cuts = [
  { edge = "superficie → render", at = "core/segments/instrumented_render.py#L16", imports = "SLDBRenderer", weight = 3, note = "un render instrumentado dentro del eje de superficie: está del lado equivocado" },
  { edge = "representacion → superficie", at = "core/node_handler.py#L3", imports = "SharedNodeHandler", weight = 1, note = "una pieza de representación que conoce al que la va a manejar" },
  { edge = "render → runtime", at = "core/renderer_engine/python_expr.py#L5", imports = "python_expression_is_allowed", weight = 1, note = "es R1" },
  { edge = "contrato → runtime", at = "models/structured_doc.py#L67", imports = "extract_model_data", weight = 1, note = "es R3; import diferido" },
]

[[unit]]
id = "persistencia"
axes = ["persistencia", "consulta", "federacion", "cache", "codec", "migracion", "bitacora", "semantica", "indice_de_aristas"]
needs = 24  # medido 2026-11-11 (secrest): lecturas de documentos trackeados por la guarda lectura_de_fuentes; antes 22. 2026-11-11 (seguridad live_stale): aristas nuevas hacia el eje lectura_de_fuentes; antes 21. 2026-11-10 (main-de-sldb-en-verde): GO05 api/where.py → op_aristas, GD23 query_engine/document_selection.py → op_modelos; antes 19/36
needed_by = 47  # medido 2026-11-10: GO07, GD23, GD24 (op_documentos y anclaje → codec, consulta, indice_de_aristas) y los ejes reglas y vistas_compuestas; antes 19/36
why = "el centro de gravedad del sistema: 110 aristas entran desde los ejes de operación"

[[unit]]
id = "grafo"
axes = ["grafo"]
needs = 5  # GO03: eval de store/graph/backend reutiliza el parser where de store/query_engine
needed_by = 8  # medido 2026-11-10 (main-de-sldb-en-verde): GO06 contrato (models/rule_doc.py:62), GD25 vocabulario_visual (models/notation/view_doc_checks.py:61), reglas y vistas_compuestas; antes 4 (GO05)
extractable_today = false
why = """
Unidad propia: 33 archivos, 28 de ellos autónomos. Necesita 7 imports de cuatro
ejes y lo necesitan 20 —casi todos de `op_aristas`—, así que produce mucho más de
lo que consume.

No extraíble hoy por la deuda `axis_boundary_debt`: cinco archivos convierten
entre el formato del índice de aristas y el del motor. Cortar esa conversión
—moviéndola al índice, que ya depende del motor— lo deja sin dependencias.
"""

[[unit]]
id = "adaptadores"
axes = ["adaptadores"]
needs = 6  # medido 2026-11-11 (secrest2): selfdoc rechaza un symlink en knowledge/ por la guarda lectura_de_fuentes; antes 5.
needed_by = 0
extractable_today = true
why = "nadie depende de él; deriva documentos de Python, argparse y click"

[adaptadores_recursion]
answer = "R2 existe acá"
evidence = """
Dos ramas que no comparten código de extracción: 8 archivos `python_*` que leen
el AST de Python, 7 que leen argparse y click. Lo único compartido es
`planned_document`, el contrato de salida, cuya docstring dice: «Declare the
planned-document contract shared by planning, persistence, and inspection. It
does not write files, register models, or decide which documents need saving.»
"""
subunits = [
  { id = "python-ast", files = 8, absorbs = "cambios en el AST de Python" },
  { id = "interfaz", files = 7, absorbs = "cambios en argparse y click" },
]
contract = "planned_document"
why_it_is_recursion = """
Un adaptador nuevo —otro lenguaje— se repara DENTRO de `adaptadores`: implementa
el contrato y nada más cambia. Eso es absorber su propia variedad, que es la
definición de unidad viable.
"""

[[unit]]
id = "recuperacion"
axes = ["recuperacion"]
needs = 4
needed_by = 0
extractable_today = true
why = "nadie depende de él; puerto Embedder sin dependencia vectorial propia"

# No son unidades, y conviene decir por qué:

[[unit]]
id = "notacion"
axes = ["vocabulario_visual", "vistas"]
needs = 4  # medido 2026-11-10 (main-de-sldb-en-verde): GD25 suma vocabulario_visual → grafo (models/notation/view_doc_checks.py:61); antes 3
needed_by = 3  # medido 2026-11-10: GD25 vistas_compuestas → vocabulario_visual; antes 2
indivisible = false
why = """
Lo que spec2viz hacía fuera del repositorio, adentro: el vocabulario (capa 0) y
el resolvedor (capa 3) son una capacidad con una superficie propia (`sldb
notations`, `/notations/*`, `/views/projection*`). Las cuentas las dice la puerta.
"""

[[non_unit]]
id = "operacion"
axes = ["op_almacen", "op_documentos", "op_modelos", "op_aristas", "anclaje", "reglas", "vistas_compuestas"]
needs = 71  # medido 2026-11-11 (secrest2): op_aristas, op_modelos y op_documentos leen y escriben por store/source_guard.py; antes 70. medido 2026-11-11 (secrest, rebasada sobre H9): api/stores y api/documents leen por la guarda lectura_de_fuentes; antes 69. 2026-11-11 (H9): vistas_compuestas → lectura_de_fuentes (api/views/view_source.py); antes 68. 2026-11-11 (seguridad live_stale): aristas nuevas hacia el eje lectura_de_fuentes; antes 66. 2026-11-10 (main-de-sldb-en-verde): 13 aristas de los ejes reglas y vistas_compuestas, y GO07, GD23, GD24, GD26; antes 47/9
needed_by = 11  # medido 2026-11-10: GO05 api/where.py → op_aristas, GD23 → op_modelos; antes 47/9
verdict = "fachada"
why = """
158 archivos, el grupo más grande, y el candidato más obvio por tamaño. Pero
necesita 16 ejes de fuera y solo 6 lo necesitan: es un consumidor neto.

Compone operaciones sobre lo que otras unidades producen y no produce nada que
otras necesiten. Eso es legítimo —es transporte— pero no absorbe su propia
variedad: cualquier cambio en las unidades de abajo la obliga a cambiar.
"""

[[non_unit]]
id = "enlaces"
axes = ["enlaces"]
needs = 4  # medido 2026-11-11 (secrest2): el resolver de enlaces chequea la guarda lectura_de_fuentes antes de resolver, y nombra el objetivo único con errores; antes 2.
needed_by = 0
verdict = "capacidad sin superficie"
why = """
7 archivos que parsean, resuelven y recuperan referencias entre documentos, y
componen un documento a partir de otros. Solo los usa la interfaz.

Lo descarté primero por tamaño y era mal criterio: `compose_document` es una
capacidad real que está construida y no expuesta. No es una sobra, es una
superficie que falta.
"""

# ---------------------------------------------------------------------------
# Lo que falta para que las unidades sean viables
#
# Las cuatro tienen ejecución —es lo que hacen— y les faltan las mismas dos
# funciones, por la misma razón: están organizadas fuera de ellas.
# ---------------------------------------------------------------------------

[[unit_gap]]
function = "auditoria"
missing_in = ["nucleo", "persistencia", "grafo", "adaptadores", "recuperacion"]
evidence = """
`tests/` tiene 3 carpetas para 24 ejes y 26 archivos sueltos en la raíz.
`tests/core/` no existe: el eje `representacion` —la idea central del sistema— no
tiene ninguna prueba que lo ejercite directamente, igual que `bitacora`.
"""
criterion = """
`tests/<unidad>/` corre sola y pasa, sin cargar las otras unidades. Hoy es
imposible: las pruebas no están agrupadas por unidad.
"""

[[unit_gap]]
function = "regulacion"
missing_in = ["nucleo", "persistencia", "grafo", "adaptadores", "recuperacion"]
evidence = """
Las tres reglas mecanizadas viven en `tests/test_clean_code_rules.py` y recorren
`src/` entero: una clase por archivo, diez líneas por función, ochenta por
archivo. Ninguna unidad tiene una regla que le aplique solo a ella.
"""
criterion = "cada unidad declara sus reglas y algo las verifica solo contra ella"

# ---------------------------------------------------------------------------
# Los alfileres
#
# 32 imports de peso 1 o 2 sostienen los dos nudos. Mientras existan, cualquier
# reorganización de carpetas es cosmética: el acoplamiento no está en la
# estructura de directorios.
#
# Precedente medido: en la Fase 0, una arista de peso 1 costaba 46 módulos.
# ---------------------------------------------------------------------------

[pins]
core_knot = 6
operation_knot = 26
note = """
Ignorando las de peso ≤2 el nudo de 11 se parte en 3, el mayor de 4. Ese 4 es la
fusión real; el resto es conveniencia acumulada.
"""

# ---------------------------------------------------------------------------
# Lo que a `persistencia` le falta para absorber su variedad
#
# Hallazgo de propuesta/09-DUDAS-CERRADAS.md: no hay versionado del formato de
# almacenamiento. La migración detecta versiones antiguas POR LA EXISTENCIA DE
# ARCHIVOS:
#
#   # store/migration_legacy_layout.py:37
#   if store_index_path(store_path).exists() or not legacy_store_index_path(...).exists():
#       return False
#
#   «si existe el archivo nuevo, o no existe el viejo, no hay nada que migrar»
#
# Eso funciona y no escala: cada formato nuevo exige una función `legacy_*_path`
# más, y que cada lector tolere ambas formas. Lo tercero escapa de la unidad, y
# ahí es donde las reglas de compatibilidad terminan viviendo en comentarios.
# ---------------------------------------------------------------------------

[persistencia_gap]
missing = "layout_version en el índice de almacén"
detection_today = "por existencia de archivos"
evidence_of_leak = """
«tolerancia a almacenes escritos antes de `field_hashes`: absent is unknown,
never no-fields» — una regla de compatibilidad de formato que vive en dos
comentarios de código, encontrada por los diagnosticadores sin saber qué era.

Con un número de versión sería una condición explícita en un solo lugar.
"""
consequence = """
`persistencia` es una unidad —produce más de lo que consume— pero no absorbe
cambios de formato: se propagan a cada lector. Es la única de las cinco unidades
a la que le falta algo además de auditoría y regulación.
"""

# ---------------------------------------------------------------------------
# Lo que falta como operación, no como diseño
# ---------------------------------------------------------------------------

[[missing_operation]]
id = "lectura-de-indices"
evidence = """
deskops/deskops/operations.py:2801 encadena tres lecturas para recorrer un
almacén: índice de almacén → índice de modelos → índice de documentos. Nadie
debería conocer esa cadena.
"""
asymmetry = """
La escritura SÍ existe como operación: `api/stores/update_store_indexes.py`.
Hay operación para escribir los índices y no para leerlos, y por eso el
consumidor bajó a `store/io`.
"""
repair = "una operación de lectura que oculte la cadena; entonces las tres funciones vuelven a ser internas"

FILE:instruccion
Cold-bundle de la tarea task-run-view-no-compone-en-cada-proceso-el-índice-de-aristas-de-todos-los-stores-enlazados-sldb-views-ru: con el TaskDoc, los rituales enrutados por el Board, las pills ligadas, los átomos ligados y los archivos que el TaskDoc nombra, reformula el encargo, lista ambigüedades con cita textual del input y da el DRY-RUN sin ejecutar nada. No ejecutes nada.

Sección de validación del TaskDoc:
- Benchmark commiteado: sldb views run board y deskops view board en proceso nuevo, con el store construido, menos de 1 s sobre el layout de la reproducción
- En frío (sin caché de disco) no más lento que hoy, con el número en el informe
- Test: el resultado y la revision de la vista salen iguales antes y después con los mismos datos; un store enlazado cambiado se nota en la siguiente corrida
- test_clean_code_rules (obligatorio) y tools/check.sh --fast
- suite completa de sldb de a un archivo desde /dev/shm en verde
- 7 pasos del workflow de sldb en clon limpio

