FILE:desk/tasks/task-sldb-create-document-y-track-document-file-evalúan-las-reglas-on-write-h4-declare-write-conserva-la.md
---
sldb:
  by: agent
  at: '2026-11-12T02:26:13Z'
  authority: generated
  via: create_document
id: task-sldb-create-document-y-track-document-file-evalúan-las-reglas-on-write-h4-declare-write-conserva-la
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
- src/sldb/api/documents/
- src/sldb/api/rules/
- src/sldb/api/tags/
- src/sldb/api/stores/
- src/sldb/cli/commands/
- tests/
- docs/architecture/rules.md
- docs/architecture/tags.md
- CHANGELOG.md
- contracts/layers.toml
task_type: task.code
inherits_from: []
inherit_acceptance_context: false
atoms: []
from_drawer: desk/drawer/tasks/task-on-write-no-se-eval-a-en-create-document-ni-en-track-document-file.md
---

# sldb: create_document y track_document_file evalúan las reglas on_write (H4), declare --write conserva la declaración de tags (H5), la familia de tags da su evaluación estructurada (H6) y se documenta qué documentos ve (H7)

## Rationale

_Explain why this task exists or the business driver behind it._

Hipótesis H4-H7 de CC35d resto de deskops (notas de inbox de sldb, la de H4 del puente q18 y la de H5-H7) y seguimiento de GD27. Hoy un documento nuevo entra por create_document o track_document_file sin pasar por las reglas on_write ni por la familia builtin:tag_namespace, y deskops mantiene un puente que repite esa validación; regenerar store.yaml con stores declare --write borra la declaración de tags; y deskops tiene que leer la evaluación de la familia parseando el texto de un hallazgo.

## Goal

_Describe the concrete result this task must produce._

create_document y track_document_file evalúan on_write como save (H4); stores declare --write conserva tag_namespaces y tag_models (H5); un hallazgo de la familia de tags lleva su evaluación estructurada y rules check, rules explain y tags check la exponen en su salida JSON (H6); la guía de reglas y de tags dice qué documentos ve la familia (H7).

## Scope

_State what is in scope and what is out of scope._

En alcance: la evaluación on_write en la creación y el tracking de documentos, la declaración conservada, el dato estructurado de los hallazgos de la familia de tags y su salida JSON, docs, tests y CHANGELOG. Fuera: borrar el puente de deskops (es otra tarea de deskops que corre cuando esta entre), que stores build evalúe on_write, y cambiar qué reglas existen.

## Implementation Path

_Outline the expected implementation route or affected surface._

Origen: ítem de drawer del seguimiento de GD27 (on_write no se evalúa en create_document ni en track_document_file), nota de inbox de H4 (q18) y nota de H5-H7 de CC35d resto.

ESTADO ACTUAL: check_on_write (rules_on_write.py) solo se llama desde save_document_payload, vía check_rules_on_write de payload_save_steps.py. create_document y track_document_file no lo llaman. declare_store (stores declare --write) conserva solo generate y derived de la declaración vigente. Un hallazgo de la familia de tags lleva su evaluación como texto, con el formato cláusula y entre paréntesis seen y un JSON.

CAMBIO (q1-q5), en este orden:
q1 (H5): declare_store conserva tag_namespaces y tag_models de la declaración vigente, igual que generate y derived. El worker revisa si StoreDeclaration tiene otra clave autorada que declare --write pierda, y la suma si la hay (lo dice en el informe). Test: una declaración con tags regenerada por stores declare --write queda igual.
q2 (H4), decisión del coordinador, revisable: create_document y track_document_file evalúan las reglas on_write, las de usuario y la familia builtin:tag_namespace, con el mismo criterio que save: una violación lanza SLDBRuleViolationError y no se escribe ni se trackea nada. apply_batch, /save con create y track, transaction.create y transaction.track y scaffold_store lo heredan. stores build (el tracking en lote de apply_includes) NO evalúa on_write: es declarativo y stores check ya lo cubre con on_check (revisable; el worker lo deja dicho en la guía de reglas). Cambio de contrato de las reglas de usuario: sección de on_write de docs/architecture/rules.md.
q3 (H6): el hallazgo de la familia de tags lleva su evaluación estructurada (namespace, tags, lo que falta) como dato propio, el mismo que hoy va dentro del texto, y rules check, rules explain y tags check lo exponen en su salida JSON. El texto del hallazgo no cambia. Test que lo lee sin parsear texto.
q4 (H7): la guía de reglas y la de tags dicen que la familia solo ve documentos indexados: un documento escrito a mano no tiene hallazgos hasta que se trackea, y uno editado se evalúa sobre su proyección indexada. Sin cambio de código.
q5: tests de q2: crear y trackear un documento que viola una regla on_write se rechaza sin escribir nada; uno que no la viola pasa; apply_batch y transaction.create heredan el rechazo y la transacción restaura el árbol; stores build sigue sin evaluar. tests/test_clean_code_rules.py es obligatorio (80 líneas efectivas por archivo, 10 de lógica por función, sin subir límites; un archivo nuevo fuera de una carpeta con eje necesita eje en contracts/layers.toml, y los grados medidos salen de tools/check.sh --fast). Docs y CHANGELOG.

VALIDACIÓN: el worker corre de a uno los tests que toca; antes de entregar, la suite completa de sldb de a un archivo desde /dev/shm, test_clean_code_rules y tools/check.sh --fast. Los 7 pasos del workflow de sldb los corre el coordinador.

## Validation

_List the checks required before this task can close._

- Tests de H4: crear y trackear un documento que viola una regla on_write se rechaza sin escribir; apply_batch y transaction.create heredan el rechazo y restauran el árbol; stores build sigue sin evaluar
- Test de H5: stores declare --write sobre una declaración con tag_namespaces y tag_models la deja igual
- Test de H6: la evaluación estructurada de un hallazgo de la familia sale en la salida JSON de rules check y de tags check, sin parsear texto
- test_clean_code_rules (obligatorio) y tools/check.sh --fast
- suite completa de sldb de a un archivo desde /dev/shm en verde
- 7 pasos del workflow de sldb en clon limpio

## Done When

_Name the observable condition that makes the task complete._

q1-q5 hechos, tests verdes y la suite completa en verde; docs y CHANGELOG actualizados; las notas de H4 y de H5-H7 y el ítem de drawer de origen se dan de baja por CLI al cierre.

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

FILE:docs/architecture/rules.md
# Reglas de sldb: RuleDoc, `rules check` y `rules explain`

Estado (2026-11-06): contrato e implementación de los nodos GO06 (§1-§8) y GO08 (§9-§10) del
plan `desk/drawer/plans/grafo-operable`. sldb evalúa reglas declaradas; los consumidores las
escriben como documentos. El lenguaje de predicados es el de
[`rules-language.md`](rules-language.md) y la evaluación entra por la costura
[`GraphBackend.eval`](graph-backend.md). Las anclas `doc:` son las de
[`anchoring.md`](anchoring.md) §6 (GO07) y las transiciones las de [`edges.md`](edges.md)
(GO09). Fuera: el retiro de los shims (GO10).

## 1. El documento `RuleDoc`

`sldb.models.rule_doc.RuleDoc` es un modelo builtin. Se registra como cualquier modelo
(`sldb models add sldb.models.rule_doc:RuleDoc`) y una regla se escribe y se registra como
cualquier documento (`sldb docs create RuleDoc ...` o `sldb.api.create_document`).

| Campo | Tipo | Significado |
|---|---|---|
| `title` | texto | El título (H1). |
| `subject` | texto | La familia de la regla: `model <= X`, o una conjunción de nivel superior de términos `model <= X` (la intersección de sus familias, `rules-language.md` §6). |
| `where` | texto, opcional | Predicado que se evalúa sobre cada miembro de la familia antes de la condición. `false` o `incomplete` = la regla no aplica a ese documento. |
| `condition` | texto | El predicado que debe cumplir cada documento al que la regla aplica. |
| `severity` | `error` \| `alert` | El nivel del finding cuando la condición da `false`. |
| `moment` | `on_write` \| `on_transition` \| `on_check` | Cuándo se evalúa (§9). `rules check` sin `--subject` corre solo `on_check`. |
| `message` | texto, opcional | Texto con el que empieza `Finding.what`. |

La familia de `model <= X` sale de la herencia de modelos que sldb ya conoce: `base_models`
de los nodos de modelo del índice, transitivamente (la misma que usan `source_types` y
`target_types` de `RelationTypeDoc`).

El hash de una regla es el `content_hash` de su documento; GO08 lo incluye en la clave de su
caché derivada. Nada del resultado de una regla se persiste.

## 2. Validación al escribir

Las invariantes de un documento son del modelo; las que dependen del store, de la escritura.

- **Validadores de `RuleDoc`** (pydantic): `condition` parsea; `where`, si no está vacío,
  parsea; `subject` parsea y es exactamente `model <= X` o una conjunción de nivel superior de
  esos términos (una comparación, un camino, un `or` o un `not` se rechazan: los filtros van en
  `where`); `severity` y `moment` son `Literal`. Construir o escribir una RuleDoc mal formada
  levanta el `ValidationError` del modelo con el campo y el motivo, y no se escribe nada.
- **Contra el store** (`sldb.api.rules.refuse_unknown_family`): cada `X` de `subject` debe
  ser un modelo registrado. Si no, la escritura se rechaza con el error existente de sldb para
  modelo desconocido, `SLDBStoreError: Model 'X' not registered.`. Lo comprueban
  `create_document`, `save_document_payload` y `sldb docs update`, después de validar el
  payload y antes de escribir.

## 3. Qué reglas hay y a qué documentos aplican

- Las reglas son las `RuleDoc` (o documentos de un submodelo de `RuleDoc`) del **store
  local**, leídas de la proyección del índice de aristas (`graph-backend.md`, GO04): no se
  re-extrae ningún documento.
- Una regla **aplica** a un documento si el `subject` da `true` sobre él (el documento está en
  la familia) y, si hay `where`, el `where` da `true`.
- El grafo sobre el que se evalúa es el índice compuesto con sus stores enlazados, de modo que
  los caminos cruzan links y un documento de un store enlazado se puede evaluar.

## 4. `sldb rules check [--subject DOC]`

```
sldb rules check [--subject DOC] [--store S] [--pythonpath P] [--format text|json|yaml]
```

- **Con `--subject`:** evalúa sobre ese documento todas las reglas que le aplican, de
  cualquier momento. `DOC` es `Model:name`, `store:Model:name` (un store enlazado) o una ruta
  (relativa a la raíz del proyecto o absoluta; también `name`, `Model/name` y `alias:ruta`).
- **Sin `--subject`:** evalúa las reglas `on_check` sobre cada documento **local** al que
  aplican (los stores enlazados no se recorren).
- Solo los resultados `false` e `incomplete` se convierten en `Finding` de
  `sldb.core.finding`, que sale por el canal de siempre (`sldb.cli.alert_sink`):

| Campo de `Finding` | Valor |
|---|---|
| `level` | La severidad de la regla si la condición da `false`; `alert` si da `incomplete`, sea cual sea la severidad. |
| `code` | `rules/<nombre>` si `false`; `rules/<nombre>/incomplete` si `incomplete`. `<nombre>` es el nombre del documento RuleDoc. |
| `subject` | El nodo evaluado: el `Model:name` del documento (`store:Model:name` si es de un store enlazado). |
| `what` | `<clause> (seen: <seen>)`, con `seen` en JSON compacto (claves ordenadas, `ensure_ascii=False`). Con `message`: `<message> \| <clause> (seen: <seen>)`. Si la cláusula que decidió es un cuantificador de nivel superior con testigo, sigue ` (witness: <Model:name> <seen del testigo>)` (§9.5). |
| `fix` | `""`: la regla no prescribe remedio. |
| `document` | La ruta del documento relativa a la raíz de su proyecto, como la guarda el registro. |

El nodo viaja en `subject` y la cláusula en `what`; `Finding` no gana campos.

- **Exit:** 1 si hay al menos un finding `error`; 0 en otro caso (los alerts nunca fallan).
- **Salida:** en texto, una línea por finding y el recuento. Con `--format json`,
  `{"findings": [<Finding.as_dict()>...]}`. Con `sldb --envelope rules check --format json`,
  `data` es ese objeto, los alerts van además en `warnings` y un exit 1 es
  `error.type = "rules/failed"`.

## 5. `sldb rules explain RULE SUBJECT`

```
sldb rules explain RULE SUBJECT [--store S] [--pythonpath P] [--format text|json|yaml]
```

`RULE` es `RuleDoc:<nombre>`, `<nombre>` o la ruta de la regla; `SUBJECT`, como `DOC` en
`rules check`. Imprime el finding de eval tal como lo devuelve `GraphBackend.eval`, también
cuando se cumple. Con `--format json` (y por tanto en `data` del envelope):

```json
{"rule": "RuleDoc:needs-owner", "subject": "TaskDoc:task-a",
 "finding": {"node": "TaskDoc:task-a", "holds": "false", "clause": "has(owner)", "seen": {"owner": ""}}}
```

La clave `finding` cierra la hipótesis H10 de `rules-language.md` para `rules explain`.

Cuando la regla no aplica al sujeto, no hay finding de eval, solo el motivo:

```json
{"rule": "RuleDoc:needs-owner", "subject": "TaskDoc:task-a", "applies": false,
 "reason": "where", "detail": "status = \"open\""}
```

`reason` es `subject` si el documento no está en la familia (`detail` = el `subject` de la
regla) o `where` si el `where` dio `false` o `incomplete` (`detail` = la `clause` del `where`
que lo decidió).

| `holds` | exit |
|---|---|
| `true` | 0 |
| `false` | 1 |
| `incomplete` | 2 |
| la regla no aplica | 3 |

La severidad no afecta el exit de `explain`.

## 6. Referencias que no resuelven

Una regla o un documento que no resuelve es el error existente de documento desconocido:
`SLDBDocumentTargetError: Unknown document target: <ref>`, que en el envelope es
el tipo `docs/missing` <!-- gone --> con exit 1 (un tipo de error, no una ruta).

## 7. API

`sldb.api.rules` (también en `sldb.api`):

- `rules_check(store, subject=None, pythonpath=None) -> list[Finding]`
- `rules_explain(store, rule, subject, pythonpath=None) -> dict` y `explain_exit(answer) -> int`
- `refuse_unknown_family(store_path, model_type, payload, pythonpath=None)`
- GO08 (§9): `rules_on_check(store) -> list[Finding]`, `on_check_findings(store, pythonpath=None)`
  y `transition_findings(store, document, subject, pythonpath=None)`; en `sldb.api`, además,
  `edges_blocked`.

Piezas: `rule_graph.py` (el índice cargado una vez en el backend del store y qué documentos
son locales), `rule_subjects.py` (qué reglas hay, a qué aplican y cómo se resuelven las
referencias), `rules_check.py`, `rules_explain.py` y `rule_writes.py`; de GO08,
`rules_on_write.py`, `rules_on_transition.py`, `rules_on_check.py`, `rule_cache.py`,
`dirty_set.py` y `fixpoint.py`.

## 8. Hipótesis

- **R1. Payload de evaluación.** La condición se evalúa sobre la proyección del índice
  (`graph-backend.md`, GO04): un campo que no se proyecta (un diccionario, una tabla) no se
  ve desde una regla.
- **R2. Arista `models → store`.** Los validadores de `RuleDoc` importan el parser del
  lenguaje, que vive en el almacén, de forma diferida; `contracts/layers.toml` la cuenta como
  la reparación pendiente R6 (bajar el parser a la capa 0).
- **R3. `sldb docs track`.** Registrar un archivo RuleDoc ya escrito valida el modelo al
  extraerlo, pero no comprueba que los modelos de `subject` estén registrados; una regla así
  no aplica a ningún documento.
- **R4. Formato.** `rules check` y `rules explain` imprimen texto por defecto, como el resto
  de la CLI; el JSON del envelope pide `--format json`.

## 9. Evaluación en su momento (GO08)

Los findings son los de §4 (`rule_finding`): mismo `level`, `code`, `subject`, `what`,
`document`. Todo finding sale por `sldb.cli.alert_sink`: los alerts en `warnings` del envelope,
los errores en `error`/`errors`. Una regla aplica como en §3.

### 9.1 `on_write`

Un paso propio de `save_document_payload` (`payload_save_steps.check_rules_on_write`),
inmediatamente después del pinneado de anclas (GO07) y antes de renderizar y escribir:

- La regla lee el payload **ya pinneado**, con `<campo>__anchor_state` de cada campo
  `__doc_anchors__` calculado como lo compondría el índice. El documento conserva su modelo y sus
  aristas del índice **anterior** a la escritura (H-GO08-3).
- Reglas: las `on_write` del store, en orden de export id (`RuleDoc:<nombre>`).
- Al menos un finding `error`: `SLDBRuleViolationError` (`sldb.core.exceptions`), con los errores
  en `findings` y un `message` de una línea por error, `<code>: <what>`. Nada se escribe. En el
  envelope es `error.type = "rules/violation"`, exit 1.
- Los alerts salen siempre (pase o no la escritura) por `sldb.core.finding_route.route`; la CLI
  instala `alert_sink` como oyente al arrancar (`warnings` del envelope y una línea por alert en
  stderr). Un programa que use la API sin instalar oyente no los recibe (H-GO08-2).
- Un store que no registra `RuleDoc` (ni un modelo construido sobre él) no lee ninguna regla:
  la escritura se comporta exactamente como antes.

### 9.2 `on_transition`

`edges_holding(store, node, subject, relation=None, include_linked=True, exclude_tags=(), document=None)`
y la nueva `edges_blocked` con la misma firma. `document` es la referencia del documento que
transiciona (`Model:name`, `store:Model:name` o ruta); las reglas `on_transition` que le aplican
se evalúan sobre `subject`, el mismo payload que leen las condiciones (los extremos de la arista
son estados, no sujetos).

- Sin error: `edges_holding` devuelve las aristas que se cumplen, cada `EdgeRecord` con `effects`
  (GO09, intacto) y `findings` (lista de `Finding`, solo alerts; `[]` si no hay).
  `edges_blocked` devuelve `[]`.
- Con un error: ninguna arista se cumple (`edges_holding` = `[]`) y `edges_blocked` devuelve las
  que se habrían cumplido, cada una con `findings` = todos los findings (errores y alerts).
- Las reglas son del sujeto, no de la arista: los mismos findings valen para toda arista que
  sale de `node` (H-GO08-4).
- Sin `document` no corre ninguna regla y `findings` queda `None`: como `effects`, no aparece en
  ningún dump mientras no tiene valor. `sldb edges show NODE --holds-for DOC` pasa `DOC` como
  `document`.

### 9.3 `on_check`

`sldb stores check` (y `check_store`, `GET /stores/check`) agrega a sus findings, a su propio
nivel y después de los del diagnóstico, los de `on_check_findings`: las reglas `on_check` de
`rules_on_check` y los alerts de `check_doc_anchors` (GO07). Exit 1 solo si hay un error; los
alerts salen en `alerts` del JSON y en `warnings` del envelope.

### 9.4 Caché derivada y dirty set

En `<.sldb_cache>/rules/` del store (`layout.cache_dir`), JSON, leída y escrita bajo el bloqueo
de store existente (`store_lock`, en espera):

- Un archivo por regla, `<content_hash de la RuleDoc>.json`: `results` (export id → finding como
  `Finding.as_dict()`, o `null` si se cumple o no aplica) y `stamps` (de qué se calculó cada
  resultado). La familia es `subject` sin aplicar `where`. Cambiar la regla cambia su hash: la
  familia entera se recalcula; los archivos de hashes que ya no existen se borran.
- `dirty.json`: el dirty set. Escribir un documento D (`on_write`, con RuleDoc en el store) agrega
  D y todo documento con una arista entrante o saliente hacia D en el índice. `rules_on_check`
  recalcula los documentos sucios y lo vacía al terminar.
- Una regla **ancha** (una clausura `+`, un camino de más de un paso o un cuantificador anidado)
  recalcula su familia entera si el dirty set no está vacío.
- Cuenta como sucio (se recalcula): un documento sin entrada, uno cuyo stamp cambió (el
  documento y sus vecinos a un salto, o el store entero para una regla ancha: `source_hash` y
  payload compuesto, anclas incluidas) y todo, si `dirty.json` falta, es ilegible o de otra
  versión. Así una escritura que no pasa por `save_document_payload` (un `create`, un `delete`,
  un archivo editado y reconstruido) no deja un resultado viejo (H-GO08-5).
- La caché nunca es autoridad: borrarla da los mismos findings. Un recálculo es una llamada a
  `rules_on_check.recompute` por par regla-documento; `check_doc_anchors` no se cachea.

### 9.5 Punto fijo y testigo

Los únicos hechos derivados son los conjuntos de una clausura `+`. El evaluador de GO05 ya los
calcula semi-naive (`predicate_reach._closure`: cada ronda expande solo los elementos nuevos; uno
ya visto no se vuelve a expandir), así que termina con ciclos; viven en memoria y nunca se
persisten. GO08 lo reutiliza (`fixpoint.py`).

Como `seen` del lenguaje no nombra elementos (rules-language.md §4, H16), el `what` de un
finding decidido por un cuantificador de nivel superior agrega el **testigo**:
` (witness: <Model:name> <su seen>)`, el primer elemento alcanzado que falsea un `all`, cumple
el `any` interno de un `none` o, en un `any` falso, el primero alcanzado (todos lo falsean);
en un `incomplete`, el primero incompleto. Sin elementos no hay testigo.

### 9.6 `sldb edges check`

Además de lo existente, falla (exit 1) si la condición de una arista (la suya o la heredada de su
tipo) no parsea: `edge <origen> -[<tipo>]-> <destino>: condition does not parse: <motivo>`.

## 10. Ejemplo end-to-end

`tests/api/test_rules_end_to_end.py`. Un store temporal con:

- `Task` (`__contract__ = ["title", "goal"]`), `Review` (`__doc_anchors__ = ["subject"]`,
  campo `verdict`) y `State`; dos estados `State:doing` y `State:done` y un `RelationDoc`
  `moves_to` entre ellos sin condición.
- La regla:

```yaml
title: reviewed
subject: model <= Task
condition: any(^subject: anchor_state = "intact" and verdict = "accepted")
severity: error
moment: on_transition
```

1. **Task sin Review.** `edges_holding(store, "State:doing", task, "moves_to", document="Task:t")`
   es `[]`; `edges_blocked(...)` devuelve la arista con el finding
   `rules/reviewed`, cuyo `what` empieza por `any(^subject: ...)` (sin testigo: nada alcanzado).
2. **Review accepted con `subject: doc:Task:t`.** Al guardarla se pinnea
   (`doc:Task:t@sha256:...`); la arista está en `edges_holding`, con `findings = []`.
3. **Editar `goal` de la Task.** El ancla queda `changed`; la arista vuelve a `edges_blocked` y el
   `what` termina en `(witness: Review:r {"anchor_state":"changed"})`. `sldb stores check`
   reporta además el alert `anchors/doc_changed` de `Review:r` y sale 0.

## 11. Hipótesis de GO08

- **H-GO08-1. Testigo.** Nombrar el elemento (aceptación: "falla nombrando C"; "explicación
  anchor_state = changed") no cabe en `seen` sin cambiar el lenguaje (GO05); va al final de
  `what`, también en `rules check`.
- **H-GO08-2. Canal de los alerts de `on_write`.** La API no importa la CLI: los alerts viajan
  por `sldb.core.finding_route`, donde `sldb.cli.main` instala `alert_sink`.
- **H-GO08-3. Aristas en `on_write`.** La regla ve el payload nuevo pero las aristas del índice
  anterior; una referencia agregada en la misma escritura se ve en la siguiente evaluación.
- **H-GO08-4. Sujeto de `on_transition`.** Un payload suelto no dice qué documento es: el
  parámetro `document` lo nombra. Sin él no corre ninguna regla.
- **H-GO08-5. Stamps.** Además del dirty set del contrato, cada resultado guarda un stamp; un
  cambio que no pasó por una escritura con reglas también recalcula.
- **H-GO08-6. Solo `save_document_payload`.** `create_document`, `docs track` y el borrado no
  corren `on_write` ni marcan el dirty set (los stamps cubren su efecto en `on_check`).

FILE:docs/architecture/tags.md
# Tag namespaces: declared in `store.yaml`, checked as a rule family, read as a tree

Node GD27 of the plan `generalizar-desde-deskops`. A document's tags (`tags` or
`semantic_tags`) may carry a namespace: `area:a.b` belongs to `area`, the text before the
first colon; what follows is the value (it may hold colons). A tag without a colon belongs to
no namespace and is never checked. The store declares its namespaces in `.sldb/store.yaml`,
beside `models` and `include`:

```yaml
tag_namespaces:
- name: area                 # what precedes the first colon
  hierarchical: true         # a.b.c is a path: a, a.b and a.b.c are tags too (default)
  folder_axis: true          # declarative: the value is the document's folder (tag_folder)
  anchored_by:               # optional: every required tag must be the `tag` of an Anchor
    model: Anchor
    field: tag
- name: kind
  hierarchical: false        # the value is one piece: no prefixes
- name: domain
  anchored_by:
    model: CrossroadDoc
    field: path
    value: bare              # the field holds `a.b`, the value without `domain:` (default: tag)
tag_models: [AtomDoc]        # optional: the family checks only these models and their descendants
```

`sldb.api.TagNamespace` (`src/sldb/api/stores/tag_namespace.py`) is one entry; its invariants
are its validators: a name without colon or blanks, `anchored_by` exactly `{model, field}`
plus an optional `value` (`tag` or `bare`), no other key; `StoreDeclaration.tag_namespaces` refuses a repeated name. A declaration without
the key reads and writes as before it existed. `sldb tags namespaces` lists what is declared.

### `anchored_by.value` (GD27 for deskops, CC35d H1)

`value: tag` (the default, and what a declaration without the key means) reads the anchor's
`field` as a complete tag: `area:a.b` anchors `area:a.b`, a value of another namespace anchors
nothing. `value: bare` reads it as the value without the namespace: a `CrossroadDoc.path` of
`a.b` anchors `domain:a.b`; a field that already carries `domain:` (or is blank, or is not text)
anchors nothing. `TagNamespace.anchor_tag(field_value)` is that decision; the tags the
namespace requires, `missing` and the tree are always complete tags.

### `tag_models` (GD27 for deskops, CC35d H2)

`StoreDeclaration.tag_models` (a list of model names, empty by default and then not dumped)
limits the family to the documents whose model is listed or has a listed one among its
`base_models`. The tags of other documents are not checked: neither `on_write`, `on_check`,
`rules check` nor `tags check` report them, and `rules explain` of the family on such a
document holds with `clause: model in tag_models` and `seen: {model, tag_models}`. The
anchors are never filtered: any local document of the `anchored_by` model anchors. In
`tag_tree`, a tag is used (and so orphan, or what places an anchor) only through documents in
scope; roots and anchors are as without it. It is store-wide, not per namespace, because the
case it solves is an undeclared namespace, which has no entry to say "does not apply". Model
names are not checked against the registered ones (a misspelt one leaves the scope empty).

## What the family checks

The checks are the built-in rule family `builtin:tag_namespace:<name>`
(`src/sldb/api/rules/builtin_tag_rules.py`), one rule per namespace a document names, not a
RuleDoc of the user (q3: the rules language has no anchor predicate). On a document, the rule
of namespace `<name>` holds when:

1. `<name>` is declared (`clause: namespace declared`; `seen: {namespace, tags, declared}`);
2. with `anchored_by`, every tag the namespace **requires** for each of its values is the
   `field` of a local document of `model` (`clause: each prefix anchored by Model.field`;
   `seen: {namespace, tags, missing}`, `missing` top-down, once each). A hierarchical
   namespace requires every prefix of the value, the whole value included (`area:a.b.c`
   requires `area:a`, `area:a.b` and `area:a.b.c`); a non-hierarchical one requires the value
   alone. The document being written counts as an anchor of the tag it carries in that field.

Without `anchored_by`, declaring the namespace is all a tag needs. Every finding is an
`error` with code `rules/builtin:tag_namespace:<name>`, the subject is the document's export
id and `what` is `<clause> (seen: <seen>)`, the form of a RuleDoc's finding (rules.md §4).

The family runs where the RuleDocs run (rules.md §9), also in a store that registers no
`RuleDoc` but declares `tag_namespaces`:

| Moment | Where | Effect |
|---|---|---|
| `on_write` | `save_document_payload` (so `fields update`, `docs update`, `transaction.update`, `apply_batch`, `POST /save`) and `replace_text` | an error is `SLDBRuleViolationError` (`rules/violation`, exit 1) and nothing is written |
| `on_check` | `stores check`, `on_check_findings` | the findings follow the `on_check` RuleDocs' (not cached) |
| `rules check [--subject]` | `rules_check` | the findings follow the RuleDocs', on the same documents |
| `rules explain builtin:tag_namespace:<name> DOC` | `rules_explain` | `{"rule", "subject", "finding": {node, holds, clause, seen}}`, also when it holds; without `tag_namespaces` the rule is an unknown target |
| `tags check` | `tag_check` | the same evaluation as `rules check` filtered to the family; exit 1 on an error |

`create_document` and `track_document_file` evaluate no `on_write` rule (a GO08 gap, q18):
a document created without its anchor is reported by `tags check`, `rules check` and
`stores check`.

## `tag_tree`, `tag_folder`

`sldb.api.tag_tree(store, namespace)` (`sldb tags tree NAMESPACE --format json` emits the same
object, in the envelope's `data`):

```json
{"namespace": "area",
 "roots": [{"tag": "area:a", "document": "Anchor:a",
            "children": [{"tag": "area:a.b", "document": "Anchor:ab", "children": []}]}],
 "orphans": [{"tag": "area:c", "used_by": ["Note:n2"]}],
 "unplaced": [{"tag": "area:a.x", "document": "Anchor:ax"}]}
```

- Everything is limited to the namespace asked; tags are complete (`area:a.b`); each level
  is alphabetical by tag; an undeclared namespace is `SLDBStoreError`.
- With `anchored_by`, `roots` is the anchors' tree: every prefix of an anchored value is a
  node, `document` its anchor's export id or `null` for a prefix without one; `orphans` are
  the tags local documents use that no anchor declares (`used_by`: their export ids);
  `unplaced` are the anchors no local document uses, directly or, when hierarchical, through
  a tag under them (an anchor of `area:a` is placed by a document tagged `area:a.b`).
- Without `anchored_by`, `roots` nests the tags local documents use (`document: null`) and
  both lists are empty. A non-hierarchical namespace has roots without children.

`sldb.api.tag_folder(tag)` is a pure function of the text: `a.b` or `area:a.b` -> `a/b`, one
segment per part (`a` -> `a`); it never reads the store (`folder_axis` is the declaration that
tells a consumer to use it). A blank value, an empty segment (`a..b`, `.a`, `a.`) or a slash
inside a segment is a `ValueError` naming the value. It stays strict on purpose (CC35d H3):
a consumer that derives folders from a `folder_axis` namespace keeps those tags out of its own
documents (deskops forbids them in its atom pattern) instead of having them silently skipped.

## API and CLI

- `sldb.api.tag_namespaces(store) -> list[dict]`, `tag_tree(store, namespace) -> dict`,
  `tag_folder(tag) -> str`, `tag_check(store) -> list[Finding]` (also in `sldb.api.tags`);
  `sldb.api.TagNamespace`.
- `sldb.api` re-exports `sldb.api.semantic`: `add_semantic_parent`, `remove_semantic_parent`,
  `add_semantic_equivalence`, `semantic_tag`.
- `sldb tags namespaces | tree NAMESPACE | check` (`--store`, `--pythonpath`, `--format`,
  with envelope). `tags check` prints as `rules check` does (`{"findings": [...]}` in JSON).
- Helpers of the store layer (`src/sldb/store/semantic_tags.py`): `payload_tags`,
  `split_namespace`, `namespaced_tags`, `tag_prefixes`.

## Hypotheses

- The anchors are read from the local store only (linked stores do not anchor).
- `anchors_of` reads every local document per evaluation: a sweep over a store of N
  documents is O(N²) dictionary reads. Enough for the stores seen so far; a cache keyed by the
  rule graph is the next step if it is not.
- `tags check` and `stores check` recompute the family every time (no `.sldb_cache/rules`
  entry): the family has no `content_hash` to key it by.

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
Cold-bundle de la tarea task-sldb-create-document-y-track-document-file-evalúan-las-reglas-on-write-h4-declare-write-conserva-la: con el TaskDoc, los rituales enrutados por el Board, las pills ligadas, los átomos ligados y los archivos que el TaskDoc nombra, reformula el encargo, lista ambigüedades con cita textual del input y da el DRY-RUN sin ejecutar nada. No ejecutes nada.

Sección de validación del TaskDoc:
- Tests de H4: crear y trackear un documento que viola una regla on_write se rechaza sin escribir; apply_batch y transaction.create heredan el rechazo y restauran el árbol; stores build sigue sin evaluar
- Test de H5: stores declare --write sobre una declaración con tag_namespaces y tag_models la deja igual
- Test de H6: la evaluación estructurada de un hallazgo de la familia sale en la salida JSON de rules check y de tags check, sin parsear texto
- test_clean_code_rules (obligatorio) y tools/check.sh --fast
- suite completa de sldb de a un archivo desde /dev/shm en verde
- 7 pasos del workflow de sldb en clon limpio

