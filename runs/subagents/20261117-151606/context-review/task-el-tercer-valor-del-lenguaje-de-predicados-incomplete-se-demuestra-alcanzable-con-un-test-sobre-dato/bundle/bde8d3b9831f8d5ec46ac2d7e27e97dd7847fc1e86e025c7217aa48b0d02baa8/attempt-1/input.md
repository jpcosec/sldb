FILE:desk/tasks/task-el-tercer-valor-del-lenguaje-de-predicados-incomplete-se-demuestra-alcanzable-con-un-test-sobre-dato.md
---
sldb:
  by: agent
  at: '2026-11-17T15:13:46Z'
  authority: generated
  via: save_document_payload
id: task-el-tercer-valor-del-lenguaje-de-predicados-incomplete-se-demuestra-alcanzable-con-un-test-sobre-dato
status: draft
summary: ''
tags:
- workspace:desk
- artifact:task
- host:robocop2
current_node: ritual-execution
history: []
references:
- docs/architecture/rules-language.md
depends_on: []
pills: []
files:
- src/sldb/api/where.py
- docs/architecture/rules-language.md
- tests/test_predicates_cli.py
- CHANGELOG.md
- tests/api/test_rules_evaluation.py
task_type: task.code
inherits_from: []
inherit_acceptance_context: false
atoms: []
---

# El tercer valor del lenguaje de predicados (incomplete) se demuestra alcanzable con un test sobre datos reales o se retira

## Rationale

_Explain why this task exists or the business driver behind it._

El lenguaje de predicados tiene tres valores (true, false, incomplete), pero incomplete parece inalcanzable con datos reales: ningún camino de evaluación sobre un store real lo produce. Origen: un análisis de sldb que el supervisor del desk verificó en parte (2026-11-16). Código: src/sldb/api/where.py, src/sldb/store/graph/language/predicate_explain.py, predicate_reach.py y src/sldb/api/rules/.

## Goal

_Describe the concrete result this task must produce._

O hay un test que, con un store real armado en tmp_path, obtiene incomplete de una evaluación pública (where o rules check) y documenta cuándo ocurre; o incomplete se retira del lenguaje, de la API y de la doc sin cambiar los resultados true/false existentes.

## Scope

_State what is in scope and what is out of scope._

Entra: buscar todos los productores y consumidores de incomplete; intentar construir el caso real; decidir con evidencia en result-summary.md; implementar la opción elegida con tests en tests/test_predicates_cli.py o tests/api/test_rules_evaluation.py; actualizar docs/architecture/rules-language.md. CHANGELOG. No entra: otros cambios del lenguaje.

Precisiones (coordinador, bundle-1): dato real = un store armado con la API pública en tmp_path; vale un store enlazado que después se borra o se renombra para que quede no disponible. Primero se intenta demostrar; solo si en result-summary.md queda la evidencia de que ningún camino público lo produce (grep de cada sitio que emite incomplete y por qué no se alcanza), se retira. El retiro abarca GraphBackend.eval, StructuredQuery, el tipo de holds, los tests de especificación que lo nombran y docs/architecture/rules-language.md; si el hash del contrato GO02 de esa doc cambia, se actualiza con el mecanismo que check.sh --fast señala. Línea base: los tests existentes pasan sin cambiar sus valores esperados true/false. tests/api/test_rules_evaluation.py existe y se amplía.

Precisiones (coordinador, bundle-2): si se retira incomplete, toda evaluación que hoy lo devolvería devuelve false, que es lo que ya da hoy cuando compose_edge_index descarta las aristas hacia nodos que no existen (H4). El test de alcance o de retiro va en tests/api/test_rules_evaluation.py, que se agrega a files; tests/test_predicates_cli.py solo se ajusta si nombra incomplete. El índice se compone después de dejar no disponible el store enlazado.

## Implementation Path

_Outline the expected implementation route or affected surface._

1) grep de incomplete en src/sldb. 2) Intentar el caso real. 3) Decidir y documentar la decisión. 4) Implementar y testear. 5) Validation.

## Validation

_List the checks required before this task can close._

- TMPDIR=/dev/shm uv run --frozen --extra code --extra dev pytest -q tests/test_predicates_cli.py
- TMPDIR=/dev/shm uv run --frozen --extra code --extra dev pytest -q tests/api/test_rules_evaluation.py
- TMPDIR=/dev/shm uv run --frozen --extra code --extra dev pytest -q tests/test_clean_code_rules.py
- TMPDIR=/dev/shm uv run --frozen --extra code --extra dev bash tools/check.sh --fast

## Done When

_Name the observable condition that makes the task complete._

Los comandos de Validation pasan; result-summary.md explica la decisión con evidencia; CHANGELOG y commit.

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

FILE:src/sldb/api/where.py
"""The predicate language as a library (GO05): one predicate on a payload, or over a store.

`where_matches` is the language on a plain payload; `where_records` is `sldb find --where`
over search records; `where_findings` evaluates over a store's graph (`GraphBackend.eval`):
paths follow the edge index and payloads come from its projection, nothing is re-extracted.
"""

from __future__ import annotations

from pathlib import Path
from types import SimpleNamespace
from typing import Any

from sldb.api.edges.edge_reading import load_edge_index
from sldb.api.graph.analyze import backend_for
from sldb.api.records.record_filters import RecordFilters
from sldb.api.stores.open_store import open_store
from sldb.store.edge_index.node_ids import bare, kind
from sldb.store.graph.backend.index_view import index_view
from sldb.store.graph.language.predicate_documents import EMPTY_VIEW, document_finding, document_node, has_paths, payload_holds


def where_matches(expression: str, payload: dict[str, Any], subject: dict[str, Any] | None = None) -> bool:
    """Whether a predicate holds on `payload` (the language of `sldb find --where`).

    Args:
        expression: A predicate of `docs/architecture/rules-language.md`: `has(f)`,
            `nonempty(f)`, `"x" in f`, `f ~ "re"`, `f = "s"`, `f >= 3`, `and`/`or`/`not`,
            parentheses...; empty always holds. Paths reach nothing: a payload has no graph.
        payload: The fields the predicate reads; need not belong to a tracked document.
        subject: Fills `{field}` placeholders (default: `payload`). A placeholder the subject
            lacks, or holds as a list or dict, makes the expression not hold.

    Raises:
        WherePredicateError: The expression does not parse.
    """
    return payload_holds(expression, payload, subject)


def where_findings(store: str | Path | None, expression: str, subject: str | None = None, include_linked: bool = False) -> list[dict[str, Any]]:
    """`eval(expression, subject)` over a store: the subject's finding (an export id), or one
    per document of the domain (rules-language.md §6). Each finding has node, holds, clause and
    seen. Reads the edge index and its payload projection; never extracts a document."""
    index = load_edge_index(store, include_linked)
    backend = backend_for(open_store(store, mode="readonly").store_path)
    backend.load(index, {bare(n.id): n.payload for n in index.nodes.values() if kind(n.id) == "document"})
    return backend.eval(expression, subject)


def store_view(store: str | Path | None, include_linked: bool = False) -> dict[str, Any]:
    """The predicate language's graph view of a store's edge index (paths of `--where`)."""
    return index_view(load_edge_index(store, include_linked))


def where_records(records: list, expression: str, store: str | Path | None, pythonpath: str | None = None, include_linked: bool = False) -> tuple[list, list[dict[str, Any]]]:
    """`--where` over `sldb find` records: `(kept, findings)`.

    A document record is evaluated by the language on its payload (plus `sldb`, its
    provenance), with paths over the store's index; it is kept only when `holds` is `true`
    (an `incomplete` does not match). Its finding is in `findings`. Field and section records
    keep their own `--where` reading (`RecordFilters`)."""
    view = store_view(store, include_linked) if has_paths(expression) else EMPTY_VIEW
    found = {id(r): document_finding(expression, _record_node(r), view) for r in records if r.kind == "doc"}
    filters = RecordFilters(pythonpath)
    kept = [r for r in records if (found[id(r)]["holds"] == "true" if r.kind == "doc" else filters.matches(r, expression))]
    return kept, list(found.values())


def _record_node(record: Any) -> dict[str, Any]:
    model_type = record.model_type or type(record.model_name or "Model", (), {})
    doc = SimpleNamespace(payload={**record.payload, "sldb": record.provenance or {}}, name=record.doc_name or record.name, model_type=model_type, model_name=record.model_name)
    prefix = "" if record.store_name in ("local", "", None) else f"{record.store_name}:"
    return document_node(doc, f"{prefix}{record.model_name}:{doc.name}")

FILE:docs/architecture/rules-language.md
# Lenguaje de reglas de sldb

Estado (2026-11-07): contrato de semántica del nodo GO02 del plan
`desk/drawer/plans/grafo-operable`, implementado por GO05; GO10 retiró los lenguajes viejos. Fija la gramática, los caminos,
la semántica trivaluada, el formato de explicación, el hash de contrato y la firma de
evaluación del lenguaje único de predicados de sldb. Los ejemplos de este documento son los
tests de especificación de `tests/test_rules_language_spec.py` (verdes desde GO05); la
implementación, la API y la CLI se describen en la sección 9.

Este documento no describe la API de Python ni la CLI de las reglas (`RuleDoc`,
`rules check`, `rules explain`): eso es GO06. Aquí se fija qué significa un predicado y qué
devuelve evaluarlo. La tabla de equivalencia final conserva los nombres de los dos lenguajes
viejos porque es la tabla histórica que GO10 exime del retiro.

## 1. Gramática (a)

Un predicado es una expresión booleana. Las palabras `and`, `or`, `not`, `in`, `has`,
`nonempty`, `model`, `any`, `all`, `none`, `count` y `rel` son sintaxis del lenguaje; los
nombres de campo y de modelo son los del documento evaluado.

```
expr      := or
or        := and ("or" and)*
and       := not ("and" not)*
not       := "not" not | primary
primary   := "(" expr ")" | atom
atom      := quantifier
           | count_cmp
           | term "in" term
           | term "~" literal
           | term cmp term
           | "has(" campo ")"
           | "nonempty(" campo ")"
           | "model" "<=" nombre_modelo
quantifier:= ("any" | "all" | "none") "(" camino ":" expr ")"
count_cmp := "count(" camino ":" expr ")" cmp term
cmp       := "=" | "!=" | "<" | "<=" | ">" | ">="
term      := campo | literal | lista
lista     := "[" [literal ("," literal)*] "]"
literal   := cadena | número
```

Reglas de forma:

- **Precedencia:** `not` liga más que `and`, y `and` más que `or`. Los operadores binarios
  son asociativos a la izquierda. Los paréntesis agrupan.
- La **conjunción de nivel superior** es la cadena de `and` que queda en la raíz después de
  parsear con esa precedencia. Un `and` dentro de paréntesis, de un `not`, de un `or` o de
  un cuantificador no es de nivel superior.
- Las comparaciones son binarias y no encadenan: `a < b < c` no es una expresión válida.
- `"x" in f` prueba pertenencia si `f` es una lista y subcadena si `f` es un string; para
  cualquier otro tipo es `false`. `f in [ ... ]` prueba pertenencia de un escalar en una
  lista literal.
- `f ~ "patrón"` usa el sabor de expresiones regulares de Python (`re`) y la misma
  semántica de búsqueda que el `~` del `--where` anterior a GO05: `re.search`, no anclaje
  implícito. Un patrón inválido es error de parseo: `WherePredicateError`, la excepción de
  todo parseo del lenguaje (`from sldb.api import WherePredicateError`).
- `model <= X` es verdadero si el modelo del documento es `X` o hereda de `X` por
  `base_models` (la familia de `X`).
- `has(f)` es verdadero si el campo está presente y su valor no es `None` ni la cadena
  vacía. `nonempty(f)` es verdadero si el valor existe y, siendo string, lista, diccionario,
  tupla o conjunto, no está vacío.
- Los literales son cadenas entre comillas dobles (con los escapes de `where_literal`) y
  números. No hay literal de nulo ni de booleano; la ausencia se prueba con `has` y la
  negación.

Ejemplos con el documento `Task:a {note: "x"}` como sujeto:

| Construcción | Predicado | Resultado |
|---|---|---|
| `and` liga más que `or` | `has(status) and status = "open" or has(note)` | `true` |
| `not` liga más que `and` | `not has(status) and has(note)` | `true` |
| paréntesis | `not (has(a) or has(b))` con `Task:b {}` | `true` |
| agrupación a la izquierda | `(has(a) or has(b)) and has(c)` con `Task:c {a: 1, c: 2}` | `true` |
| agrupación a la izquierda | `(has(a) or has(b)) and has(c)` con `Task:d {b: 1}` | `false` |

Comparaciones sobre un documento con `status: "open"`, `priority: 2` (o el valor indicado):

| Construcción | Predicado | Resultado |
|---|---|---|
| igualdad | `status = "open"` | `true` |
| desigualdad | `status != "open"` con `status: "closed"` | `true` |
| menor | `priority < 3` con `priority: 2` | `true` |
| menor o igual | `priority <= 3` con `priority: 3` | `true` |
| mayor | `priority > 3` con `priority: 4` | `true` |
| mayor o igual | `priority >= 3` con `priority: 3` | `true` |

Pertenencia y expresiones regulares:

| Construcción | Predicado | Datos | Resultado |
|---|---|---|---|
| `in` en lista | `"draft" in statuses` | `statuses: ["draft", "open"]` | `true` |
| `in` como subcadena | `"raf" in title` | `title: "draft spec"` | `true` |
| `in` sobre otro tipo | `"x" in priority` | `priority: 5` | `false` |
| escalar en lista literal | `status in ["open", "draft"]` | `status: "draft"` | `true` |
| `~` busca, no ancla | `title ~ "beta"` | `title: "alpha beta"` | `true` |
| regex inválida | `title ~ "("` | — | `WherePredicateError` al parsear |

`model <=`, `has` y `nonempty`:

| Construcción | Predicado | Datos | Resultado |
|---|---|---|---|
| familia de modelo | `model <= BaseDoc` | modelo `ChildDoc`, con `ChildDoc < BaseDoc` | `true` |
| campo presente y no vacío | `has(status)` | `status: "open"` | `true` |
| campo presente pero vacío | `has(status)` | `status: ""` | `false` |
| colección no vacía | `nonempty(tags)` | `tags: ["x"]` | `true` |
| colección vacía | `nonempty(tags)` | `tags: []` | `false` |

## 2. Caminos y cuantificadores (b)

Un **camino** es una secuencia de uno o más pasos. Cada paso se escribe de una de estas
formas:

- `campo` sigue las aristas `references` que ese campo declara. Si el modelo del documento
  actual no declara ese campo como referencia, el conjunto alcanzado es el vacío, no un
  error.
- `rel:<tipo>` sigue las aristas de ese tipo de relación (por ejemplo
  `rel:task_activates`).
- `^campo` es la inversa: los documentos cuyo campo `campo` apunta al documento actual
  (por ejemplo `^subject` son los documentos cuyo `subject` es el actual).

El signo `+` pegado a un paso (`depends_on+`, `rel:tipo+`, `^subject+`) aplica la **clausura
transitiva**: sigue ese paso repetidamente en la misma dirección. El origen queda excluido,
el resultado es un conjunto sin duplicados y la evaluación termina aunque haya ciclos.

Un cuantificador recorre los elementos alcanzados por el camino y evalúa un predicado sobre
cada uno. Los dos puntos separan el camino del predicado: `any(camino: predicado)` es
sintaxis, no una glosa.

- `any(camino: p)` = or del predicado sobre los elementos.
- `all(camino: p)` = and del predicado sobre los elementos.
- `none(camino: p)` = `not any(camino: p)`.

`count(camino: p)` es un entero que solo puede aparecer como un operando de una comparación,
por ejemplo `count(depends_on: status = "open") = 0`.

La sustitución `{campo}` toma el valor del payload del sujeto. Se reconoce únicamente fuera
de literales entre comillas, no admite escapes y usa la sintaxis de `where_subject`. Un
campo ausente o no escalar hace que el predicado no se cumpla.

Ejemplos. La notación `A --depends_on--> B` es una arista `references` del campo
`depends_on`; `A --rel:task_activates--> B` es una arista del tipo de relación indicado.

| Construcción | Predicado | Grafo y datos | Resultado |
|---|---|---|---|
| paso por campo | `any(depends_on: status = "open")` | `A --depends_on--> B`, `B.status: "open"` | `true` |
| cuantificador `all` | `all(depends_on: status = "closed")` | `A --depends_on--> B` y `A --depends_on--> C`, `B.status` y `C.status`: `"closed"` | `true` |
| cuantificador `none` | `none(depends_on: status = "open")` | `A --depends_on--> B` y `A --depends_on--> C`, `B.status` y `C.status`: `"closed"` | `true` |
| campo no declarado como referencia | `any(no_declarado: status = "open")` | `A` sin ese campo de referencia | `false` |
| campo no declarado como referencia | `all(no_declarado: status = "open")` | conjunto vacío | `true` |
| `rel:<tipo>` | `any(rel:task_activates: status = "active")` | `A --rel:task_activates--> B`, `B.status: "active"` | `true` |
| `^campo` | `any(^subject: verdict = "accepted")` | `Review:r --subject--> Task:a`, `r.verdict: "accepted"` | `true` |
| clausura por campo | `all(depends_on+: status = "closed")` | `A --> B --> C`, `B` y `C` con `status: "closed"` | `true` |
| clausura con ciclo | `count(depends_on+: has(status)) = 2` | `A --> B --> C --> A`, con `status` en todos | `true` (termina; origen excluido; sin duplicados) |
| clausura por tipo de relación | `any(rel:task_activates+: status = "done")` | `A --> B --> C`, `C.status: "done"` | `true` |
| clausura inversa | `any(^subject+: verdict = "accepted")` | `Task:a <--subject-- Review:r1 <--subject-- Review:r2`, `r2.verdict: "accepted"` | `true` |
| `count` dentro de comparación | `count(depends_on: status = "open") = 0` | `A --> B`, `B.status: "closed"` | `true` |
| sustitución `{campo}` | `capacity >= {party_size}` | sujeto `{capacity: 6, party_size: 4}` | `true` |
| sustitución con campo ausente | `capacity >= {party_size}` | sujeto `{capacity: 6}` | `false` |
| sustitución con campo no escalar | `capacity >= {party_size}` | sujeto `{capacity: 6, party_size: [4]}` | `false` |
| llaves dentro de un literal | `label = "{party_size}"` | sujeto `{label: "{party_size}", party_size: 4}` | `true` (no se sustituye) |
| referencia a documento inexistente | `count(depends_on: has(status)) = 0` | `A --depends_on--> DocumentoQueNoExiste` | `true` (la referencia se omite) |
| referencia a store enlazado no disponible | `any(rel:external_link: status = "open")` | arista hacia un documento de un store que no se puede abrir | `incomplete` |
| `count` con elemento incomplete | `count(rel:external_link: status = "open") = 0` | igual que la fila anterior | `incomplete` |

## 3. Semántica (c)

Dentro de un store, el lenguaje es bivaluado y de mundo cerrado: lo que no está en el store
no existe. Es un subconjunto de Datalog estratificado, sin funciones salvo las comparaciones
y con negación solo estratificada. El evaluador no inventa hechos ni persiste resultados.

Hay dos ausencias que no se confunden:

- **Documento inexistente dentro de un store disponible:** la referencia no produce
  elemento. El documento se omite del conjunto alcanzado por el camino. Por eso `all` sobre
  el conjunto vacío es `true`, `any` es `false` y `count` vale `0`.
- **Referencia que cae en un store enlazado que no se puede abrir al evaluar:** el elemento
  no se conoce. El resultado es `incomplete`, no `false`.

`incomplete` se combina con la lógica trivaluada de Kleene fuerte. Los valores son `true`
(T), `false` (F) e `incomplete` (I).

| `p` | `q` | `p and q` | `p or q` |
|---|---|---|---|
| T | T | T | T |
| T | F | F | T |
| T | I | I | T |
| F | T | F | T |
| F | F | F | F |
| F | I | F | I |
| I | T | I | T |
| I | F | F | I |
| I | I | I | I |

| `p` | `not p` |
|---|---|
| T | F |
| F | T |
| I | I |

Los cuantificadores son generalizaciones de `or` y `and`. Las columnas son excluyentes:
«algún I, sin T» significa elementos I y F, sin ningún T; «algún I, sin F» significa
elementos I y T, sin ningún F; «algún I con T y F» significa que hay de los tres valores; «todos I» significa que todos los elementos alcanzados son I.

| Forma | Conjunto vacío | Todos T | Todos F | Mezcla de T y F | Todos I | Algún I, sin T | Algún I, sin F | Algún I con T y F |
|---|---|---|---|---|---|---|---|---|
| `any(c: p)` | F | T | F | T | I | I | T | T |
| `all(c: p)` | T | T | F | F | I | F | I | F |
| `none(c: p)` = `not any(c: p)` | T | F | T | F | I | I | F | F |

La comparación con `count` también es trivaluada:

| Elementos alcanzados por el camino | `count(c: p)` | `count(c: p) cmp n` |
|---|---|---|
| Ningún elemento I | entero `k`: número de elementos con `p = T` | T si `k cmp n`; F si no |
| Algún elemento I | I | I |

Cualquier comparación u operador con un operando `incomplete` es
`incomplete`, y un predicado evaluado sobre un elemento `incomplete` es `incomplete`.

Una regla de severidad `error` cuyo resultado es `incomplete` falla con explicación
`"incomplete"`; una regla `alert` lo reporta como alerta.

## 4. Formato de explicación (d)

La evaluación produce findings con cuatro claves:

- `node`: el documento evaluado (su `Model:name`).
- `holds`: `true`, `false` o `incomplete`.
- `clause`: la cláusula textual que decidió el resultado.
- `seen`: mapa `campo → valor leído` de las hojas de esa cláusula.

Ejemplo de una hoja falsa sobre `Task:a {status: "closed"}` evaluando
`status = "open"`:

```json
{
  "node": "TaskDoc:a",
  "holds": "false",
  "clause": "status = \"open\"",
  "seen": {"status": "closed"}
}
```

Regla de `seen` (p4):

- En un `and`, las hojas de la primera rama falsa.
- En un `or`, las hojas de la primera rama verdadera.
- En un `not`, la hoja negada.
- En un cuantificador, las hojas del elemento testigo: el primero que falsa un `all` o el
  primero que cumple un `any` (para `none`, el primero que cumple su `any` interno).

Una hoja `incomplete` aporta el valor `{"incomplete": "<referencia no resuelta>"}`. El
finding (`node`, `holds`, `clause`, `seen`) viaja en el envelope de la CLI. El comando
concreto y la clave exacta del envelope son de GO06 (hipótesis H10), no de este contrato.

## 5. Hash de contrato (e)

Un modelo declara el subconjunto de campos que forman su contrato con el atributo de clase
`__contract__`, una lista de nombres.

- `__contract__` **ausente** (el atributo no está definido): todos los campos del payload del
  documento sujeto.
- `__contract__ = []` (definido y vacío): error al cargar el modelo.
- Un campo listado que falta en el payload aporta la línea `<campo>=` con hash vacío.

El hash de contrato es el `sha256` hexadecimal de las líneas `"<campo>=<field_hash>"`,
ordenadas por los **bytes UTF-8 del nombre del campo**, unidas por `\n` y sin salto final,
codificadas en UTF-8. `field_hash` es el hash de ese campo ya guardado en
`DocumentEntry.field_hashes`.

Por ejemplo, con el contrato `["title", "goal"]` y los hashes `title=t` y `goal=g`, el texto
canónico es:

```
goal=g
title=t
```

y su `sha256` es el hash de contrato. Si `goal` falta del payload, el texto canónico es:

```
goal=
title=t
```

## 6. Firma de evaluación (f)

GO03 implementa y GO05 completa:

```
eval(predicado_parseado, sujeto_opcional) -> lista de findings
```

Cada finding tiene `node`, `holds`, `clause` y `seen`, como en la sección 4.

- **Con sujeto:** un único finding, el de ese sujeto.
- **Sin sujeto:** un finding por cada documento del dominio. El dominio son todos los
  documentos del store, salvo que el predicado sea una conjunción de nivel superior que
  contenga `model <= X`; en ese caso el dominio son los documentos de la familia de `X`.
  Un `model <= X` anidado bajo `not`, `or`, un cuantificador o un camino no restringe el
  dominio.
- Dos `model <=` en la conjunción de nivel superior restringen el dominio a la
  **intersección** de sus familias (p5).
- Una referencia a un documento inexistente se omite del conjunto alcanzado por un camino
  (sección 3): `all` sobre vacío es `true`, `any` es `false` y `count` es `0`.
- Una referencia a un store enlazado no disponible produce `incomplete` en la hoja y se
  propaga con Kleene.

## 7. Tabla de equivalencia

La tabla de abajo es histórica: relaciona cada operador de los dos lenguajes que GO10
retiró con su construcción en el lenguaje de este documento (columna «Construcción nueva»).
Ninguna de esas construcciones reutiliza como nombre de operador los de la columna «Operador
viejo» de las filas 12 a 19.

### Histórico: equivalencia de los lenguajes retirados

| # | Operador viejo | Origen | Construcción nueva | Nota |
|---|---|---|---|---|
| 1 | `has(f)` | `where_parse` | `has(f)` | presente y no `None`/`""` |
| 2 | `nonempty(f)` | `where_parse` | `nonempty(f)` | rechaza colecciones vacías |
| 3 | `"x" in f` | `where_parse` | `"x" in f` | lista: pertenencia; string: subcadena |
| 4 | `f ~ "pat"` | `where_parse` | `f ~ "pat"` | `re.search`; inválida = `WherePredicateError` |
| 5 | `model <= X` | `where_parse` | `model <= X` | familia por `base_models` |
| 6 | `f = v` | `where_parse` | `f = v` | comparación |
| 7 | `f != v` | `where_parse` | `f != v` | comparación |
| 8 | — | nuevo | `f < v` | no existía en `where_parse` |
| 9 | `f <= v` | `where_parse` | `f <= v` | comparación |
| 10 | — | nuevo | `f > v` | no existía en `where_parse` |
| 11 | `f >= v` | `where_parse` | `f >= v` | comparación |
| 12 | `eq` | `FieldCondition` | `f = v` | mismo valor esperado |
| 13 | `ne` | `FieldCondition` | `f != v` | mismo valor esperado |
| 14 | `gt` | `FieldCondition` | `f > v` | mismo valor esperado |
| 15 | `lt` | `FieldCondition` | `f < v` | mismo valor esperado |
| 16 | `contains` | `FieldCondition` | `"x" in f` | en el viejo, solo listas; en el nuevo, también subcadena |
| 17 | `starts_with` | `FieldCondition` | `f ~ "^x"` | escapar los metacaracteres de `x` |
| 18 | `is_null` | `FieldCondition` | `not has(f)` | aproximación: `has` también rechaza `""` |
| 19 | `is_not_null` | `FieldCondition` | `has(f)` | aproximación: `has` también rechaza `""` |

Las filas 18 y 19 son la equivalencia fijada por el contrato; `has` no distingue `None` de
`""`, así que para datos donde esa diferencia importe hay que consultar el valor y no usar
solo la presencia.

## 8. Hipótesis

Lo que el contrato de GO02 no fija y este documento resuelve de forma provisional. GO05
puede ajustarlo sin cambiar la semántica de las secciones anteriores.

- **H1. Nombres de la API de spec.** Los tests de especificación llaman a un módulo
  `sldb.store.query_engine.rules` con `parse_predicate(texto)`, `eval_predicate(ast, grafo,
  sujeto=None)` y `contract_hash(modelo, field_hashes)`. El contrato fija `eval(predicado
  parseado, sujeto opcional)`, no la ruta del módulo ni la forma de pasar el grafo.
- **H2. Grafo de los tests.** Los tests representan el store como un diccionario
  `{"nodes": {id: {"model": ..., "payload": ..., "base_models"?: [...]}}, "edges": [{"source",
  "type", "target", "field"?, "unavailable"?}]}`. La familia de `model <= X` sale de
  `base_models` del nodo (GO05 p9). El objeto real es el índice compuesto / `GraphBackend`
  de GO03: allí la familia sale de `base_models` de los nodos de modelo, transitivamente.
- **H3. Sujeto de `eval`.** Los tests pasan como sujeto el identificador `Model:name` del
  nodo. GO03 admite además el payload y el `export_id` con proyección.
- **H4. `incomplete` por store no disponible.** Los tests marcan la arista con
  `"unavailable": True`; en el índice real la marca es `metadata.unavailable` de la arista.
  Hoy `compose_edge_index` descarta las aristas hacia nodos que no existen, así que una
  referencia a un store enlazado que no se pudo abrir se lee como documento inexistente
  hasta que el índice la marque.
- **H5. Separación de pasos.** El contrato no fija cómo se concatenan varios pasos de un
  camino. Se propone `.` (`depends_on.rel:tipo`), sin afectar los ejemplos de un solo paso.
- **H6. `^` sobre relaciones.** Se interpreta que `^` también invierte un paso `rel:<tipo>`,
  aunque los ejemplos fijados usan `^campo`.
- **H7. Literales.** Los literales escalares son cadenas entre comillas dobles y números; no
  hay sintaxis de `true`, `false` ni `null`. Las listas literales son de escalares, sin
  anidamiento.
- **H8. Mayúsculas y espacios.** Las palabras clave son minúsculas y sensibles a mayúsculas;
  el espacio en blanco entre tokens no es significativo.
- **H9. Campos anidados.** El contrato no fija campos con punto. Se conserva la resolución
  por ruta de `where_lookup` para un paso de campo: `tasks.0.title`, o la autoridad del
  bloque de procedencia `sldb` de un documento (`--where 'sldb.authority = "source_raw"'`,
  una ruta de campo y no un módulo de Python).
- **H10. Clave del envelope.** El contrato fija que la explicación viaja en el envelope,
  pero no el nombre exacto de la clave; GO06 lo fija al definir `rules explain`.
- **H11. Error por `__contract__` vacío.** Los tests esperan `ValueError`; el contrato solo
  dice «error al cargar el modelo».
- **H12. Separador y `rel` en caminos (GO05).** Un nombre con puntos dentro de un camino son
  varios pasos de campo (`depends_on.subject`); `rel:<tipo>` puede ir en cualquier posición
  (`depends_on.rel:task_activates`). Un campo de referencia llamado `rel` seguido de `:` se
  lee como paso de relación. `^` invierte solo el primer paso del grupo; `+` aplica al último.
- **H13. `doc ~ "re"`.** Como el `~` del `--where` anterior a GO05, `doc ~` lee el nombre del documento
  (no un campo `doc`).
- **H14. Ausencia en comparaciones.** Un campo ausente no cumple ninguna comparación, `in`
  ni `~`, con literal de cadena o de número. El `--where` anterior a GO05 dejaba cumplir `f != <número>`
  sobre un campo ausente y levantaba `TypeError` al ordenar `None` o tipos mezclados; el
  lenguaje devuelve `false` (tabla de equivalencia, golden de la fila 7).
- **H15. Sustitución.** `{campo}` lee el valor de primer nivel del sujeto, también dentro de un
  cuantificador; si alguno falta o no es escalar (cadena o número, no booleano), el predicado
  entero es `false` con `clause` = el predicado y `seen` = los valores leídos.
- **H16. Cláusula de `not` y de los cuantificadores.** `clause` es el texto del `not` o del
  cuantificador; `seen` sigue la sección 4. Un `any` falso, un `all` verdadero y un `count`
  no tienen testigo: `seen` es `{}`.

## 9. Implementación (GO05)

- **Lenguaje:** `src/sldb/store/graph/language/`: tokens, parser (`parse_predicate(texto) ->
  Predicate`, el tipo público parseado: `text` y `root`), átomos y términos, caminos
  (`predicate_paths`, `predicate_reach`), evaluador con Kleene fuerte (`predicate_eval`,
  `predicate_explain`) y la vista mínima de grafo (`predicate_view`: por nodo `model`,
  `base_models`, `payload`; aristas salientes y entrantes con `field`, `type` y
  `unavailable`). `sldb.store.query_engine.rules` es la fachada de los tests de spec
  (`parse_predicate`, `eval_predicate`, `contract_hash`).
- **API única:** `GraphBackend.eval` (sobre la vista del índice compuesto,
  `backend/index_view.py`), `sldb.api.where.where_matches` (un payload suelto),
  `sldb.api.where.where_findings` (un store, sin re-extraer: lee la proyección del índice),
  `sldb.api.where.where_records` (`sldb find --where`), `edges_holding` (la condición de cada
  arista) y `StructuredQuery` (cada `FacetFilter` lleva un `where`: un predicado sin caminos
  sobre los campos de su facet).
- **CLI:** `sldb find ... --where <expr>` usa el lenguaje: un documento cumple solo si `holds`
  es `true`; un camino recorre el índice del store. `--explain` agrega a `data` la clave
  `findings`, un finding por documento evaluado (cumpla o no). Los registros de campo y de
  sección conservan su lectura propia de `--where`. `sldb graph query` lee filtros
  `{"facet": ..., "where": "<predicado>"}`; un camino en ese `where` es
  `SLDBGraphArgumentError` y un JSON con la clave anterior `conditions` es rechazado al
  validar (`ValidationError`).
- **Retiro (GO10):** los shims que GO05 dejó para los dos lenguajes viejos ya no existen;
  la API única es `where_matches` (y las demás de arriba) con la gramática de este documento.
  `WherePredicateError` vive en `sldb.core.exceptions` y se importa como
  `from sldb.api import WherePredicateError`.
- **Equivalencia:** `tests/fixtures/where_goldens/` guarda el resultado de cada fila de la
  sección 7 con el código anterior a GO05; la expresión vieja queda como dato y
  `tests/store/test_predicate_language.py` evalúa la construcción nueva y compara.
  Diferencias declaradas: fila 7 con número sobre campo ausente (H14), fila 16 (`in` también
  es subcadena), filas 18 y 19 (`has` rechaza `""`).

FILE:tests/test_predicates_cli.py
import json

import yaml

from sldb.cli import main as cli_main
from sldb.store.io import load_store_index


def test_store_init_seeds_editable_predicates(tmp_path, capsys):
    assert cli_main(["stores", "init", "--path", str(tmp_path)]) == 0
    capsys.readouterr()

    store = tmp_path / ".sldb"
    index = load_store_index(store)
    assert {item.name for item in index.predicates} >= {"implements", "grounded_by"}

    assert (
        cli_main(
            [
                "predicates",
                "show",
                "implements",
                "--store",
                str(store),
                "--format",
                "json",
            ]
        )
        == 0
    )
    payload = json.loads(capsys.readouterr().out)
    assert payload["name"] == "implements"
    assert payload["axis"] == "HOW"


def test_predicates_add_list_validate_and_remove(tmp_path, capsys):
    assert cli_main(["stores", "init", "--path", str(tmp_path)]) == 0
    store = tmp_path / ".sldb"
    capsys.readouterr()

    assert (
        cli_main(
            [
                "predicates",
                "add",
                "depends_on",
                "--axis",
                "dependency",
                "--description",
                "Declares a dependency.",
                "--store",
                str(store),
            ]
        )
        == 0
    )
    capsys.readouterr()

    assert (
        cli_main(["predicates", "list", "--store", str(store), "--format", "json"]) == 0
    )
    listed = json.loads(capsys.readouterr().out)
    custom = next(item for item in listed["predicates"] if item["name"] == "depends_on")
    assert custom == {
        "name": "depends_on",
        "axis": "DEPENDENCY",
        "description": "Declares a dependency.",
    }

    assert cli_main(["predicates", "validate", "--store", str(store)]) == 0
    assert "PASS" in capsys.readouterr().out

    assert cli_main(["predicates", "remove", "depends_on", "--store", str(store)]) == 0
    capsys.readouterr()
    assert all(item.name != "depends_on" for item in load_store_index(store).predicates)


def test_predicates_validate_reports_duplicate_yaml_entries(tmp_path, capsys):
    assert cli_main(["stores", "init", "--path", str(tmp_path)]) == 0
    store = tmp_path / ".sldb"
    index_file = store / "core" / "store_index.yaml"
    payload = yaml.safe_load(index_file.read_text(encoding="utf-8"))
    payload["predicates"].append(dict(payload["predicates"][0]))
    index_file.write_text(yaml.safe_dump(payload, sort_keys=False), encoding="utf-8")
    capsys.readouterr()

    assert (
        cli_main(["predicates", "validate", "--store", str(store), "--format", "json"])
        == 1
    )
    result = json.loads(capsys.readouterr().out)
    assert result["valid"] is False
    assert any("Duplicate predicate" in error for error in result["errors"])


def test_docs_recover_uses_custom_store_predicate(tmp_path, capsys):
    assert cli_main(["stores", "init", "--path", str(tmp_path)]) == 0
    store = tmp_path / ".sldb"
    assert (
        cli_main(
            [
                "predicates",
                "add",
                "depends_on",
                "--axis",
                "DEPENDENCY",
                "--store",
                str(store),
            ]
        )
        == 0
    )
    target = tmp_path / "target.md"
    target.write_text("# Target\n", encoding="utf-8")
    source = tmp_path / "source.md"
    source.write_text("[depends_on:: [[target.md]]]", encoding="utf-8")
    capsys.readouterr()

    assert (
        cli_main(
            ["docs", "recover", str(source), "--store", str(store), "--format", "json"]
        )
        == 0
    )
    result = json.loads(capsys.readouterr().out)
    assert result["links"][0]["predicate"] == "depends_on"
    assert result["links"][0]["w5h1_type"] == "DEPENDENCY"

FILE:tests/api/test_rules_evaluation.py
"""GO08: the rules evaluated when they are due (docs/architecture/rules.md §9).

`on_write` refuses a write on an error (nothing persisted, the explanation in the envelope) and
lets an alert pass (persisted, in `warnings`); `on_transition` keeps the edges of
`edges_holding` with their alerts and moves an edge an error blocks to `edges_blocked`;
`stores check` reports the `on_check` rules and the document anchors, exit 1 only on an error;
the `on_check` cache recomputes nothing when nothing changed, a whole family when its rule
changes, and gives the same findings without `.sldb_cache`; a closure terminates on a cycle;
`edges check` fails on a condition that does not parse.
"""

from __future__ import annotations

import importlib
import json
import shutil
import sys
from pathlib import Path

import pytest

from sldb import api
from sldb.cli import main
from sldb.core.exceptions import SLDBRuleViolationError
from sldb.store.layout import cache_dir

on_check_module = importlib.import_module("sldb.api.rules.rules_on_check")
MODULE = "sldb_go08_rule_models"
MODELS = '''from pydantic import Field
from sldb import StructuredNLDoc


class X(StructuredNLDoc):
    __references__ = ["depends_on"]
    __template__ = "---\\nstatus: ⸢rev•status⸥\\ndepends_on: ⸢rev•depends_on⸥\\n---\\n\\n# ⸢rev•title⸥"
    title: str = Field(description="Title.")
    status: str = Field(default="", description="Status.")
    depends_on: str = Field(default="", description="Referenced document.")


class Sub(X):
    pass


class State(StructuredNLDoc):
    __template__ = "# ⸢rev•title⸥"
    title: str = Field(description="Title.")
'''
RULE = {"title": "closed", "subject": "model <= X", "condition": 'status = "closed"', "severity": "error", "moment": "on_check"}


class World:
    def __init__(self, base: Path) -> None:
        self.root, self.py = base / "world", str(base)
        self.root.mkdir()
        self.store = api.init_store(self.root).store_path
        for ref in (f"{MODULE}:X", f"{MODULE}:Sub", f"{MODULE}:State", "sldb.models.rule_doc:RuleDoc"):
            api.add_model(self.store, ref, self.py)
        api.init_relations(self.store, self.py)
        for name in ("x1", "x2"):
            self.doc("X", name, {"title": name, "status": "open"})

    def doc(self, model: str, name: str, payload: dict) -> None:
        api.create_document(self.store, model, self.root / f"{name}.md", payload, name, self.py)

    def rule(self, name: str, **fields) -> None:
        api.create_document(self.store, "RuleDoc", self.root / "rules" / f"{name}.md", {**RULE, "title": name, **fields}, name, self.py)

    def save(self, model: str, name: str, payload: dict) -> None:
        api.save_document_payload(self.store, model, name, payload, self.py)

    def envelope(self, capsys, *argv: str, pythonpath: bool = True) -> dict:
        main(["--envelope", *argv, "--store", str(self.store)] + (["--pythonpath", self.py] if pythonpath else []))
        return json.loads(capsys.readouterr().out)


@pytest.fixture
def world(tmp_path: Path):
    (tmp_path / f"{MODULE}.py").write_text(MODELS, encoding="utf-8")
    sys.path.insert(0, str(tmp_path))
    try:
        yield World(tmp_path)
    finally:
        sys.path.remove(str(tmp_path))
        sys.modules.pop(MODULE, None)


@pytest.fixture
def recomputed(monkeypatch) -> list[str]:
    """Every recalculation (p8): one call of `recompute` per rule-document pair."""
    calls: list[str] = []
    real = on_check_module.recompute

    def counted(graph, rule, node):
        calls.append(f"{rule['name']}@{node}")
        return real(graph, rule, node)

    monkeypatch.setattr(on_check_module, "recompute", counted)
    return calls


def _codes(findings) -> list[tuple[str, str, str]]:
    return [(f.level, f.code, f.subject) for f in findings]


def test_an_error_rule_refuses_the_write_and_nothing_is_persisted(world: World, capsys) -> None:
    world.rule("closed", moment="on_write")
    before = (world.root / "x1.md").read_text(encoding="utf-8")
    with pytest.raises(SLDBRuleViolationError) as refused:
        world.save("X", "x1", {"title": "x1", "status": "review"})
    assert str(refused.value) == 'rules/closed: status = "closed" (seen: {"status":"review"})'
    assert (world.root / "x1.md").read_text(encoding="utf-8") == before
    assert api.edge_node(world.store, "X:x1").payload["status"] == "open"
    envelope = world.envelope(capsys, "fields", "update", "docs/X/x1/status", "review")
    assert (envelope["ok"], envelope["exit"], envelope["error"]["type"]) == (False, 1, "rules/violation")
    assert 'rules/closed: status = "closed" (seen: {"status":"review"})' in envelope["error"]["message"]
    assert (world.root / "x1.md").read_text(encoding="utf-8") == before


def test_two_error_rules_are_both_in_the_envelope_ordered_by_rule(world: World, capsys) -> None:
    world.rule("b-titled", moment="on_write", condition='title = "other"')
    world.rule("a-closed", moment="on_write")
    envelope = world.envelope(capsys, "fields", "update", "docs/X/x1/status", "review")
    lines = envelope["error"]["message"].splitlines()
    assert [line.split(":", 1)[0] for line in lines] == ["rules/a-closed", "rules/b-titled"]
    assert envelope["error"]["type"] == "rules/violation"


def test_an_alert_rule_lets_the_write_pass_and_reports_it_in_warnings(world: World, capsys) -> None:
    world.rule("closed", moment="on_write", severity="alert")
    envelope = world.envelope(capsys, "fields", "update", "docs/X/x1/status", "review")
    assert (envelope["ok"], [w["code"] for w in envelope["warnings"]]) == (True, ["rules/closed"])
    assert envelope["warnings"][0]["subject"] == "X:x1" and "review" in envelope["warnings"][0]["what"]
    assert api.edge_node(world.store, "X:x1").payload["status"] == "review"


def test_a_document_not_yet_indexed_is_refused_by_a_rule_on_its_base_family(world: World) -> None:
    from sldb.store.layout import edges_shard_path

    world.rule("closed", moment="on_write")
    world.doc("Sub", "s1", {"title": "s1", "status": "closed"})
    edges_shard_path(world.store, "Sub", "s1").unlink()
    assert api.edge_node(world.store, "Sub:s1") is None
    before = (world.root / "s1.md").read_text(encoding="utf-8")
    with pytest.raises(SLDBRuleViolationError, match="rules/closed"):
        world.save("Sub", "s1", {"title": "s1", "status": "open"})
    assert (world.root / "s1.md").read_text(encoding="utf-8") == before


def test_a_store_without_on_write_rules_writes_as_before(world: World) -> None:
    world.rule("closed")
    world.save("X", "x1", {"title": "x1", "status": "review"})
    assert api.edge_node(world.store, "X:x1").payload["status"] == "review"


def _machine(world: World) -> None:
    for state in ("open", "done"):
        world.doc("State", state, {"title": state})
    world.doc("RelationTypeDoc", "rt-moves", {"title": "moves", "name": "moves_to", "source_types": ["State"], "target_types": ["State"], "description": "A transition."})
    payload = {"title": "finish", "source_id": "State:open", "target_id": "State:done", "relation_type": "moves_to", "attributes": {"sets": {"status": "done"}}}
    world.doc("RelationDoc", "e-finish", payload)


def test_edges_holding_carries_the_alerts_and_an_error_moves_the_edge_to_edges_blocked(world: World) -> None:
    _machine(world)
    subject = {"title": "x1", "status": "open"}
    world.rule("titled", moment="on_transition", severity="alert", condition='title = "x9"')
    [edge] = api.edges_holding(world.store, "State:open", subject, "moves_to", document="X:x1")
    assert edge.effects == {"sets": {"status": "done"}, "terminal": False}
    assert _codes(edge.findings) == [("alert", "rules/titled", "X:x1")]
    assert api.edges_blocked(world.store, "State:open", subject, "moves_to", document="X:x1") == []
    world.rule("closed", moment="on_transition")
    assert api.edges_holding(world.store, "State:open", subject, "moves_to", document="X:x1") == []
    [blocked] = api.edges_blocked(world.store, "State:open", subject, "moves_to", document="X:x1")
    assert blocked.target == "sldb://document/State:done" and blocked.effects == edge.effects
    assert _codes(blocked.findings) == [("error", "rules/closed", "X:x1"), ("alert", "rules/titled", "X:x1")]
    assert "findings" not in api.edges_holding(world.store, "State:open", subject, "moves_to")[0].model_dump()


def test_stores_check_reports_on_check_rules_and_doc_anchors_and_fails_only_on_error(world: World, capsys, monkeypatch) -> None:
    from sldb.core.finding import alert

    anchor = alert("anchors/doc_changed", "X:x2", "subject: doc:X:x1 is changed")
    monkeypatch.setattr(on_check_module, "check_doc_anchors", lambda store, pythonpath=None: [anchor])
    world.rule("closed", severity="alert")
    envelope = world.envelope(capsys, "stores", "check", "--format", "json")
    assert (envelope["ok"], sorted(w["code"] for w in envelope["warnings"])) == (True, ["anchors/doc_changed", "rules/closed", "rules/closed"])
    world.rule("titled", condition='title = "x1"')
    envelope = world.envelope(capsys, "stores", "check", "--format", "json")
    assert (envelope["ok"], envelope["exit"]) == (False, 1)
    assert [(e["code"], e["subject"]) for e in envelope["data"]["errors"]] == [("rules/titled", "X:x2")]


def test_a_second_check_recomputes_nothing_and_a_changed_rule_recomputes_its_family(world: World, recomputed: list[str]) -> None:
    world.rule("closed")
    first = _codes(api.rules_on_check(world.store))
    assert first == [("error", "rules/closed", "X:x1"), ("error", "rules/closed", "X:x2")] and len(recomputed) == 2
    recomputed.clear()
    assert _codes(api.rules_on_check(world.store)) == first and recomputed == []
    world.save("RuleDoc", "closed", {**RULE, "condition": 'status = "open"'})
    assert api.rules_on_check(world.store) == [] and sorted(recomputed) == ["closed@X:x1", "closed@X:x2"]


def test_a_write_dirties_the_document_and_its_neighbours_only(world: World, recomputed: list[str]) -> None:
    world.doc("X", "x3", {"title": "x3", "status": "open"})
    world.rule("closed")
    api.rules_on_check(world.store)
    recomputed.clear()
    world.save("X", "x1", {"title": "x1", "status": "closed", "depends_on": "X:x2"})
    dirty = json.loads((cache_dir(world.store) / "rules" / "dirty.json").read_text(encoding="utf-8"))["dirty"]
    assert dirty == ["X:x1"]
    assert _codes(api.rules_on_check(world.store)) == [("error", "rules/closed", "X:x2"), ("error", "rules/closed", "X:x3")]
    assert sorted(recomputed) == ["closed@X:x1", "closed@X:x2"]


def test_without_the_cache_the_findings_are_the_same(world: World, recomputed: list[str]) -> None:
    world.rule("closed")
    first = _codes(api.rules_on_check(world.store))
    shutil.rmtree(cache_dir(world.store) / "rules")
    recomputed.clear()
    assert _codes(api.rules_on_check(world.store)) == first == _codes(api.rules_check(world.store))
    assert len(recomputed) == 2


def test_a_closure_over_a_cycle_terminates_and_names_the_open_document(world: World) -> None:
    for name, target in (("a", "b"), ("b", "c"), ("c", "a")):
        world.doc("X", name, {"title": name, "status": "closed", "depends_on": f"X:{target}"})
    api.rebuild_edges(world.store, world.py)
    world.save("X", "c", {"title": "c", "status": "open", "depends_on": "X:a"})
    world.rule("deps", where='title = "a"', condition='all(depends_on+: status = "closed")')
    [found] = api.rules_on_check(world.store)
    assert (found.code, found.subject) == ("rules/deps", "X:a") and found.what.endswith("(witness: X:c {\"status\":\"open\"})")
    world.save("X", "c", {"title": "c", "status": "closed", "depends_on": "X:a"})
    assert api.rules_on_check(world.store) == []


def test_edges_check_fails_on_a_condition_that_does_not_parse(world: World, capsys) -> None:
    _machine(world)
    assert api.check_edges(world.store).ok
    payload = {"title": "bad", "source_id": "State:done", "target_id": "State:open", "relation_type": "moves_to", "condition": 'status = = "x"'}
    world.doc("RelationDoc", "e-bad", payload)
    [error] = api.check_edges(world.store).errors
    assert "State:done -[moves_to]-> sldb://document/State:open: condition does not parse" in error
    envelope = world.envelope(capsys, "edges", "check", pythonpath=False)
    assert (envelope["ok"], envelope["exit"]) == (False, 1)

FILE:instruccion
Cold-bundle de la tarea task-el-tercer-valor-del-lenguaje-de-predicados-incomplete-se-demuestra-alcanzable-con-un-test-sobre-dato: con el TaskDoc, los rituales enrutados por el Board, las pills ligadas, los átomos ligados y los archivos que el TaskDoc nombra, reformula el encargo, lista ambigüedades con cita textual del input y da el DRY-RUN sin ejecutar nada. No ejecutes nada.

Sección de validación del TaskDoc:
- TMPDIR=/dev/shm uv run --frozen --extra code --extra dev pytest -q tests/test_predicates_cli.py
- TMPDIR=/dev/shm uv run --frozen --extra code --extra dev pytest -q tests/api/test_rules_evaluation.py
- TMPDIR=/dev/shm uv run --frozen --extra code --extra dev pytest -q tests/test_clean_code_rules.py
- TMPDIR=/dev/shm uv run --frozen --extra code --extra dev bash tools/check.sh --fast

