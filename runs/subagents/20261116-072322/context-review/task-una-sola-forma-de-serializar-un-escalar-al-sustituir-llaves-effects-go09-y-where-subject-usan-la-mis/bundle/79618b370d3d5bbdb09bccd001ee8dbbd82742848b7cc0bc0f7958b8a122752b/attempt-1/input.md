FILE:desk/tasks/task-una-sola-forma-de-serializar-un-escalar-al-sustituir-llaves-effects-go09-y-where-subject-usan-la-mis.md
---
sldb:
  by: agent
  at: '2026-11-16T06:15:09Z'
  authority: generated
  via: save_document_payload
id: task-una-sola-forma-de-serializar-un-escalar-al-sustituir-llaves-effects-go09-y-where-subject-usan-la-mis
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
- src/sldb/store/query_engine/where_literal.py
- src/sldb/store/query_engine/where_subject.py
- src/sldb/api/edges/edge_effects.py
- tests/store/test_predicate_language.py
- tests/api/test_edge_effects.py
- CHANGELOG.md
task_type: task.refactor
inherits_from: []
inherit_acceptance_context: false
atoms:
- atom-sldb-evaluates-declared-rules-consumers-author-them
from_drawer: desk/drawer/tasks/task-dos-formas-de-serializar-un-escalar-al-sustituir-llaves-effects-de-go09-y-where-subject.md
---

# Una sola forma de serializar un escalar al sustituir llaves: effects (GO09) y where_subject usan la misma función

## Rationale

_Explain why this task exists or the business driver behind it._

La sustitución {campo} tiene dos serializadores: src/sldb/api/edges/edge_effects.py:38-44 (_written) usa yaml.safe_dump (1e20 da 1.0e+20, booleanos true/false, y hoy una fecha lanza LookupError), mientras src/sldb/store/query_engine/where_literal.py:47-51 (scalar_literal, usado por fill_braces de src/sldb/store/query_engine/where_subject.py:19) usa Decimal sin exponente y devuelve None para booleanos. El mismo valor sale distinto según dónde se sustituya. Hallazgo de GO09 (H3, H4). Origen: drawer desk/drawer/tasks/task-dos-formas-de-serializar-un-escalar-al-sustituir-llaves-effects-de-go09-y-where-subject.md.

## Goal

_Describe the concrete result this task must produce._

Existe una función brace_text(value) -> str en src/sldb/store/query_engine/where_literal.py que usan tanto edge_effects._written como fill_braces, con estas salidas exactas: int y Decimal sin exponente (1e20 -> 100000000000000000000), float con repr más corto sin exponente cuando sea posible (0.5 -> 0.5), bool -> true/false, datetime.date -> ISO 8601 (2026-11-16), str tal cual; cualquier otro tipo lanza TypeError con el tipo.

## Scope

_State what is in scope and what is out of scope._

Entra: escribir brace_text, cambiar _written y scalar_literal/fill_braces para usarla, y tests parametrizados con los cinco casos de Goal en tests/store/test_predicate_language.py y tests/api/test_edge_effects.py (mismo valor, mismo texto por los dos caminos). Si un test existente esperaba 1.0e+20 o None para bool, se actualiza al formato nuevo y el commit lo dice. CHANGELOG.md. No entra: cambiar la gramática del lenguaje de reglas ni los literales que el parser acepta.

Precisiones (preflight-1): orden de despacho: bool antes que int; datetime.datetime -> isoformat() completo antes que date; date -> isoformat(); int -> str(int); Decimal -> format(d, "f") (fraccionarios, negativos y ceros finales tal cual los da "f"; NaN e Infinity lanzan ValueError con el valor); float -> repr(f) si no contiene "e", y si contiene "e" -> format(Decimal(repr(f)), "f"); str -> tal cual. Mensaje de TypeError: "cannot write {type(value).__name__} into braces". scalar_literal se queda y llama a brace_text para los escalares (sigue devolviendo None para los tipos que hoy no maneja, salvo bool, que ahora da true/false).

Convenciones (valen para todo el contrato): la entrada de CHANGELOG.md es una línea en español bajo el encabezado "## 0.1.13 — not released yet", con el estilo de las entradas vecinas. El commit lo hace el coordinador con deskops closeout commit (mensaje "<título corto de la tarea>"); el ejecutor no hace push. El informe del ejecutor es runs/subagents/<run-dir>/result-summary.md y ahí va todo lo que el contrato manda "anotar en el informe". Los números de línea citados son orientativos a HEAD 7288d93e: se localiza por nombre de función. Un aviso con deskops message send --to <repo> lleva como título el de la tarea y como cuerpo qué cambió y el commit; si el comando responde que el repo no está registrado, el aviso va como línea "Aviso a <repo>: ..." en el informe. "Un store de prueba" se arma con las fixtures o helpers que ya usa el archivo de test nombrado (leerlo primero); si no hay, con sldb.api (stores init, add_model, create_document) en tmp_path.

## Implementation Path

_Outline the expected implementation route or affected surface._

1) Leer edge_effects.py 30-50, where_literal.py 40-60 y where_subject.py 1-40. 2) Escribir brace_text. 3) Usarla en los dos caminos. 4) Tests. 5) Correr los tres archivos de Validation.

## Validation

_List the checks required before this task can close._

- TMPDIR=/dev/shm pytest -q tests/api/test_edge_effects.py
- TMPDIR=/dev/shm pytest -q tests/store/test_predicate_language.py
- TMPDIR=/dev/shm pytest -q tests/store/test_where_empty_and_errors.py

## Done When

_Name the observable condition that makes the task complete._

Los tres comandos pasan; grep -n "safe_dump" src/sldb/api/edges/edge_effects.py ya no aparece en _written; los cinco casos dan el mismo texto por effects y por where_subject; CHANGELOG y commit.

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

FILE:src/sldb/store/query_engine/where_literal.py
"""String literals of the `--where` grammar: their pattern, their value, and how to write one.

`split_outside_literals` cuts an expression where a separator appears outside every literal,
so a quoted `" and "` or `"{x}"` is never mistaken for grammar.
"""

from __future__ import annotations

import re
from decimal import Decimal
from typing import Any

# '"', then non-quote/non-backslash chars or a backslash escaping any char, then '"'.
# The value unquotes \" -> " and \\ -> \.
LITERAL = r'"(?:[^"\\]|\\.)*"'
LITERAL_NONEMPTY = r'("(?:[^"\\]|\\.)+")'


def unquote(raw: str) -> str:
    """The literal's value: the quotes off, the two escapes resolved; any other backslash survives verbatim."""
    body, out, i = raw[1:-1], [], 0
    while i < len(body):
        if body[i] == "\\" and i + 1 < len(body) and body[i + 1] in ('"', "\\"):
            out.append(body[i + 1])
            i += 2
        else:
            out.append(body[i])
            i += 1
    return "".join(out)


def quote(value: str) -> str:
    """The literal whose value is `value` (the inverse of `unquote`)."""
    return '"' + value.replace("\\", "\\\\").replace('"', '\\"') + '"'


def split_outside_literals(text: str, separator: str) -> list[str]:
    """`text` cut at every match of the `separator` regex that is not inside a literal."""
    parts, last = [], 0
    for m in re.finditer(f"({LITERAL})|{separator}", text):
        if m.group(1) is None:
            parts.append(text[last:m.start()])
            last = m.end()
    return parts + [text[last:]]


def scalar_literal(value: Any) -> str | None:
    """`value` written in the grammar: a quoted string or a number; None for anything else."""
    if isinstance(value, bool) or not isinstance(value, (str, int, float)):
        return None
    return quote(value) if isinstance(value, str) else format(Decimal(repr(value)), "f")

FILE:src/sldb/store/query_engine/where_subject.py
"""A `--where` predicate on a plain payload, with `{field}` filled from a subject.

An edge's condition names fields of the document it is tested on, and may name fields of a
subject in braces (`capacity >= {party_size}`). Braces are filled only outside literals,
each with the subject's value written as a literal; a brace whose field the subject lacks,
or holds a non-scalar, makes the condition not hold, as an absent field does.
"""

from __future__ import annotations

import re
from typing import Any

from sldb.store.query_engine.where_literal import LITERAL, scalar_literal

_BRACE = re.compile(f"({LITERAL})|\\{{([A-Za-z_]\\w*)\\}}")


def fill_braces(expression: str, subject: dict[str, Any]) -> tuple[str, bool]:
    """`expression` with every `{field}` replaced by the subject's value, and whether all were.

    A brace that cannot be filled becomes a placeholder literal, so the expression still parses.
    """
    missing: list[str] = []

    def fill(m: re.Match) -> str:
        if m.group(1) is not None:
            return m.group(1)
        written = scalar_literal(subject.get(m.group(2)))
        missing.extend([] if written is not None else [m.group(2)])
        return written if written is not None else '"?"'

    return _BRACE.sub(fill, expression), not missing


def payload_matches(expression: str, payload: dict[str, Any], subject: dict[str, Any] | None = None, name: str = "") -> bool:
    """Whether `expression` holds on `payload`; `{field}` reads `subject` (default: `payload`).

    The predicate language (GO05) evaluates it: `doc ~ "..."` reads `name`; `model <= X` never
    holds, a payload carries no model class. An empty expression always holds. Raises
    WherePredicateError when it does not parse.
    """
    from sldb.store.graph.language.predicate_documents import payload_holds

    return payload_holds(expression, payload, subject, name)

FILE:src/sldb/api/edges/edge_effects.py
"""An edge's effects on a subject: its `sets` with `{field}` filled from the subject, and `terminal`."""

from __future__ import annotations

import re
from typing import Any

import yaml

_FIELD = re.compile(r"\{([A-Za-z_]\w*)\}")


def effects_of(attributes: dict[str, Any] | None, subject: dict[str, Any]) -> dict[str, Any] | None:
    """`{"sets": ..., "terminal": ...}` of an edge whose `attributes` follow the transition convention.

    Absent or null `attributes`/`sets` are `sets = {}`; absent or null `terminal` is false; other
    keys stay out. `{field}` (where_subject's syntax) is filled only inside strings, each string
    of a list too, with the subject's scalar in its YAML form (true/false, numbers, strings as
    they are). None when a `{field}` is absent, null or not a scalar: the edge does not hold.
    """
    attributes = attributes or {}
    try:
        sets = {key: _resolved(value, subject) for key, value in (attributes.get("sets") or {}).items()}
    except LookupError:
        return None
    return {"sets": sets, "terminal": bool(attributes.get("terminal"))}


def _resolved(value: Any, subject: dict[str, Any]) -> Any:
    """`value` with `{field}` filled in its strings; LookupError when one cannot be."""
    if isinstance(value, list):
        return [_resolved(item, subject) for item in value]
    if not isinstance(value, str):
        return value
    return _FIELD.sub(lambda m: _written(subject.get(m.group(1)), m.group(1)), value)


def _written(value: Any, field: str) -> str:
    """The subject's scalar as text: a string as is, any other scalar in its YAML form."""
    if isinstance(value, str):
        return value
    if isinstance(value, (bool, int, float)):
        return yaml.safe_dump(value).split("\n", 1)[0]
    raise LookupError(field)

FILE:tests/store/test_predicate_language.py
"""GO05: the unified predicate language against the two old ones (rules-language.md §7).

`PAYLOADS` is the fixed set of payloads (p5): null, lists, an absent field, numbers and
strings. `tests/fixtures/where_goldens/` holds, for each row of the equivalence table, the old
expression (a `where_parse` string, or a `FieldCondition` as its JSON dict, p13) and the
sorted names of the payloads it matched, captured with the code of main before GO05 touched
`src/` (commit 4d090ee2). The old evaluators are gone (GO10): the old expression is data, and
each row evaluates its new construction of §7 against the golden. The goldens are never
regenerated. An old evaluator that raised on a payload (where_parse ordering `None` or mixed
types raises TypeError) counted as "does not match".
"""

from __future__ import annotations

import json
from pathlib import Path

import pytest

GOLDENS = Path(__file__).resolve().parents[1] / "fixtures" / "where_goldens"

PAYLOADS: dict[str, dict] = {
    "absent": {},
    "closed": {"status": "closed", "priority": 5, "tags": [], "title": "alpha beta", "note": ""},
    "float": {"status": "draft", "priority": 2.5, "tags": ["y"], "title": "Draft", "note": "b"},
    "list_valued": {"status": ["open"], "priority": [2], "tags": "x-y", "title": ["draft"], "note": ["n"]},
    "null": {"status": None, "priority": None, "tags": None, "title": None, "note": None},
    "numeric_text": {"status": "3", "priority": 3, "tags": ["3"], "title": "3", "note": "x"},
    "open": {"status": "open", "priority": 2, "tags": ["x", "y"], "title": "draft spec", "note": "a"},
}

# (table row, old where_parse expression); the new construction is the same text (§7 rows 1-11)
WHERE_ROWS: list[tuple[str, str]] = [
    ("1", "has(status)"),
    ("2", "nonempty(tags)"),
    ("3", '"x" in tags'),
    ("4", 'title ~ "dra"'),
    ("5", "model <= BaseDoc"),
    ("6", 'status = "open"'),
    ("6", "priority = 2"),
    ("7", 'status != "open"'),
    ("7", "priority != 2"),
    ("9", "priority <= 3"),
    ("11", "priority >= 3"),
]

# (table row, old FieldCondition dict, new construction of §7)
FIELD_CONDITION_ROWS: list[tuple[str, dict, str]] = [
    ("12", {"field": "status", "op": "eq", "value": "open"}, 'status = "open"'),
    ("13", {"field": "status", "op": "ne", "value": "open"}, 'status != "open"'),
    ("14", {"field": "priority", "op": "gt", "value": 2}, "priority > 2"),
    ("15", {"field": "priority", "op": "lt", "value": 3}, "priority < 3"),
    ("16", {"field": "tags", "op": "contains", "value": "x"}, '"x" in tags'),
    ("17", {"field": "title", "op": "starts_with", "value": "dra"}, 'title ~ "^dra"'),
    ("18", {"field": "note", "op": "is_null", "value": None}, "not has(note)"),
    ("19", {"field": "note", "op": "is_not_null", "value": None}, "has(note)"),
]


def _golden(name: str) -> list[dict]:
    return json.loads((GOLDENS / f"{name}.json").read_text(encoding="utf-8"))


def _matching(check) -> list[str]:
    names = []
    for name, payload in sorted(PAYLOADS.items()):
        try:
            if check(payload):
                names.append(name)
        except TypeError:
            pass
    return names


def test_the_goldens_cover_every_row_in_order():
    assert [g["old"] for g in _golden("where_parse")] == [old for _, old in WHERE_ROWS]
    assert [g["old"] for g in _golden("field_condition")] == [old for _, old, _ in FIELD_CONDITION_ROWS]


# Where the new language answers otherwise than the golden, and why (rules-language.md §7).
WHERE_DIFFERENCES = {
    # an absent field holds no comparison; where_parse let `!=` with a number literal hold on it
    "priority != 2": {"absent"},
}
FIELD_CONDITION_DIFFERENCES = {
    "16": {"list_valued"},  # contains: also a substring in the new language ("x" in "x-y")
    "18": {"closed"},  # is_null ~ not has(f): has also rejects ""
    "19": {"closed"},  # is_not_null ~ has(f): has also rejects ""
}


def _changed(new: list[str], golden: list[str]) -> set[str]:
    return set(new) ^ set(golden)


def test_where_parse_rows_answer_their_goldens_in_the_new_language():
    from sldb.api.where import where_matches

    for (row, old), golden in zip(WHERE_ROWS, _golden("where_parse")):
        assert golden["old"] == old, row
        new = _matching(lambda payload: where_matches(old, payload))
        assert _changed(new, golden["matches"]) == WHERE_DIFFERENCES.get(old, set()), (row, old)


def test_field_condition_rows_answer_their_goldens_with_the_construction_of_the_table():
    from sldb.store.graph.language.predicate_documents import payload_holds

    for (row, old, construction), golden in zip(FIELD_CONDITION_ROWS, _golden("field_condition")):
        assert golden["old"] == old, row
        through_the_language = _matching(lambda p: payload_holds(construction, {k: v for k, v in p.items() if v is not None}))
        assert _changed(through_the_language, golden["matches"]) == FIELD_CONDITION_DIFFERENCES.get(row, set()), row


def test_the_new_api_does_not_warn():
    import warnings

    from sldb.api.where import where_matches
    from sldb.store.graph.language.predicate_parser import parse_predicate

    with warnings.catch_warnings():
        warnings.simplefilter("error", DeprecationWarning)
        assert where_matches('status = "open" and not has(note)', {"status": "open"})
        assert parse_predicate('any(depends_on: status = "open")').text


# --- GraphBackend.eval over a composed index (GO05 step 3; h1, p8, p10) ------------------

def _index(payloads: dict[str, dict], edges: list[tuple], bases: dict[str, list[str]] | None = None):
    from sldb.store.edge_index.edge_index import EdgeIndex
    from sldb.store.models import EdgeNodeRecord, EdgeRecord

    docs = [EdgeNodeRecord(id=f"sldb://document/{i}", node_type=i.split(":")[0], payload=p) for i, p in payloads.items()]
    models = [EdgeNodeRecord(id=f"sldb://model/{m}", node_type="sldb_model", semantics={"base_models": b}) for m, b in (bases or {}).items()]
    records = [EdgeRecord(source=f"sldb://document/{s}", target=f"sldb://document/{t}", relation=r, metadata=m) for s, r, t, m in edges]
    return EdgeIndex(nodes={n.id: n for n in docs + models}, edges=records)


def _backend(index, projection=None):
    from sldb.store.graph.backend import NetworkXBackend

    backend = NetworkXBackend()
    backend.load(index, projection)
    return backend


_TASKS = {"Task:a": {"depends_on": ["Task:b", "Task:c"], "subject": "Task:b"}, "Task:b": {"status": "closed"}, "Task:c": {"status": "open"}, "Sub:d": {"status": "open"}}
_EDGES = [
    ("Task:a", "references", "Task:b", {"field": "depends_on", "declared": "Task:b"}),
    ("Task:a", "references", "Task:c", {"field": "depends_on", "declared": "Task:c"}),
    ("Task:a", "references", "Task:b", {"field": "subject", "declared": "Task:b"}),
    ("Task:c", "task_activates", "Sub:d", {}),
]


def test_backend_eval_follows_paths_over_the_index():
    backend = _backend(_index(_TASKS, _EDGES))
    holds = lambda text: backend.eval(text, {"id": "Task:a", **_TASKS["Task:a"]})[0]["holds"]  # noqa: E731
    assert holds('any(depends_on: status = "open")') == "true"
    assert holds('all(depends_on: status = "closed")') == "false"
    assert holds('any(depends_on.rel:task_activates: status = "open")') == "true"
    assert backend.eval('any(^depends_on: has(subject))', {"id": "Task:b"})[0]["holds"] == "true"


def test_backend_eval_without_subject_covers_every_document_of_the_index():
    backend = _backend(_index(_TASKS, _EDGES, {"Sub": ["Task"]}))
    assert [f["node"] for f in backend.eval("has(status)")] == ["Sub:d", "Task:a", "Task:b", "Task:c"]
    assert [f["node"] for f in backend.eval('model <= Task and status = "open"')] == ["Sub:d", "Task:a", "Task:b", "Task:c"]
    assert [f["node"] for f in backend.eval('model <= Sub and status = "open"')] == ["Sub:d"]


def test_backend_eval_by_export_id_reads_the_projection():
    projection = {i: dict(p) for i, p in _TASKS.items()}
    backend = _backend(_index(_TASKS, _EDGES), projection)
    assert backend.eval('any(depends_on: status = "open")', "Task:a")[0]["holds"] == "true"


def test_anchor_state_is_exposed_when_the_origin_carries_the_entry():
    projection = {**{i: dict(p) for i, p in _TASKS.items()}}
    projection["Task:a"] = {**_TASKS["Task:a"], "depends_on__anchor_state": ["fresh", "stale"], "subject__anchor_state": "fresh"}
    backend = _backend(_index(_TASKS, _EDGES), projection)
    finding = backend.eval('any(depends_on: anchor_state = "stale")', "Task:a")[0]
    assert (finding["holds"], finding["seen"]) == ("true", {"anchor_state": "stale"})
    assert backend.eval('all(depends_on: has(anchor_state))', "Task:a")[0]["holds"] == "true"
    assert backend.eval('any(subject: anchor_state = "fresh")', "Task:a")[0]["holds"] == "true"


def test_anchor_state_is_undefined_without_the_entry():
    backend = _backend(_index(_TASKS, _EDGES), {i: dict(p) for i, p in _TASKS.items()})
    assert backend.eval("any(depends_on: has(anchor_state))", "Task:a")[0]["holds"] == "false"


def test_backend_eval_and_eval_predicate_give_the_same_findings():
    from sldb.store.query_engine.rules import eval_predicate, parse_predicate

    nodes = {i: {"model": i.split(":")[0], "payload": p, "base_models": ["Task"] if i.startswith("Sub") else []} for i, p in _TASKS.items()}
    graph = {"nodes": nodes, "edges": [{"source": s, "type": r, "target": t, **m} for s, r, t, m in _EDGES]}
    backend = _backend(_index(_TASKS, _EDGES, {"Sub": ["Task"]}))
    for text in ('any(depends_on: status = "open")', "count(depends_on+: has(status)) = 2", "model <= Task and not has(status)", 'none(rel:task_activates: status = "open")'):
        assert backend.eval(parse_predicate(text)) == eval_predicate(parse_predicate(text), graph), text


# --- the CLI: find --where (paths, --explain), graph query's where, zero extractions -----

_TASK_MODULE = "sldb_go05_predicate_models"
_TASK_MODELS = '''from pydantic import Field
from sldb import StructuredNLDoc


class Task(StructuredNLDoc):
    __references__ = ["depends_on"]
    __template__ = """---
status: ⸢rev•status⸥
depends_on: ⸢rev•depends_on⸥
---

# ⸢rev•title⸥
"""
    title: str = Field(description="Title.")
    status: str = Field(description="Status.")
    depends_on: list[str] = Field(default_factory=list, description="Tasks this one waits for.")
'''


@pytest.fixture
def tasks(tmp_path):
    import sys

    from sldb import api

    (tmp_path / f"{_TASK_MODULE}.py").write_text(_TASK_MODELS, encoding="utf-8")
    sys.path.insert(0, str(tmp_path))
    try:
        root = tmp_path / "world"
        root.mkdir()
        sp, py = api.init_store(root).store_path, str(tmp_path)
        api.add_model(sp, f"{_TASK_MODULE}:Task", py)
        for name, status, depends in (("b", "closed", []), ("c", "open", []), ("a", "open", ["Task:b", "Task:c"]), ("d", "open", ["Task:b"])):
            api.create_document(sp, "Task", root / f"{name}.md", {"title": name, "status": status, "depends_on": depends}, name, py)
        yield sp, py
    finally:
        sys.path.remove(str(tmp_path))
        sys.modules.pop(_TASK_MODULE, None)


def _cli(*argv: str) -> tuple[int, str]:
    import contextlib
    import io

    from sldb.cli import main as cli_main

    out = io.StringIO()
    with contextlib.redirect_stdout(out):
        code = cli_main(list(argv))
    return code, out.getvalue()


def _find(sp, py, where: str, *extra: str) -> dict:
    code, printed = _cli("--envelope", "find", "Task", "--type", "doc", "--where", where, "--format", "json", "--store", str(sp), "--pythonpath", py, *extra)
    return json.loads(printed)


def test_find_where_any_over_a_relation_answers_through_the_envelope(tasks):
    envelope = _find(*tasks, 'any(depends_on: status = "open")')
    assert envelope["ok"] and envelope["warnings"] == []
    assert [r["doc"] for r in envelope["data"]["results"]] == ["a"]
    assert "findings" not in envelope["data"]


def test_find_where_all_with_explain_names_the_failing_clause_per_document(tasks):
    envelope = _find(*tasks, 'all(depends_on: status = "closed")', "--explain")
    assert sorted(r["doc"] for r in envelope["data"]["results"]) == ["b", "c", "d"]
    findings = {f["node"]: f for f in envelope["data"]["findings"]}
    assert sorted(findings) == ["Task:a", "Task:b", "Task:c", "Task:d"]
    assert findings["Task:a"] == {"node": "Task:a", "holds": "false", "clause": 'all(depends_on: status = "closed")', "seen": {"status": "open"}}
    assert {f["holds"] for n, f in findings.items() if n != "Task:a"} == {"true"}


def test_find_where_with_the_same_expression_does_not_warn(tasks):
    import warnings

    with warnings.catch_warnings():
        warnings.simplefilter("error", DeprecationWarning)
        envelope = _find(*tasks, 'status = "closed"')
    assert envelope["warnings"] == [] and [r["doc"] for r in envelope["data"]["results"]] == ["b"]


def test_graph_query_with_a_where_filter_answers_without_warnings(tasks, tmp_path):
    sp, py = tasks
    query = tmp_path / "query.json"
    query.write_text(json.dumps({"filters": [{"facet": "payload", "where": 'status = "closed"'}]}), encoding="utf-8")
    plain_code, plain = _cli("graph", "query", "--query-file", str(query), "--store", str(sp), "--local")
    code, printed = _cli("--envelope", "graph", "query", "--query-file", str(query), "--store", str(sp), "--local")
    envelope = json.loads(printed)
    assert plain_code == code == 0 and envelope["data"] == json.loads(plain)
    assert [n["id"] for n in envelope["data"]] == ["sldb://document/Task:b"]
    assert envelope["warnings"] == []


def test_a_path_in_a_facet_where_is_rejected_naming_it():
    from sldb.store.edge_index.edge_index import EdgeIndex
    from sldb.store.exceptions import SLDBGraphArgumentError
    from sldb.store.graph import StructuredQuery, execute_query

    query = StructuredQuery.model_validate({"filters": [{"facet": "payload", "where": 'any(depends_on: status = "open")'}]})
    with pytest.raises(SLDBGraphArgumentError, match="any\\(depends_on"):
        execute_query(EdgeIndex(nodes={}), query)


def test_where_over_every_document_of_a_repo_model_extracts_nothing(tmp_path, monkeypatch):
    from sldb import api
    from sldb.api.where import where_findings
    from sldb.runtime.validation import Validator
    from sldb.store.edge_index.compose import invalidate_composed_edge_indexes
    from sldb.store.io.shards import invalidate_shard_cache
    from sldb.store.runtime_cache import invalidate_runtime_cache

    repo = str(Path(__file__).resolve().parents[2])
    root = tmp_path / "world"
    root.mkdir()
    sp = api.init_store(root).store_path
    api.add_model(sp, "docs.models:SpecDoc", repo)
    for name in ("alpha", "beta", "gamma"):
        api.create_document(sp, "SpecDoc", root / f"{name}.md", {"title": name, "body": f"About {name}."}, name, repo)
    calls = []
    original = Validator.extract
    monkeypatch.setattr(Validator, "extract", lambda self, md: calls.append(1) or original(self, md))
    invalidate_composed_edge_indexes(), invalidate_shard_cache(), invalidate_runtime_cache()
    findings = where_findings(sp, 'model <= SpecDoc and title ~ "a"')
    assert [(f["node"], f["holds"]) for f in findings] == [("SpecDoc:alpha", "true"), ("SpecDoc:beta", "true"), ("SpecDoc:gamma", "true")]
    assert calls == []

FILE:tests/api/test_edge_effects.py
"""Transitions as edge data (GO09): a RelationDoc's `attributes.sets/terminal` travel with the edge.

Covers: the convention validated on RelationDoc (one rejection per rule, through the existing
write path); `edges_holding` returns each holding edge with `effects` resolved (`{field}` of a
boolean written as true, absent attributes as `{sets: {}, terminal: false}`, extra keys left
out, an unfillable `{field}` makes the edge not hold); `apply_effects` builds the new payload
and rejects an invalid one; `effects` never shows in a dump while unset.
"""

from __future__ import annotations

import sys
from pathlib import Path

import pytest
from pydantic import ValidationError

from sldb import api

MODULE = "sldb_edge_effects_test_models"
MODELS = '''from pydantic import Field
from sldb import StructuredNLDoc


class State(StructuredNLDoc):
    __template__ = "# ⸢rev•title⸥"
    title: str = Field(description="Title.")


class Item(StructuredNLDoc):
    __template__ = "---\\nstatus: ⸢rev•status⸥\\ndone: ⸢rev•done⸥\\nclosed: ⸢rev•closed⸥\\n---\\n\\n# ⸢rev•title⸥"
    title: str = Field(description="Title.")
    status: str = Field(description="Where the item is.")
    done: bool = Field(default=False, description="Whether the work is done.")
    closed: str = Field(default="", description="Closing mark.")
'''
SUBMIT = {"sets": {"status": "review", "closed": "{done}"}, "terminal": False}
CLOSE = {"sets": {"status": "closed"}, "terminal": True, "owner": "ops"}


@pytest.fixture
def machine(tmp_path: Path):
    sys.modules.pop(MODULE, None)
    (tmp_path / f"{MODULE}.py").write_text(MODELS, encoding="utf-8")
    root, py = tmp_path / "desk", str(tmp_path)
    root.mkdir()
    store = api.init_store(root).store_path
    for model in ("State", "Item"):
        api.add_model(store, f"{MODULE}:{model}", py)
    api.init_relations(store, py)

    def create(model: str, name: str, payload: dict) -> None:
        api.create_document(store, model, root / f"{name}.md", payload, name, py)

    for state in ("open", "review", "closed"):
        create("State", state, {"title": state})
    create("RelationTypeDoc", "rt-moves", {"title": "moves", "name": "moves_to", "source_types": ["State"], "target_types": ["State"], "description": "A transition."})
    for name, source, target, condition, attributes in (
        ("e-submit", "open", "review", 'status = "open"', SUBMIT),
        ("e-abandon", "open", "closed", 'status = "abandoned"', None),
        ("e-close", "review", "closed", "nonempty(status)", CLOSE),
    ):
        payload = {"title": name, "source_id": f"State:{source}", "target_id": f"State:{target}", "relation_type": "moves_to", "condition": condition}
        create("RelationDoc", name, payload | ({"attributes": attributes} if attributes else {}))
    return store, py, create


def _relation(attributes: object) -> dict:
    return {"title": "bad", "source_id": "State:open", "target_id": "State:review", "relation_type": "moves_to", "attributes": attributes}


def test_the_holding_transition_carries_its_resolved_effects(machine):
    store, _, _ = machine
    [edge] = api.edges_holding(store, "State:open", {"title": "i", "status": "open", "done": True}, "moves_to")
    assert edge.target == "sldb://document/State:review"
    assert edge.effects == {"sets": {"status": "review", "closed": "true"}, "terminal": False}


def test_an_edge_without_attributes_has_empty_effects(machine):
    store, _, _ = machine
    [edge] = api.edges_holding(store, "State:open", {"status": "abandoned", "done": False}, "moves_to")
    assert edge.target == "sldb://document/State:closed"
    assert edge.effects == {"sets": {}, "terminal": False}


def test_an_extra_attribute_stays_out_of_effects(machine):
    store, _, _ = machine
    [edge] = api.edges_holding(store, "State:review", {"status": "review"}, "moves_to")
    assert edge.effects == {"sets": {"status": "closed"}, "terminal": True}
    assert edge.metadata["attributes"]["owner"] == "ops"


@pytest.mark.parametrize("done", [None, {"a": 1}, "absent"])
def test_an_unfillable_field_makes_the_edge_not_hold(machine, done):
    store, _, _ = machine
    subject = {"status": "open"} | ({} if done == "absent" else {"done": done})
    assert api.edges_holding(store, "State:open", subject, "moves_to") == []


def _item(store, py):
    return api.load_registered_model(store, "Item", py).model_type


def test_apply_effects_builds_the_new_payload(machine):
    store, py, _ = machine
    subject = {"title": "i", "status": "open", "done": True, "closed": ""}
    [edge] = api.edges_holding(store, "State:open", subject, "moves_to")
    new = api.apply_effects(subject, edge.effects, _item(store, py))
    assert new == {"title": "i", "status": "review", "done": True, "closed": "true"}
    assert subject["status"] == "open"
    assert api.apply_effects({"title": "i", "status": "open"}, {"sets": {"extra_list": ["a"]}, "terminal": False}, _item(store, py))["extra_list"] == ["a"]


def test_apply_effects_rejects_a_value_invalid_for_the_model(machine):
    store, py, _ = machine
    with pytest.raises(ValidationError, match="done"):
        api.apply_effects({"title": "i", "status": "open"}, {"sets": {"done": "maybe"}, "terminal": False}, _item(store, py))
    with pytest.raises(ValidationError, match="status"):
        api.apply_effects({"title": "i", "status": "open"}, {"sets": {"status": None}, "terminal": False}, _item(store, py))


@pytest.mark.parametrize("value,kind", [({"a": 1}, "a map"), ([["a"]], "a nested list")])
def test_apply_effects_rejects_a_value_that_is_not_scalar(machine, value, kind):
    store, py, _ = machine
    with pytest.raises(ValueError, match=f"attributes.sets.status.*{kind}"):
        api.apply_effects({"title": "i", "status": "open"}, {"sets": {"status": value}}, _item(store, py))


@pytest.mark.parametrize(
    "attributes,reason",
    [
        (["sets"], "valid dictionary"),
        ({"sets": "status=closed"}, "attributes.sets must be a map"),
        ({"terminal": "yes"}, "attributes.terminal must be a boolean"),
        ({"sets": {"status": {"to": "closed"}}}, "attributes.sets.status .*a map"),
        ({"sets": {"tags": [["a"]]}}, "attributes.sets.tags .*a nested list"),
    ],
    ids=["attributes-not-map", "sets-not-map", "terminal-not-bool", "sets-value-map", "sets-value-nested-list"],
)
def test_the_convention_is_rejected_when_writing_the_relation_doc(machine, attributes, reason):
    _, _, create = machine
    with pytest.raises(ValidationError, match=f"(?s)attributes.*{reason}"):
        create("RelationDoc", "e-bad", _relation(attributes))


@pytest.mark.parametrize("attributes", [None, {}, {"sets": None, "terminal": None}, {"sets": {"x": None, "tags": ["a", 1, True, None]}, "terminal": True, "role": {"free": [1]}}])
def test_the_convention_accepts_its_defaults_and_free_keys(attributes):
    from sldb.models.relation_doc import RelationDoc

    assert RelationDoc(**_relation(attributes)).attributes == (attributes or {})


def test_effects_fill_strings_with_yaml_scalars_and_keep_null():
    subject = {"done": False, "n": 3, "x": 1.5, "big": 1e20, "who": 'J "P"'}
    sets = {"a": "{done}", "b": "n={n} x={x}", "c": "{big}", "d": "{who}", "e": None, "f": ["{n}", 2, "{done}"], "g": "{{who}}"}
    effects = api.effects_of({"sets": sets}, subject)
    assert effects == {"sets": {"a": "false", "b": "n=3 x=1.5", "c": "1.0e+20", "d": 'J "P"', "e": None, "f": ["3", 2, "false"], "g": '{J "P"}'}, "terminal": False}
    assert api.effects_of({"sets": {"f": ["ok", "{missing}"]}}, subject) is None


def test_effects_stay_out_of_every_dump_while_unset(machine):
    store, _, _ = machine
    record = api.EdgeRecord(source="a", target="b", relation="r")
    assert "effects" not in record.model_dump() and "effects" not in record.model_dump_json()
    assert all("effects" not in e for e in api.serialize_edge_records(api.edges_from(store, "State:open")))
    [held] = api.edges_holding(store, "State:review", {"status": "review"}, "moves_to")
    assert api.serialize_edge_record(held)["effects"] == {"sets": {"status": "closed"}, "terminal": True}

FILE:instruccion
Cold-bundle de la tarea task-una-sola-forma-de-serializar-un-escalar-al-sustituir-llaves-effects-go09-y-where-subject-usan-la-mis: con el TaskDoc, los rituales enrutados por el Board, las pills ligadas, los átomos ligados y los archivos que el TaskDoc nombra, reformula el encargo, lista ambigüedades con cita textual del input y da el DRY-RUN sin ejecutar nada. No ejecutes nada.

Sección de validación del TaskDoc:
- TMPDIR=/dev/shm pytest -q tests/api/test_edge_effects.py
- TMPDIR=/dev/shm pytest -q tests/store/test_predicate_language.py
- TMPDIR=/dev/shm pytest -q tests/store/test_where_empty_and_errors.py

