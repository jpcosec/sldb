FILE:desk/tasks/task-go05-lenguaje-de-predicados-unificado.md
---
id: task-go05-lenguaje-de-predicados-unificado
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
- src/sldb/store/graph/language/__init__.py
- src/sldb/store/graph/language/field_condition.py
- src/sldb/store/graph/language/predicate_ast.py
- src/sldb/store/graph/language/predicate_parser.py
- src/sldb/store/graph/language/predicate_eval.py
- src/sldb/store/graph/language/predicate_paths.py
- src/sldb/store/graph/language/predicate_explain.py
- src/sldb/store/graph/backend/parser.py
- src/sldb/store/graph/backend/tokens.py
- src/sldb/store/graph/backend/evaluate.py
- src/sldb/store/graph/backend/eval.py
- src/sldb/store/graph/backend/networkx_backend.py
- src/sldb/store/graph/executor.py
- src/sldb/store/graph/payload_match.py
- src/sldb/store/query_engine/where_parse.py
- src/sldb/store/query_engine/where_subject.py
- src/sldb/store/query_engine/structural_queries.py
- src/sldb/api/where.py
- src/sldb/api/edges/edges_holding.py
- src/sldb/cli/parsers/find.py
- src/sldb/cli/commands/find.py
- src/sldb/cli/commands/find_filter.py
- src/sldb/cli/commands/graph.py
- docs/architecture/rules-language.md
- docs/architecture/graph-backend.md
- CHANGELOG.md
- tests/test_rules_language_spec.py
- tests/store/test_predicate_language.py
- tests/fixtures/where_goldens/
task_type: task.code
inherits_from: []
inherit_acceptance_context: false
atoms: []
---

# GO05: Lenguaje de predicados unificado

## Rationale

_Explain why this task exists or the business driver behind it._

Nodo GO05 del plan desk/drawer/plans/grafo-operable (dag.yaml rev 9), hijo de PK02. Hoy hay dos lenguajes de condicion (where_parse y FieldCondition), ninguno cruza relaciones ni tiene or/not/parentesis, y --where re-extrae el payload. GO02 fijo la semantica (docs/architecture/rules-language.md, 52 xfail), GO03 la costura GraphBackend (eval sobre el subconjunto sin caminos) y GO04 la facet payload en el indice (d7eefdeb). GO05 implementa el lenguaje completo sobre esas dos piezas y deja los lenguajes viejos como shims deprecados.

## Goal

_Describe the concrete result this task must produce._

Un parser y un evaluador del lenguaje de GO02 (booleanos completos, caminos con cuantificadores, clausura transitiva, sustitucion desde el sujeto, incomplete en el borde de links, explicacion estructurada) detras de GraphBackend.eval y de una API unica que usan where_matches, edges_holding, StructuredQuery y --where; where_parse y FieldCondition quedan como shims con DeprecationWarning; los 52 tests xfail de GO02 pasan a verdes.

## Scope

_State what is in scope and what is out of scope._

En alcance: src/sldb/store/graph/language/ (AST, parser, evaluador, caminos, explicacion; FieldCondition como shim), src/sldb/store/graph/backend/ (eval deja de levantar NotImplementedError ante caminos), src/sldb/store/query_engine/ (where_parse y compile_where como shims), src/sldb/api/where.py y src/sldb/api/edges/edges_holding.py (enrutados a la API unica), la CLI --where de docs find y su --explain, el envelope de sldb graph query, docs/architecture/rules-language.md y graph-backend.md, CHANGELOG.md, tests. Fuera: RuleDoc y rules check (GO06), anclas doc: y la produccion de F__anchor_state (GO07), transiciones como datos (GO09), evaluacion incremental (GO08), retiro de los shims (GO10), la firma de __indexed__ en contract_signature (drawer task-cambiar-indexed-de-un-modelo-no-marca-stale-la-proyeccion-del-payload).

HEREDADO DE NODOS ANTERIORES: (h1, de GO03 H4) GraphBackend.eval sin sujeto evalua sobre todos los documentos de la proyeccion cargada (rules-language.md, dominio sin sujeto); hoy devuelve [] con proyeccion None. (h2, de GO03 H1) eval recibe el predicado como texto y lo parsea; GO05 expone ademas el tipo predicado parseado publico que eval acepta. (h3, de GO04 H2/H3/H6) la facet payload solo existe en nodos de documento; un campo nulo no llega a la proyeccion; un campo que ningun modelo proyecta es SLDBGraphArgumentError. (h4) El comando de la CLI que entra por la via vieja es sldb graph query (recibe un StructuredQuery con FieldCondition como dicts JSON); --where es el de sldb docs find.

PRECISIONES (preflight de GO05, 2026-11-06):
p1 (comando viejo): el comando de consulta estructurada que entra por la via vieja es sldb graph query (src/sldb/cli/parsers/graph.py, "Run a structured query from a JSON file"). Cuando su StructuredQuery trae FieldCondition como dicts, el envelope (sldb --envelope graph query <archivo>) lleva en warnings una entrada con la forma de docs/cli-envelope.md: level "warning", code "deprecated/field-condition", subject "graph query", what que nombra el reemplazo (la expresion del lenguaje nuevo). La salida de data no cambia.
p2 (gramatica): la sintaxis de booleanos, caminos (campo, rel:tipo, ^campo), cuantificadores any/all/none/count, clausura, precedencia, sustitucion {campo} e incomplete es la de docs/architecture/rules-language.md secciones 1-3 y 6 (G_SEMANTICS satisfecho); los 52 tests de tests/test_rules_language_spec.py son la spec ejecutable y no se modifican salvo quitar la marca xfail. Nada de sintaxis se inventa fuera de ese documento; un hueco se registra como hipotesis.
p3 (--explain): sldb docs find --where <expr> --explain agrega a data la clave findings: lista con un finding (node, holds, clause, seen; rules-language.md seccion 4) por cada documento evaluado, incluidos los que no cumplen; el resultado de find (los documentos que cumplen) no cambia. Sin --explain la salida es identica a la actual. La clave de rules explain sigue siendo de GO06 (H10).
p4 (anchor_state): GO07 aun no produce F__anchor_state; el alias se prueba con una proyeccion sintetica cargada en el backend (load(indice, proyeccion)) cuya facet de origen trae la entrada F__anchor_state, y con otra sin ella (has(anchor_state) es false). No se escribe nada de GO07.
p5 (goldens): antes de tocar src/, un primer commit captura con el codigo de main tests/fixtures/where_goldens/where_parse.json y tests/fixtures/where_goldens/field_condition.json: para cada fila de la tabla de equivalencia (rules-language.md seccion 7), la expresion vieja y la lista ordenada de nombres de los payloads que cumple, sobre un conjunto fijo de payloads definido en tests/store/test_predicate_language.py (cubre null, listas, campo ausente, numeros, strings). El test de equivalencia evalua la columna nueva sobre los mismos payloads y compara con el golden; los goldens no se regeneran despues.
p6 (extract): Validator.extract es sldb.runtime.validation.Validator.extract; el test lo cuenta con monkeypatch (como test_status_closed_is_answered_with_zero_extractions de GO04).

## Implementation Path

_Outline the expected implementation route or affected surface._

CONTRATO DEL NODO (dag.yaml rev 9, GO05 scope): Parser y evaluador del lenguaje de GO02 sobre el backend de GO03 y la facet payload de GO04: booleanos completos, caminos con cuantificadores, clausura transitiva, sustitución desde el sujeto, incomplete en el borde de links, explicación estructurada. Alias genérico al atravesar un campo: cuando un camino atraviesa un campo F del documento origen y la facet del origen tiene una entrada derivada F__anchor_state (GO07 la produce), cada elemento alcanzado expone esa entrada bajo el nombre anchor_state; si la entrada no existe, anchor_state no está definido (has(anchor_state) es false). Compatibilidad: antes de cambiar nada, se capturan goldens del resultado de cada expresión de la tabla de GO02 con where_parse y FieldCondition actuales; luego la gramática nueva (superconjunto) reemplaza a where_parse, que queda como shim que delega en el parser nuevo y emite warnings.warn(DeprecationWarning); FieldCondition queda como shim que traduce al AST nuevo con el mismo aviso; en la CLI, --where entra siempre por la vía nueva y nunca avisa; el único comando de la CLI que entra por la vía vieja es el de consulta estructurada, el que hoy recibe FieldCondition como dicts JSON (nombre exacto del comando fijado en el TaskDoc), y ese agrega una entrada a la lista warnings del envelope (docs/cli-envelope.md); en Python, llamar a where_parse/compile_where o construir FieldCondition emite DeprecationWarning; los operadores de where_parse no avisan por sí mismos, porque la gramática nueva los incluye idénticos. Los tests de equivalencia comparan el resultado nuevo con los goldens. Los tests xfail de GO02 pasan a verdes. API única detrás de where_matches, edges_holding, StructuredQuery y --where. El retiro de los shims es GO10. ACEPTACION: Tests de spec de GO02 verdes; tests de equivalencia contra goldens verdes; sldb docs find --where con any()/all() sobre una relación responde desde la CLI con envelope y, con --explain, la cláusula fallida por documento; un test cuenta cero llamadas a Validator.extract al evaluar un --where sobre todos los documentos de un modelo de este repo; un test captura el DeprecationWarning al llamar a where_parse y al construir un FieldCondition, otro captura la entrada en warnings del envelope de graph query con filtros dict, y otro comprueba que --where con la misma expresión no avisa; CHANGELOG y docs/architecture actualizados. OUTPUT_SCOPE: src/sldb/store/query_engine/, src/sldb/store/graph/language/, src/sldb/api/where.py, src/sldb/api/edges/edges_holding.py (enrutado a la API única), CLI --where, docs/architecture/, CHANGELOG.md REGLAS COMUNES: alcance.md de desk/drawer/plans/grafo-operable (regla 2: no cierra con tests rojos ni saltados; regla 3: toda capacidad nueva entra con spec, CLI con envelope JSON, pruebas, CHANGELOG y doc en docs/architecture; regla 4: --where actual sigue funcionando; regla 5: nada se persiste del resultado de una regla; regla 6: ante un contrato ausente registrar la hipotesis en este TaskDoc, no inventar API). Semantica: docs/architecture/rules-language.md (GO02). Costura: docs/architecture/graph-backend.md (GO03, GO04).

## Validation

_List the checks required before this task can close._

- TMPDIR=/dev/shm pytest tests/test_rules_language_spec.py sin xfail ni skipped (los 52 pasan a verdes, sin marca xfail)
- tests de equivalencia contra los goldens de where_parse y FieldCondition capturados antes de tocar codigo
- test que cuenta cero llamadas a Validator.extract al evaluar un --where sobre todos los documentos de un modelo de este repo
- tests de DeprecationWarning (where_parse, compile_where, FieldCondition), de warnings en el envelope de sldb graph query con filtros dict, y de --where sin aviso
- sldb docs find --where con any()/all() sobre una relacion y --explain probado por CLI con envelope
- TMPDIR=/dev/shm pytest tests/test_clean_code_rules.py tests/test_store_seams.py en verde
- suite completa sin rojos (una vez, al final del nodo, la corre el supervisor)

## Done When

_Name the observable condition that makes the task complete._

Aceptacion de GO05 cumplida linea por linea, revision en frio aceptada, nodo integrado en main.

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

FILE:src/sldb/store/graph/language/__init__.py
"""The structured query language: facet filters, graph scope and relation filters."""

from sldb.store.graph.language.field_condition import FieldCondition
from sldb.store.graph.language.facet_filter import FacetFilter
from sldb.store.graph.language.graph_scope import GraphScope
from sldb.store.graph.language.relation_filter import RelationFilter
from sldb.store.graph.language.structured_query import StructuredQuery

__all__ = ["FacetFilter", "FieldCondition", "GraphScope", "RelationFilter", "StructuredQuery"]

FILE:src/sldb/store/graph/language/field_condition.py
"""One comparison condition on a facet field."""

from __future__ import annotations

from typing import Any, Literal

from pydantic import BaseModel, Field


class FieldCondition(BaseModel):
    """A single comparison condition on a facet field."""

    field: str = Field(description="Name of the field within the facet.")
    op: Literal["eq", "ne", "is_null", "is_not_null", "contains", "gt", "lt", "starts_with"] = Field(description="The comparison operator.")
    value: Any = Field(default=None, description="The value to compare against; ignored by the null operators.")

FILE:src/sldb/store/graph/backend/parser.py
"""The boolean grammar of the GO02 subset: `or` over `and` over `not` over parentheses and atoms."""

from __future__ import annotations

from sldb.store.graph.backend.atoms import atom
from sldb.store.graph.backend.state import expect_op, ident, is_op, peek, take
from sldb.store.graph.backend.tokens import tokenize
from sldb.store.query_engine.where_parse import WherePredicateError


def parse(text: str, expression: str):
    """Parse one predicate; the whole text must be consumed."""
    state = [tokenize(text, expression), 0]
    node = _or(state, text, expression)
    if peek(state).kind != "eof":
        raise WherePredicateError(expression)
    return node


def _or(state: list, text: str, expression: str):
    """`and` joined by `or`, left-associative."""
    node = _and(state, text, expression)
    while ident(state, "or"):
        take(state)
        right = _and(state, text, expression)
        node = ("or", node[1], right[2], text[node[1]:right[2]], node, right)
    return node


def _and(state: list, text: str, expression: str):
    """`not` joined by `and`, left-associative."""
    node = _not(state, text, expression)
    while ident(state, "and"):
        take(state)
        right = _not(state, text, expression)
        node = ("and", node[1], right[2], text[node[1]:right[2]], node, right)
    return node


def _not(state: list, text: str, expression: str):
    """`not` binds tighter than `and`; parentheses group."""
    if not ident(state, "not"):
        return _primary(state, text, expression)
    start = take(state).start
    child = _not(state, text, expression)
    return ("not", start, child[2], child)


def _primary(state: list, text: str, expression: str):
    if not is_op(state, "("):
        return atom(state, text, expression)
    take(state)
    node = _or(state, text, expression)
    expect_op(state, ")", expression)
    return node

FILE:src/sldb/store/graph/backend/tokens.py
"""Tokens of the GO02 predicate subset: literals, numbers, fields, keywords and operators."""

from __future__ import annotations

import re
from collections import namedtuple
from typing import Any

from sldb.store.query_engine.where_literal import unquote
from sldb.store.query_engine.where_parse import WherePredicateError

_TOKEN = re.compile(
    r"""\s*(?:
        (?P<literal>"(?:[^"\\]|\\.)*")
      | (?P<number>-?\d+(?:\.\d+)?)
      | (?P<ident>[A-Za-z_][\w.]*)
      | (?P<op>!=|<=|>=|[=<>~()\[\],{}:^+])
    )""",
    re.VERBOSE,
)
_Token = namedtuple("_Token", "kind value raw start end")


def tokenize(text: str, expression: str) -> list:
    """Every token of `text`, with its source offsets, ended by an `eof` token."""
    tokens: list = []
    position = 0
    while (token := _next_token(text, position, expression)) is not None:
        tokens.append(token)
        position = token.end
    tokens.append(_Token("eof", "", "", len(text), len(text)))
    return tokens


def _next_token(text: str, position: int, expression: str) -> Any:
    position = _skip_space(text, position)
    if position >= len(text):
        return None
    match = _TOKEN.match(text, position)
    if match is None or match.end() == position:
        raise WherePredicateError(expression)
    kind = match.lastgroup or ""
    raw = match.group(kind)
    return _Token(kind, _token_value(kind, raw), raw, match.start(kind), match.end(kind))


def _skip_space(text: str, position: int) -> int:
    while position < len(text) and text[position].isspace():
        position += 1
    return position


def _token_value(kind: str, raw: str) -> Any:
    if kind == "literal":
        return unquote(raw)
    if kind == "number":
        return int(raw) if re.fullmatch(r"-?\d+", raw) else float(raw)
    return raw

FILE:src/sldb/store/graph/backend/evaluate.py
"""Evaluate the small AST of the GO02 subset, keeping the clause and `seen` of the decision."""

from __future__ import annotations

from typing import Any


def evaluate(node: tuple, payload: dict[str, Any]) -> tuple[bool, str, dict[str, Any]]:
    """`(holds, clause, seen)` for one AST node over a payload."""
    tag = node[0]
    if tag == "leaf":
        return _leaf(node, payload)
    if tag == "not":
        return _not(node, payload)
    return _bool(node, payload)


def _leaf(node: tuple, payload: dict[str, Any]) -> tuple[bool, str, dict[str, Any]]:
    holds, seen = node[4](payload)
    return holds, node[3], seen


def _not(node: tuple, payload: dict[str, Any]) -> tuple[bool, str, dict[str, Any]]:
    holds, clause, seen = evaluate(node[3], payload)
    return not holds, clause, seen


def _bool(node: tuple, payload: dict[str, Any]) -> tuple[bool, str, dict[str, Any]]:
    tag, _, _, clause, left, right = node
    left_result = evaluate(left, payload)
    if tag == "and" and not left_result[0]:
        return left_result
    if tag == "or" and left_result[0]:
        return left_result
    return _combine(tag, clause, left_result, evaluate(right, payload))


def _combine(tag: str, clause: str, left: tuple, right: tuple) -> tuple[bool, str, dict[str, Any]]:
    seen = {**left[2], **right[2]}
    if tag == "and":
        return right if not right[0] else (True, clause, seen)
    return right if right[0] else (False, clause, seen)

FILE:src/sldb/store/graph/backend/eval.py
"""One `eval` finding: fill the subject's braces, parse, evaluate, keep the GO02 shape."""

from __future__ import annotations

from typing import Any

from sldb.store.graph.backend.evaluate import evaluate
from sldb.store.graph.backend.parser import parse
from sldb.store.query_engine.where_subject import fill_braces


def evaluate_finding(predicate: Any, payload: dict[str, Any], node: str) -> dict[str, Any]:
    """The finding for this payload; a missing or non-scalar brace makes it false."""
    text = predicate if isinstance(predicate, str) else str(predicate)
    filled, complete = fill_braces(text, payload)
    holds, clause, seen = evaluate(parse(filled, text), payload)
    return {"node": node, "holds": _holds(holds and complete), "clause": clause, "seen": seen}


def _holds(value: bool) -> str:
    return "true" if value else "false"

FILE:src/sldb/store/graph/backend/networkx_backend.py
"""The networkx implementation of the `GraphBackend` seam.

It wraps `sldb.store.graph.analysis` unchanged: every operation receives the composed index
and returns what the analysis returned. The index is kept private; callers only ask for an
operation by name. `eval` implements the GO02 subset without paths, over a payload or an
`export_id` resolved through the projection.

The seam exists so that a future engine (Kùzu, Neo4j, Datalevin) can sit behind the same three
methods. See `docs/architecture/graph-backend.md`.
"""

from __future__ import annotations

from typing import Any, Callable

from sldb.store.graph import analysis
from sldb.store.graph.backend.eval import evaluate_finding

_OPERATIONS: dict[str, Callable[..., Any]] = {
    "path": analysis.path_between,
    "paths": analysis.paths_between,
    "cycles": analysis.cycles,
    "order": analysis.topological_order,
    "layers": analysis.layers,
    "components": analysis.components,
    "islands": analysis.islands,
    "isolated": analysis.isolated,
    "central": analysis.central,
    "similar": analysis.similar_to,
}


class NetworkXBackend:
    """The current engine: `sldb.store.graph.analysis` over the composed edge index."""

    def __init__(self) -> None:
        self._index: Any = None
        self._projection: dict[str, dict[str, Any] | None] | None = None

    def load(self, index: Any, projection: dict[str, dict[str, Any] | None] | None = None) -> None:
        """Keep the composed index and the optional export-id projection; return nothing."""
        self._index = index
        self._projection = projection
        return None

    def analyze(self, op: str, **args: Any) -> Any:
        """Run one analysis operation with the arguments the analyses already take."""
        if self._index is None:
            raise RuntimeError("GraphBackend.analyze called before load")
        operation = _OPERATIONS.get(op)
        if operation is None:
            raise ValueError(f"Unknown graph operation: {op}")
        return operation(self._index, **args)

    def eval(self, predicate: Any, subject: Any = None) -> list[dict[str, Any]]:
        """Evaluate a parsed predicate on a payload or export id, or over the projection."""
        if subject is None:
            return self._eval_domain(predicate)
        payload, node = self._subject(subject)
        return [evaluate_finding(predicate, payload, node)]

    def _subject(self, subject: Any) -> tuple[dict[str, Any], str]:
        if isinstance(subject, str):
            return self._projected(subject), subject
        if isinstance(subject, dict):
            return subject, str(subject.get("id") or subject.get("name") or "")
        raise TypeError("el sujeto de eval es un payload (dict) o un export_id (str)")

    def _projected(self, export_id: str) -> dict[str, Any]:
        if self._projection is None or export_id not in self._projection:
            raise ValueError(f"sin proyección para {export_id}")
        return self._projection[export_id] or {}

    def _eval_domain(self, predicate: Any) -> list[dict[str, Any]]:
        if not self._projection:
            return []
        return [evaluate_finding(predicate, payload or {}, export_id) for export_id, payload in sorted(self._projection.items())]

FILE:src/sldb/store/graph/executor.py
"""Structured query execution over the edge index's _out/_in maps."""

from __future__ import annotations

from collections import deque

from sldb.store.graph.edge_filter import filtered_edges
from sldb.store.exceptions import SLDBGraphArgumentError
from sldb.store.graph.facet_match import matches_filters
from sldb.store.graph.payload_match import unprojected_fields
from sldb.store.graph.node_view import GraphNode


def execute_query(index, query) -> list[GraphNode]:
    """Run a StructuredQuery against an edge index; returns matching nodes. A `payload` filter
    reads the projection the shards hold (nothing is re-extracted); one naming a field no model
    projects is rejected (SLDBGraphArgumentError naming the field)."""
    _check_payload_fields(index, query.filters)
    matches: list[GraphNode] = []
    for node_id in candidate_ids(index, query.scope):
        node = index.nodes[node_id]
        if matches_filters(node, query.filters):
            matches.append(_node_view(index, node, query.relations))
    return matches


def _check_payload_fields(index, filters) -> None:
    missing = unprojected_fields(getattr(index, "payload_fields", {}), filters)
    if missing:
        raise SLDBGraphArgumentError(f"payload filter on {', '.join(repr(f) for f in missing)}: not projected into the graph (a dict or a list of non-scalars, outside the model's __indexed__, or not a field of any model).")


def candidate_ids(index, scope) -> list[str]:
    """The node ids the scope admits, sorted for determinism."""
    if scope is None:
        return sorted(index.nodes)
    if scope.descendant_of:
        return sorted(descendants(index, scope.descendant_of))
    if scope.ancestor_of:
        return sorted(ancestors(index, scope.ancestor_of))
    if scope.node_id_prefix:
        return sorted(n for n in index.nodes if n.startswith(scope.node_id_prefix))
    return sorted(index.nodes)


def descendants(index, root: str) -> set[str]:
    """Nodes reachable from `root` following outgoing edges, excluding `root` itself."""
    visited = {root}
    queue = deque([root])
    while queue:
        for edge in index.edges_from(queue.popleft()):
            if edge.target not in visited:
                visited.add(edge.target)
                queue.append(edge.target)
    visited.discard(root)
    return visited


def ancestors(index, root: str) -> set[str]:
    """Nodes that reach `root` following incoming edges, excluding `root` itself."""
    visited = {root}
    queue = deque([root])
    while queue:
        for edge in index.edges_to(queue.popleft()):
            if edge.source not in visited:
                visited.add(edge.source)
                queue.append(edge.source)
    visited.discard(root)
    return visited


def _node_view(index, node, relation_filters) -> GraphNode:
    return GraphNode(id=node.id, node_type=node.node_type, semantics=node.semantics, facets=node.facets, edges=filtered_edges(index, node.id, relation_filters))

FILE:src/sldb/store/graph/payload_match.py
"""Conditions on the `payload` facet (GO04): a document node's projected fields.

The facet's operators keep `facet_match`'s meaning, with what a projection adds: on a null (an
absent field) only `is_null` / `is_not_null` decide, the others are false; on a list,
`contains` is membership, `eq` / `ne` compare the whole list (Python equality, no coercion),
`gt` / `lt` / `starts_with` are false, `is_null` false and `is_not_null` true. A comparison
Python cannot order (`"a" > 1`) is false, not an error. Only document nodes carry the facet:
any other node matches no payload filter.
"""

from __future__ import annotations

from sldb.store.edge_index.node_ids import kind
from sldb.store.graph.facet_match import condition_matches, ordered_compare

PAYLOAD = "payload"
_NULL_OPS = ("is_null", "is_not_null")


def payload_matches(node, facet_filter) -> bool:
    """Whether a document node's projection satisfies every condition of the filter."""
    if kind(node.id) != "document":
        return False
    return all(payload_condition(node.payload, condition) for condition in facet_filter.conditions)


def payload_condition(payload: dict, condition) -> bool:
    """One FieldCondition over a projected payload."""
    if condition.op in _NULL_OPS:
        return condition_matches(payload, condition)
    actual = payload.get(condition.field)
    if actual is None or (isinstance(actual, list) and condition.op in ("gt", "lt")):
        return False
    try:
        return ordered_compare(actual, condition)
    except TypeError:
        return False


def unprojected_fields(payload_fields: dict[str, list[str]], filters: list) -> list[str]:
    """Fields a payload filter names that no model projects, in the order named."""
    known = {f for fields in payload_fields.values() for f in fields}
    named = [c.field for f in filters if f.facet == PAYLOAD for c in f.conditions]
    return [f for f in dict.fromkeys(named) if f not in known]

FILE:src/sldb/store/query_engine/where_parse.py
"""One grammar for sldb's `--where` predicates: parsed once per query, matched per document.

`compile_where` raises `WherePredicateError` when no evaluator understands the predicate,
so an unparseable expression is a loud error instead of a silent empty result. Predicates
join with ` and ` (outside literals); there is no `or` and no parentheses.
"""

from __future__ import annotations

import re
from typing import Any, Callable

from sldb.store.exceptions import SLDBError
from sldb.store.query_engine.where_literal import LITERAL as _LITERAL
from sldb.store.query_engine.where_lookup import _ABSENT, _lookup
from sldb.store.query_engine.where_literal import LITERAL_NONEMPTY as _LITERAL_NONEMPTY
from sldb.store.query_engine.where_literal import split_outside_literals
from sldb.store.query_engine.where_literal import unquote as _unquote

Predicate = Callable[[Any, Any, Any], bool]  # (doc, resolve_model_ref, pythonpath) -> bool


class WherePredicateError(ValueError, SLDBError):
    """A --where predicate that no evaluator can parse."""

    def __init__(self, expression: str):
        super().__init__(f"no evaluator understands the predicate: {expression!r}")


def compile_where(expression: str) -> Predicate:
    """Parses one --where predicate, or several joined by ` and ` (all must hold); raises
    WherePredicateError naming the first part no evaluator parses."""
    predicates = [_compile_one(part) for part in split_outside_literals(expression.strip(), r"\s+and\s+")]
    if len(predicates) == 1:
        return predicates[0]
    return lambda doc, resolve_model_ref, pythonpath: all(p(doc, resolve_model_ref, pythonpath) for p in predicates)


def _compile_one(expression: str) -> Predicate:
    text = expression.strip()
    for pattern, build in _EVALUATORS:
        m = pattern.fullmatch(text)
        if m:
            return build(m)
    raise WherePredicateError(text)


def _build_has(m: re.Match) -> Predicate:
    field = m.group(1)

    def check(doc: Any, resolve_model_ref: Any, pythonpath: Any) -> bool:
        return field in doc.payload and doc.payload[field] not in (None, "")

    return check


def _build_nonempty(m: re.Match) -> Predicate:
    field = m.group(1)

    def check(doc: Any, resolve_model_ref: Any, pythonpath: Any) -> bool:
        value = _lookup(doc.payload, field)
        return value is not None and not (isinstance(value, (str, list, dict, tuple, set)) and len(value) == 0)

    return check


def _build_contains(m: re.Match) -> Predicate:
    needle, field = _unquote(m.group(1)), m.group(2)

    def check(doc: Any, resolve_model_ref: Any, pythonpath: Any) -> bool:
        value = _lookup(doc.payload, field)
        return needle in value if isinstance(value, (list, str)) else False

    return check


def _build_regex(m: re.Match) -> Predicate:
    field, pattern = m.group(1), _unquote(m.group(2))

    def check(doc: Any, resolve_model_ref: Any, pythonpath: Any) -> bool:
        target = doc.name if field == "doc" else str(_lookup(doc.payload, field, ""))
        return re.search(pattern, target) is not None

    return check


def _build_model(m: re.Match) -> Predicate:
    base = m.group(1)

    def check(doc: Any, resolve_model_ref: Any, pythonpath: Any) -> bool:
        from sldb.store.query_engine.structural import model_in_family

        return model_in_family(doc.model_type, base)

    return check


def _build_compare(m: re.Match) -> Predicate:
    field, op, raw = m.group(1), m.group(2), m.group(3)
    expected: Any = _unquote(raw) if raw.startswith('"') else float(raw)

    def check(doc: Any, resolve_model_ref: Any, pythonpath: Any) -> bool:
        if raw.startswith('"') and _lookup(doc.payload, field, _ABSENT) is _ABSENT:
            return False  # an absent field matches neither "=" nor "!=" (string literals)
        return _apply_op(_lookup(doc.payload, field), op, expected)

    return check


def _apply_op(value: Any, op: str, expected: Any) -> bool:
    if op == "=": return value == expected
    if op == "!=": return value != expected
    if op == ">=": return value >= expected
    if op == "<=": return value <= expected
    return False


# same order the old evaluator tried them: has, in, regex, model family, comparison;
# nonempty(f) is has(f) that also rejects [] and {}
_EVALUATORS = [
    (re.compile(r"has\(([^)]+)\)"), _build_has),
    (re.compile(r"nonempty\(([^)]+)\)"), _build_nonempty),
    (re.compile(_LITERAL_NONEMPTY + r"\s+in\s+([A-Za-z_][\w.]*)"), _build_contains),
    (re.compile(r'([A-Za-z_][\w.]*)\s*~\s*' + _LITERAL_NONEMPTY), _build_regex),
    (re.compile(r"model\s*<=\s*([A-Za-z_][\w.]*)"), _build_model),
    (
        re.compile(r'([A-Za-z_][\w.]*)\s*(=|!=|>=|<=)\s*(' + _LITERAL + r'|-?\d+(?:\.\d+)?)'),
        _build_compare,
    ),
]

FILE:src/sldb/store/query_engine/where_subject.py
"""A `--where` predicate on a plain payload, with `{field}` filled from a subject.

An edge's condition names fields of the document it is tested on, and may name fields of a
subject in braces (`capacity >= {party_size}`). Braces are filled only outside literals,
each with the subject's value written as a literal; a brace whose field the subject lacks,
or holds a non-scalar, makes the condition not hold, as an absent field does.
"""

from __future__ import annotations

import re
from types import SimpleNamespace
from typing import Any

from sldb.store.query_engine.where_literal import LITERAL, scalar_literal
from sldb.store.query_engine.where_parse import compile_where

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

    `doc ~ "..."` reads `name`; `model <= X` never holds, a payload carries no model class.
    An empty expression always holds. Raises WherePredicateError when it does not parse.
    """
    if not expression.strip():
        return True
    filled, complete = fill_braces(expression, payload if subject is None else subject)
    predicate = compile_where(filled)
    return complete and predicate(SimpleNamespace(payload=payload, name=name, model_type=None), None, None)

FILE:src/sldb/store/query_engine/structural_queries.py
from __future__ import annotations

import fnmatch
import re
from pathlib import Path

from sldb.store.query_engine.structural import _model_scope_docs
from sldb.store.query_engine.where_parse import compile_where
from sldb.store.query_engine.store_prefix import split_store, with_store


def glob_structural(
    store_path: Path, pattern: str, resolve_model_ref, pythonpath: str | None = None
) -> list[str]:
    """Matches structural addresses against a glob pattern."""
    return StructuralQueryEngine.glob_structural(store_path, pattern, resolve_model_ref, pythonpath)

def find_structural(
    store_path: Path, address: str, where: str, resolve_model_ref, pythonpath: str | None = None,
) -> list[str]:
    """Finds documents matching a structural scope and filter."""
    return StructuralQueryEngine.find_structural(store_path, address, where, resolve_model_ref, pythonpath)

class StructuralQueryEngine:
    """Engine for processing glob and find queries on structural nodes."""

    @classmethod
    def glob_structural(
        cls, store_path: Path, pattern: str, resolve_model_ref, pythonpath: str | None = None
    ) -> list[str]:
        """Matches structural addresses against a glob pattern."""
        store, pattern = split_store(pattern)
        match = re.fullmatch(r"st\.\{([^{}+]+)(\+)?\}\.([^.]+)(?:\.(.+))?", pattern)
        if not match:
            return []
        model_name, recursive_flag, doc_pattern, field_pattern = match.groups()
        docs = _model_scope_docs(store_path, model_name, bool(recursive_flag), resolve_model_ref, pythonpath, store)
        base_scope = with_store(store, f"st.{{{model_name}{'+' if recursive_flag else ''}}}")
        return cls._glob_docs(docs, doc_pattern, field_pattern, base_scope)

    @classmethod
    def _glob_docs(cls, docs, doc_pattern: str, field_pattern: str | None, base_scope: str) -> list[str]:
        results: list[str] = []
        for doc in docs:
            if not fnmatch.fnmatch(doc.name, doc_pattern):
                continue
            if field_pattern is None:
                results.append(f"{base_scope}.{doc.name}")
                continue
            cls._glob_fields(doc, field_pattern, base_scope, results)
        return sorted(results)

    @classmethod
    def _glob_fields(cls, doc, field_pattern: str, base_scope: str, results: list[str]) -> None:
        for field_name in sorted(doc.payload.keys()):
            if fnmatch.fnmatch(field_name, field_pattern):
                results.append(f"{base_scope}.{doc.name}.{field_name}")

    @classmethod
    def find_structural(
        cls, store_path: Path, address: str, where: str, resolve_model_ref, pythonpath: str | None = None,
    ) -> list[str]:
        """Finds documents matching a structural scope and filter."""
        store, address = split_store(address)
        match = re.fullmatch(r"st\.\{([^{}+]+)(\+)?\}", address)
        if not match:
            return []
        return cls._find_docs(match, store_path, where, resolve_model_ref, pythonpath, store)

    @classmethod
    def _find_docs(cls, match, store_path: Path, where: str, resolve_model_ref, pythonpath: str | None, store: str | None = None) -> list[str]:
        model_name, recursive_flag = match.groups()
        docs = _model_scope_docs(store_path, model_name, bool(recursive_flag), resolve_model_ref, pythonpath, store)
        base_scope = with_store(store, f"st.{{{model_name}{'+' if recursive_flag else ''}}}")
        predicate = compile_where(where)  # once per query; unparseable predicates raise
        return sorted(
            f"{base_scope}.{doc.name}"
            for doc in docs
            if predicate(doc, resolve_model_ref, pythonpath)
        )

FILE:src/sldb/api/where.py
"""`--where` as a library: test one predicate against a plain payload, tracked or not."""

from __future__ import annotations

from typing import Any

from sldb.store.query_engine.where_subject import payload_matches


def where_matches(expression: str, payload: dict[str, Any], subject: dict[str, Any] | None = None) -> bool:
    """Whether a `--where` predicate holds on `payload` (the grammar of `sldb find --where`).

    Args:
        expression: Predicates joined by ` and `: `has(f)`, `nonempty(f)`, `"x" in f`,
            `f ~ "re"`, `f = "s"`, `f >= 3`, ...; empty always holds.
        payload: The fields the predicate reads; need not belong to a tracked document.
        subject: Fills `{field}` placeholders (default: `payload`). A placeholder the subject
            lacks, or holds as a list or dict, makes the expression not hold.

    Raises:
        WherePredicateError: No evaluator parses some part of the expression.
    """
    return payload_matches(expression, payload, subject)

FILE:src/sldb/api/edges/edges_holding.py
"""Edges whose condition holds for a subject: the graph read as a state machine."""

from __future__ import annotations

from pathlib import Path
from typing import Any, Iterable

from sldb.api.edges.edge_reading import edges_from
from sldb.store.models import EdgeRecord
from sldb.store.query_engine.where_subject import payload_matches


def edges_holding(store: str | Path | None, export_id: str, subject: dict[str, Any], relation: str | None = None, include_linked: bool = True, exclude_tags: Iterable[str] = ()) -> list[EdgeRecord]:
    """The edges leaving `export_id` whose condition holds on `subject`.

    Each edge's condition (its own, else its relation type's) is a `--where` predicate read on
    the subject's fields, `{field}` filled from the subject too; an edge without a condition
    always holds. To test a condition on another document (an edge's target, say) with the
    subject in braces, use `where_matches(condition, that_payload, subject)`.

    Args:
        store: The store (path, alias, or None to discover it).
        export_id: The node the edges leave (`Model:name`), e.g. the state a task is in.
        subject: The payload the conditions read; need not be a tracked document's.
        relation, include_linked, exclude_tags: As in `edges_from`.

    Raises:
        WherePredicateError: An edge's condition does not parse.
    """
    edges = edges_from(store, export_id, relation, include_linked, exclude_tags)
    return [e for e in edges if payload_matches(e.metadata.get("condition") or "", subject)]

FILE:src/sldb/cli/parsers/find.py
from __future__ import annotations
import argparse

def add_find_commands(s: argparse._SubParsersAction) -> None:
    p = s.add_parser("find", help="Unified semantic + physical retrieval.", epilog="Typical shapes:\n  sldb find roadmap --in physical --type doc")
    p.add_argument("term", help="Resource term, semantic tag, or physical token")
    p.add_argument("--in", dest="search_in", choices=("semantic", "physical", "both"), default="both", help="Use `physical` for names, paths, section titles, and field addresses")
    for f in ("--global", "--regex", "--fuzzy", "--rebuild"):
        p.add_argument(f, action="store_true", dest="global_scope" if f == "--global" else None)
    p.add_argument("--type", choices=("all", "store", "model", "doc", "section", "field"), default="all")
    p.add_argument("--select", help="Comma-separated projection fields")
    p.add_argument("--where", help="Filter expression")
    _add_common(p)

def _add_common(p):
    p.add_argument("--store", help="Store path")
    p.add_argument("--pythonpath", help="Project path")
    p.add_argument("--format", choices=("text", "json", "yaml"), default="text")

FILE:src/sldb/cli/commands/find.py
from __future__ import annotations
from typing import Any
from sldb.cli.graph_ops import iter_search_records, search_records, SearchRecord
from sldb.api.records.record_filters import RecordFilters
from sldb.cli.commands.find_format import FindFormatter
from sldb.store.query_engine.where_parse import compile_where

class FindCLI:
    """Unified semantic + physical retrieval."""

    def run(self, args: Any) -> int:
        """Run the find command."""
        if args.where: compile_where(args.where)  # once per query: unparseable predicates raise
        matched = self._get_matches(args)
        if args.where:
            matched = self._apply_filters(matched, args)
        return FindFormatter().format_output(matched, args)

    def _get_matches(self, args: Any) -> list[SearchRecord]:
        rebuild = getattr(args, "rebuild", False)
        records = iter_search_records(args.store, args.pythonpath, include_linked=args.global_scope, rebuild=rebuild)
        kinds = {args.type} if args.type != "all" else None
        return search_records(records, args.term, search_in=args.search_in, regex=args.regex, fuzzy=args.fuzzy, kinds=kinds)

    def _apply_filters(self, matched: list[SearchRecord], args: Any) -> list[SearchRecord]:
        filters = RecordFilters(args.pythonpath)
        return [r for r in matched if filters.matches(r, args.where)]

FILE:src/sldb/cli/commands/find_filter.py
import re
from typing import Any

from sldb.cli.commands.find_proxy import _RuntimeDocProxy
from sldb.cli.graph_ops import SearchRecord
from sldb.cli.model_utils import resolve_model_ref
from sldb.store.query_engine.filter import _where_matches as core_where_matches

def _model_proxy(record: SearchRecord) -> type:
    class _Proxy:
        __module__ = ""

    _Proxy.__name__ = record.model_name or "Model"
    return _Proxy

def _where_matches_doc(record: SearchRecord, expression: str, pythonpath: str | None) -> bool:
    runtime_doc = _RuntimeDocProxy(  # `sldb.<key>`: the provenance block is addressable like a field
        payload={**record.payload, "sldb": record.provenance or {}}, name=record.doc_name or record.name, model_type=_model_proxy(record)
    )
    return core_where_matches(runtime_doc, expression, resolve_model_ref, pythonpath) # type: ignore[arg-type]

def _where_matches_field(record: SearchRecord, expression: str) -> bool:
    data = {"value": record.value, "doc": record.doc_name, "model": record.model_name, "field": record.field_path, "path": record.path, "owning_section": record.owning_section or ""}
    if expression.startswith("has("): return _where_matches_field_has(data, expression)
    for op in ("=", "!="):
        if op in expression: return _where_matches_field_op(data, expression, op)
    return False

def _where_matches_field_has(data: dict, expression: str) -> bool:
    key = expression[4:-1]
    return key in data and data[key] not in (None, "", [], {})

def _where_matches_field_op(data: dict, expression: str, op: str) -> bool:
    left, right = [part.strip() for part in expression.split(op, 1)]
    expected = right[1:-1] if right.startswith('"') and right.endswith('"') else right
    actual = data.get(left)
    return (str(actual) == expected) if op == "=" else (str(actual) != expected)

def _where_matches_section(record: SearchRecord, expression: str) -> bool:
    if expression.startswith("title ~ "):
        return re.search(expression.split("~", 1)[1].strip().strip('"'), record.title or "") is not None
    contains_match = re.fullmatch(r'"([^"]+)"\s+in\s+(about|breadcrumbs|semantic_tags)', expression)
    if contains_match: return _where_matches_section_contains(record, contains_match)
    if expression.startswith("path = "): return record.path == expression.split("=", 1)[1].strip().strip('"')
    return True

def _where_matches_section_contains(record: SearchRecord, contains_match: Any) -> bool:
    needle, field = contains_match.groups()
    if field == "about": return needle in (record.about or [])
    if field == "breadcrumbs": return needle in record.payload.get("breadcrumbs", [])
    if field == "semantic_tags": return needle in record.semantic
    return False

def where_matches(record: SearchRecord, expression: str, pythonpath: str | None) -> bool:
    if record.kind == "doc": return _where_matches_doc(record, expression, pythonpath)
    if record.kind == "field": return _where_matches_field(record, expression)
    if record.kind == "section": return _where_matches_section(record, expression)
    return True

FILE:src/sldb/cli/commands/graph.py
"""`sldb graph` handlers: thin printing wrappers over `sldb.api`'s graph functions."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from sldb.api.graph import (
    collect_neighborhood,
    collect_neighborhood_by_direction,
    execute_query,
    graph_get,
    graph_list,
    ingest_sldb,
    save_graph,
    snapshot_load,
    snapshot_save,
)
from sldb.cli.commands.graph_analysis import GraphAnalysisCLI
from sldb.store.graph.language import StructuredQuery


class GraphCLI:
    """Noun-first surface of the graph layer."""

    def __init__(self, backend: Any = None) -> None:
        self.backend = backend

    def run(self, args: Any) -> int:
        handlers = {
            "get": self._get,
            "list": self._list,
            "query": self._query,
            "neighborhood": self._neighborhood,
            "snapshot": self._snapshot,
            "ingest-sldb": self._ingest_sldb,
        }
        handler = handlers.get(args.graph_command)
        return handler(args) if handler else GraphAnalysisCLI(backend=self.backend).run(args)

    def _get(self, args: Any) -> int:
        node = graph_get(args.store, args.node, not args.local, args.exclude_tag)
        if node is None:
            return 1
        print(json.dumps(node.model_dump(), indent=2, ensure_ascii=False))
        return 0

    def _list(self, args: Any) -> int:
        print(json.dumps(graph_list(args.store, not args.local, args.exclude_tag), indent=2, ensure_ascii=False))
        return 0

    def _query(self, args: Any) -> int:
        query = StructuredQuery.model_validate(json.loads(Path(args.query_file).read_text(encoding="utf-8")))
        nodes = execute_query(args.store, query, not args.local, args.exclude_tag)
        print(json.dumps([n.model_dump() for n in nodes], indent=2, ensure_ascii=False))
        return 0

    def _neighborhood(self, args: Any) -> int:
        if args.direction == "both":
            ids = collect_neighborhood(args.store, [args.node], args.depth, not args.local, args.exclude_tag)
        else:
            ids = collect_neighborhood_by_direction(args.store, {args.node}, args.depth, args.direction, not args.local, args.exclude_tag)
        print(json.dumps(sorted(ids), indent=2, ensure_ascii=False))
        return 0

    def _snapshot(self, args: Any) -> int:
        return {"save": self._snapshot_save, "load": self._snapshot_load}[args.snapshot_command](args)

    def _snapshot_save(self, args: Any) -> int:
        snapshot_save(args.store, args.output, not args.local, args.exclude_tag)
        print(f"Saved graph snapshot to {args.output}")
        return 0

    def _snapshot_load(self, args: Any) -> int:
        print(json.dumps(snapshot_load(args.input).model_dump(mode="json"), indent=2, ensure_ascii=False))
        return 0

    def _ingest_sldb(self, args: Any) -> int:
        payload = json.loads(Path(args.input).read_text(encoding="utf-8"))
        save_graph(ingest_sldb(payload), args.output)
        print(f"Saved graph snapshot to {args.output}")
        return 0

FILE:docs/architecture/rules-language.md
# Lenguaje de reglas de sldb

Estado (2026-11-04): contrato de semántica del nodo GO02 del plan
`desk/drawer/plans/grafo-operable`. Fija la gramática, los caminos, la semántica
trivaluada, el formato de explicación, el hash de contrato y la firma de evaluación del
lenguaje único de predicados de sldb. El evaluador lo implementa GO05 sobre el backend de
GO03 y la proyección de GO04; hasta entonces los ejemplos de este documento viven como
tests de especificación marcados `xfail` en `tests/test_rules_language_spec.py`.

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
  semántica de búsqueda que el `~` actual de `where_parse`: `re.search`, no anclaje
  implícito. Un patrón inválido es error de parseo: `WherePredicateError`, la excepción
  existente de `sldb.store.query_engine.where_parse`.
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

La columna «nuevo» es la construcción del lenguaje de este documento. Ninguna de esas
construcciones usa `eq`, `ne`, `gt`, `lt`, `contains`, `starts_with`, `is_null` ni
`is_not_null` como nombres de operador.

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
  `{"nodes": {id: {"model": ..., "payload": ...}}, "edges": [{"source", "type", "target",
  "field"?}]}`. El objeto real es el índice compuesto / `GraphBackend` de GO03.
- **H3. Sujeto de `eval`.** Los tests pasan como sujeto el identificador `Model:name` del
  nodo. GO03 admite además el payload y el `export_id` con proyección.
- **H4. `incomplete` por store no disponible.** Los tests marcan la arista con
  `"unavailable": True`; el índice real resolverá esa condición al abrir el store enlazado.
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
  por ruta de `where_lookup` (`sldb.authority`, `tasks.0.title`) para un paso de campo.
- **H10. Clave del envelope.** El contrato fija que la explicación viaja en el envelope,
  pero no el nombre exacto de la clave; GO06 lo fija al definir `rules explain`.
- **H11. Error por `__contract__` vacío.** Los tests esperan `ValueError`; el contrato solo
  dice «error al cargar el modelo».

FILE:docs/architecture/graph-backend.md
# GraphBackend: the seam under every graph analysis

Estado (2026-11-05): contrato del nodo GO03 del plan
`desk/drawer/plans/grafo-operable` (gate G_SEAM). Fija la costura `GraphBackend` sobre
networkx. Cualquier motor futuro —Kùzu, Neo4j, Datalevin— entra detrás de esta costura; las
reglas y los comandos no lo ven. La semántica de los predicados vive en
[`rules-language.md`](rules-language.md); la proyección real llega en GO04 y el evaluador
completo en GO05.

## El protocolo

`src/sldb/store/graph/backend/protocol.py` declara tres operaciones:

```python
load(index, projection) -> None
eval(predicate, subject=None) -> list[finding]
analyze(op, **args) -> resultado
```

- **`load`** guarda en la instancia el índice compuesto y la proyección. El índice es el
  objeto que devuelve `sldb.store.edge_index.compose.compose_edge_index`: nodos y aristas ya
  resueltos. **Compose queda fuera del backend**: él lo produce y se lo entrega a `load`.
  Devuelve `None`.
- **`eval`** evalúa un predicado sobre un sujeto. El sujeto es un payload (`dict`) o un
  `export_id` (`str`). Si es un `export_id`, se lee la proyección cargada; sin proyección o
  sin ese id, `eval` levanta `ValueError("sin proyección para <id>")`. En GO03 la proyección
  real siempre es `None` (la produce GO04), así que los tests pasan el sujeto como payload.
- **`analyze`** responde una pregunta de grafo completo con los argumentos que las
  operaciones ya reciben. Hoy son las diez de `sldb.api.graph.analyze`: `path`, `paths`,
  `cycles`, `order`, `layers`, `components`, `islands`, `isolated`, `central` y `similar`;
  las seis de la CLI (`path`, `cycles`, `order`, `components`, `central`, `similar`) son el
  subconjunto que el contrato del nodo nombra.

El backend **nunca expone su grafo interno**. Se guarda en un atributo privado y las
operaciones lo usan dentro; no hay accesor público ni fuga del `MultiDiGraph` de networkx.

La implementación actual, `NetworkXBackend`, envuelve `sldb.store.graph.analysis` sin
cambiar ninguna respuesta.

## eval en GO03

Acepta el subconjunto de GO02 **sin caminos**: `has`, `nonempty`, `in`, `~`, `model <=`,
comparaciones `= != < <= > >=`, `and`/`or`/`not`, paréntesis y sustitución `{campo}` desde
el payload del sujeto. Reutiliza `where_lookup` para las rutas de campo,
`where_subject.fill_braces` para la sustitución y `WherePredicateError` para lo que no
parsea.

Un predicado con camino —`any(...)`, `all(...)`, `none(...)`, `count(...)`, `rel:<tipo>`,
`^campo`, pasos con `+`— levanta `NotImplementedError` hasta GO05.

Cada resultado es un finding de la forma fijada en `rules-language.md` §4 y §6:

```json
{"node": "Task:a", "holds": "true", "clause": "status = \"open\"", "seen": {"status": "open"}}
```

## Selección por store.yaml

`.sldb/store.yaml` puede declarar:

```yaml
graph_backend: networkx
```

- **Ausente**: se usa `networkx` (también si el store no tiene declaración).
- **`"networkx"`**: aceptado.
- **Cualquier otro valor**: el store falla al cargar la declaración con el mensaje exacto
  `graph_backend <valor> no admitido; admitidos: ["networkx"]`.

La resolución vive en `src/sldb/api/graph/analyze.py` (`backend_for`, que llama a
`declared_graph_backend` en `src/sldb/api/stores/store_declaration.py` y pasa el nombre a
`make_backend` en `src/sldb/store/graph/backend/__init__.py`). Así el paquete `store` no
importa nada de `sldb.api`.

Para tests y para futuros motores, un llamador de Python puede inyectar una instancia:
`graph_path(..., backend=motor)`, `GraphAnalysisCLI(backend=motor)` o
`GraphCLI(backend=motor)`. `store.yaml` sigue siendo el selector de producción.

## Regla de la costura

Toda capacidad de análisis de grafo entra por `analyze`; toda evaluación de predicados entra
por `eval`; toda lectura de un índice entra por `load`. Un motor nuevo implementa las tres
operaciones y nada más cambia: ni las reglas, ni la API, ni la CLI conocen networkx.

## La proyección del payload (GO04)

Estado (2026-11-06): contrato del nodo GO04. `load` lee el índice de aristas; desde la
versión 5 (`EDGE_INDEX_VERSION`) cada nodo de documento lleva, persistidos en su shard,
cuatro campos de primer nivel de `EdgeNodeRecord` (no van en `facets`, que sigue siendo solo
de lectura). Los demás nodos (secciones, modelos, campos, tags...) los dejan vacíos y el
shard no los escribe.

- `payload`: mapa plano campo → valor con los campos de nivel superior del payload extraído
  cuyo valor es escalar (str, int, float, bool) o lista de escalares (incluida la vacía). Si
  el modelo declara `__indexed__`, exactamente esos nombres; un nombre ausente en el payload
  de un documento se omite.
- `field_hashes`: el mapa completo de `DocumentEntry.field_hashes` (todos los campos, no solo
  los proyectados).
- `source_hash`: el `hash_c` de la `DocumentEntry`.
- `contract_signature`: sha256 del JSON canónico (claves ordenadas, UTF-8, sin espacios) de
  `{fields, references, containment, compositions}`: todos los nombres de campo del modelo
  tras la herencia y los nombres de `__references__`, `__containment__` y `__compositions__`,
  ordenados; un atributo ausente aporta la lista vacía. Solo nombres.

### Omisiones

- Un campo cuyo valor es un diccionario (un bloque `dict`, un submodelo) o una lista con algún
  elemento no escalar (una tabla) no se proyecta: se lee con `--where` o con el documento.
- Un campo nulo no se proyecta: la extracción lo descarta (`exclude_none`), así que en la
  proyección está ausente, igual que un campo que el documento no tiene.
- Los valores son los del payload en modo JSON: una fecha o un enum llegan como cadena.
- Un modelo que no se puede cargar al reconstruir deja `payload` vacío y `contract_signature`
  en `""`; abrir el store no falla.
- Las relaciones, los tipos de relación y las anclas no son nodos de documento: no llevan
  proyección.
- `__indexed__` se valida al cargar el modelo (`resolve_model_ref`): un nombre que no es campo
  del modelo tras la herencia, o cuyo tipo declarado no es escalar ni lista de escalares, es
  `SLDBModelError` con el modelo y el campo. Cuentan como escalares los tipos cuya forma JSON
  es escalar (enums, fechas, UUID, `Literal` de escalares).
- `__indexed__` no entra en `contract_signature` (el contrato fija sus cuatro claves): cambiarlo
  en un modelo con documentos ya indexados reproyecta un documento cuando se reconstruye su
  shard (su texto cambia o la reconstrucción es completa), no antes.

### Staleness

`EdgeIndex.stale` nombra un documento cuando su shard falta, se construyó desde otro hash o
bajo otra `EDGE_INDEX_VERSION` (un shard de versión 4 queda stale al abrir y entra al dirty
set; la siguiente escritura o `stores build` lo reconstruye), cuando el texto del archivo ya
no da el `source_hash` del shard (edición fuera de sldb) o cuando la firma del modelo cargado
difiere de la guardada (por ejemplo, un campo nuevo en `__references__`). Las dos últimas se
comprueban en cada lectura del índice (`compose_edge_index` con `model_type_of`, que pasan
`load_edge_index` y `rebuild_edges`), no se guardan con el índice compuesto: ninguna mueve un
shard. El hash de cada archivo se recuerda mientras su mtime y su tamaño no cambien.

### Consulta

`StructuredQuery` filtra sobre la proyección con
`FacetFilter(facet="payload", conditions=[FieldCondition(field=..., op=..., value=...)])`. Se
evalúa sobre lo que dice el shard: nunca se re-extrae un documento. Solo los nodos de documento
tienen la facet; los demás no casan con un filtro `payload`. Sobre un campo ausente (nulo) solo
deciden `is_null` e `is_not_null`; sobre una lista, `contains` es pertenencia, `eq` / `ne`
comparan la lista entera, `gt` / `lt` / `starts_with` dan false, `is_null` false e
`is_not_null` true. `eq` / `ne` usan la igualdad de Python sin coerción (`1 == 1.0`,
`True == 1`); una comparación que Python no puede ordenar da false. Un filtro sobre un campo
que ningún modelo proyecta (diccionario, lista no escalar, fuera de `__indexed__`, o inexistente)
es `SLDBGraphArgumentError` con el nombre del campo; un campo proyectable ausente en todos los
payloads da el conjunto vacío. La lista de campos proyectables por modelo vive en el shard del
modelo (`ModelEdges.projected_fields`) y el índice compuesto la expone en
`EdgeIndex.payload_fields`. Las facets existentes (`identity`, `semantics`, `source`...) no
cambian, y `GraphNode` no gana claves.

FILE:CHANGELOG.md
# Changelog

Version note (2026-09-13, updated 2026-10-18): `pyproject.toml` declares `0.1.12`; it was `0.1.0` while PyPI already had `0.1.1`. Existing entries below are historical development records, not a verified registry release inventory. The product-generation label “v1” is separate from package versioning. No new package version or release is created by this documentation reconciliation.

## 0.1.13 — not released yet (no tag, not on PyPI)

- Transclusión de campos y segmentos ricos de diagramas y vistas en /document/segments (SV03):
  - `sldb.api.segments`:
    - `source_ref.py`: `SourceRef` incorpora el campo opcional `field: str | None = None`.
    - `composition_spec.py`: Soporta `ref: Literal["document", "field", "view", "spec"]`.
    - `composition_piece.py` y `field_segment.py`: incorporan los campos opcionales `projection: dict | None = None` y `table_data: dict | None = None`.
    - `field_ref_resolver.py`: `FieldRefResolver` resuelve referencias `Model:name#campo`, `docs/<Model>/<name>/<campo>` y `docs/<name>/<campo>` devolviendo `{model, doc, path, field, value, payload}`.
    - `segment_enrichment.py`: Enriquecimiento de segmentos con vistas resueltas (`resolve_view` / `evaluate_projection_view`) y tablas estructuradas (`table_data`).
    - `build_document_segments.py`: Inyecta `FieldRefResolver` en `render_with_spans` y enriquece los nodos con `projection` y `table_data`.
  - `sldb.models.structured_doc`: `StructuredNLDoc.compose_field` y `render_payload` aceptan `field_resolver`; cuando `ref == "field"`, resuelve campos remotos emitiendo `CompositionPiece` con `SourceRef(model, doc, path, field)`. Sin resolver inyectado, rinde vacío preservando la pureza del renderizador.
  - Documentación de arquitectura en `docs/architecture/segments-and-transclusion.md`.
  - Suite de tests en `tests/segments/test_field_transclusion_and_diagram_segments.py`.
- Visual notation and projection view resolver, store synchronization, CLI, and serve routes (SV02):
  - `sldb.api.notations`:
    - `notation_view.py`: `resolve_view` and `resolve_documents` resolving glyphs, compartments (`data.attributes`), template/keyword interpolation, edge ordering, UML fragments, and legends.
    - `projection_view.py`: `evaluate_projection_view`, `list_projection_views`, and `save_projection_view` evaluating node where-predicates, relation filters, layout, palette ink, and notation styling.
    - `notation_sync.py`: `sync_palette` and `sync_notation` writing `PaletteDoc`, `NotationDoc`, `GlyphDoc`, `LinkDoc`, and `RelationTypeDoc` into stores without intermediate YAML dependencies.
    - Re-exported in `sldb.api` and `sldb.api.notations`.
  - CLI: `sldb notations (list, sync, view, resolve)` with JSON output and envelope support (`sldb --envelope notations ...`).
  - HTTP serve routes in `sldb serve`: `GET /notations`, `GET /notations/view`, `POST /notations/resolve`, `GET /views/projection`, `GET|POST /views/projection/evaluate`, `POST /views/projection/save`.
  - Documentation updated in `docs/architecture/notations-and-views.md`.
  - Comprehensive test suite in `tests/notations/test_notation_view_and_routes.py`.
- Declaración y edición draft de containment, references, compositions, semantics y authority en modelos (SV04):
  - `sldb.api.create_model` y `ModelSource` aceptan `containment`, `references`, `compositions`, `semantics`, `authority`; validan que los campos referenciados existan y que las composiciones tengan marcador `⸢render•<name>⸥` en template (o lo generan en `default_template`), emitiendo las asignaciones correspondientes en el código Python generado.
  - `describe_model` y `ModelDescription` exponen `containment`, `references`, `compositions`, `semantics_map`, `authority`, `template`, `has_draft`, `draft_path`.
  - `sldb.api.edit_model_metadata` en `sldb.api.model_drafts` edita `__containment__`, `__references__`, `__compositions__`, `__semantics__` y `__authority__` en el `.draft.py` (`.py.temp`) mediante manipulación AST en `metadata_literals.py`, y sincroniza secciones de composiciones en el template.
  - `validate_template_contract` y `check_and_plan` validan coherencia de referencias/containment/compositions contra campos declarados y template, rechazando errores con `SLDBModelEditError`. `promote_model_draft(..., backfill=True)` re-renderiza documentos y reconstruye índices de modelo, semántico y de aristas.
  - Expuesto en CLI (`sldb models metadata edit`, `sldb models validate --promote --backfill`, y flags de creación) y HTTP serve (`POST /models/create`, `POST /models/metadata-edit`, `POST /models/promote` con `backfill`).
  - Documentación de arquitectura en `docs/architecture/model-authoring.md`.
- Visual vocabulary models, palettes and builtin notations absorbed from spec2viz (SV01):
  - 7 models in `sldb.models.notation_models` (re-exported in `sldb.models` and `sldb.api`):
    `SpecDoc`, `SpecNodeDoc`, `NotationDoc`, `GlyphDoc`, `LinkDoc`, `PaletteDoc`, and `ViewDoc`.
    `ViewDoc` adds optional `params: dict` and `sections: list` for GD25 convergence.
  - Submodule `sldb.notations` containing palette (`palette.py`), notation (`notation.py`),
    and styling (`styling.py`) engines, along with builtin `palettes/default.yml` and the 8 builtin
    notations in `builtin/` (`uml-class`, `statechart`, `component`, `deployment`, `uml-sequence`,
    `activity`, `component-view-matrix`, `reflection`).
  - `resolve_model_ref` maps legacy `spec2viz.sldb_models:<Model>` references to
    `sldb.models.notation_models:<Model>` for transparent backwards compatibility with existing stores.
  - Architecture documentation in `docs/architecture/notations-and-views.md`.
- Each document node of the edge index carries its projected payload (GO04): `EdgeNodeRecord`
  gains `payload` (top-level fields holding a scalar or a list of scalars; dicts and lists of
  non-scalars are left out; a model's `__indexed__` picks exactly those names), `field_hashes`
  (the entry's whole map), `source_hash` (hash_c) and `contract_signature` (sha256 of the model's
  field names and `__references__` / `__containment__` / `__compositions__` names), persisted in
  the shard; other nodes leave them empty. `EDGE_INDEX_VERSION` 4 -> 5: a version-4 shard reads
  as stale and is rebuilt on the next write or `stores build`. `EdgeIndex.stale` now also names
  a document whose Markdown was edited outside sldb and one built under another contract
  signature of its model (a new `__references__` entry). `StructuredQuery` filters on
  `FacetFilter(facet="payload", ...)` from the shard, with no re-extraction; a filter on a field
  no model projects raises `SLDBGraphArgumentError` naming it. An `__indexed__` name that is not
  a field or not scalar is `SLDBModelError` when the model loads. Existing queries answer as
  before. Edge index of this repo after `sldb stores build` (`du -sb` of the edges shards root,
  MB = 10^6; shards = `.yaml` files there; 2026-11-06): before (main 804f1ad4) 47.64 MB in
  3116 shards; after (wt/go04 on c1e50419, which tracks more documents) 58.54 MB in 3277 shards.
  `docs/architecture/graph-backend.md` documents the projection and what it leaves out.
- A bare id in a reference field that allows a model also names a document of one of its submodels
  (`depends_on: task-x` with `TaskDoc` allowed names `TaskCodeDoc:task-x`), read from `base_models`
  of the model nodes in the composed index (an inherited model's node takes them from its class, since
  its local index keeps none). The allowed model itself wins; several submodels with that
  name stay `ambiguous`. `resolve_indexed_document` also reads the bases of an inherited model from
  its owner store.
- `sldb.api.resolve_indexed_document(store_path, model, name)` finds `Model:name` when the document is
  tracked under a submodel of `Model` (`TaskDoc:task-x` finds `TaskCodeDoc:task-x`): an instance of a
  submodel is an instance of its bases, read from `base_models` in the model indexes, without importing
  any class. An exact match on the model wins; two submodels tracking the same name raise
  `AmbiguousDocument`. Consumers such as graph_ui resolve ids through it instead of comparing model names.
- The whole-graph analyses sit behind a `GraphBackend` seam (`load`, `eval`, `analyze`).
  `NetworkXBackend` wraps `sldb.store.graph.analysis` unchanged, so the six `sldb graph`
  analyses and the ten `api/graph/analyze.py` functions print the same output as before and
  can be given another backend by Python for tests. A store selects it with
  `graph_backend` in `.sldb/store.yaml`: absent means `networkx`; any other value fails on
  load with `graph_backend <value> no admitido; admitidos: ["networkx"]`. `eval` implements
  the GO02 subset without paths (finding shape in `rules-language.md` §4 and §6); a path
  raises `NotImplementedError` until GO05. `docs/architecture/graph-backend.md` fixes the
  seam: a future engine (Kùzu, Neo4j, Datalevin) enters behind it and the rules never see it.
- A project's declared-edge graph as a library (`sldb.api.edges.project_graph`): `ProjectGraph(root,
  ProjectGraphConfig)` reads the documents of configured surfaces and the files path rules
  classify as nodes, the schema edges and unresolved values of the project's own store from its
  cached composed edge index (`include_linked=False`), and from each document's text what its
  model does not declare (configured mapping fields, fenced YAML blocks, mentions under headings
  or on every line). `edges_from(node)` / `missing_from(node)` read one source alone and give
  what `extraction()` gives for it, so a reader asking about a few documents reads only those.
  The project owns only the configuration (deskops' desk is the first, `deskops/graph/desk_graph.py`).
  New `sldb.api.tracked_documents(store, refs)`: `doc_status` for many references from one read
  of the documents index.
- The store splits in two sibling directories: `.sldb/` (`store.yaml` and `core/`) is
  versioned whole, so that git holds the tree's past, and `.sldb_cache/` (edges, sections,
  semantic shards, graphs, locks; `.sldb/runtime/` until now) is regenerable and ignored
  (`docs/architecture/derived-store-boundary.md`; owner's decision, 2026-10-29).
  `sldb stores init` adds the line `.sldb_cache/` to the root `.gitignore` (idempotent, no
  other line touched); `sldb stores check` reports the error `stores/core_ignored` (exit 1)
  when git ignores `.sldb/core/` or `.sldb/store.yaml` and the alert `stores/cache_not_ignored`
  (exit 0) when the cache is not ignored; `stores build --check` leaves `.sldb_cache/` out of
  its copy. New `sldb stores migrate-layout [--store PATH] [--force]` moves the content of
  `.sldb/runtime/` to `.sldb_cache/` (refusing a non-empty cache unless `--force`, which
  deletes it first), deletes the journal without archiving it, removes `.sldb/runtime/` and
  rewrites the root `.gitignore`: only the lines whose pattern is `.sldb/core` or
  `.sldb/runtime` go, `.sldb_cache/` comes in, everything else stays verbatim. The
  `selfdoc python-sync` graph defaults to `.sldb_cache/graphs/python-source.graph.json`.
- The write journal is retired (2026-11-04): no write through `sldb.api` produces one, and
  `sldb journal show` (and `verify`) print `El journal fue retirado el 2026-11-04; el pasado
  del store se consulta con sldb docs history <doc>.` and exit 0. `sldb.api.journal()` answers
  `[]` and `verify_journal()` a valid, empty report, for importers; `SLDB_JOURNAL_OFF` is gone;
  the `actor` parameters stay (they still stamp a document's provenance where they did).
  `docs/architecture/journal-authority.md` records the decision: the tree is the authority
  and git is its memory.
- Edges can carry their evidence, on request: `sldb edges show --evidence` and
  `sldb.api.edges.edge_evidence.stamp_evidence` add `metadata.evidence` with `ref_hash` (the
  target's `content_hash`, a model's `model_hash`; for a section its document's, flagged
  `ref: document`, since sections have no hash of their own), `contract` (the source model's
  `contract_hash`) and `engine` (`{name, version}`) or, for an authored edge, `actor`
  (`relation_doc:<name>`). No timestamp. Computed on read, so the shards do not change, and
  `ref_hash` is the target's current hash: telling an edge went stale takes a caller that kept
  an earlier evidence to compare.
- `sldb --envelope <command> ...` prints one JSON value per run, `{ok, command, store,
  revision, data, warnings}` or `{ok: false, error: {type: "ns/name", message}, exit}`, and
  exits with a typed code: 0 ok, 1 missing, 2 ambiguous, 3 rejected input, 4 busy, 5 store or
  runtime failure, 6 usage, 70 unexpected (`docs/cli-envelope.md`). Opt-in: without the flag
  the CLI prints and exits as before, because callers parse that output today.
- `sldb stores declare` and `sldb stores build`. A store's source is `.sldb/store.yaml`: the
  models it registers (local, or inherited from a linked store), its links, its predicates,
  the generators that write derived documents (such as `selfdoc python-sync`), the paths
  they write, and `include` rules saying which file is tracked under which model and name.
  The index and the model and document indexes are rebuilt from it by `stores build`
  (idempotent); `stores build --check` rebuilds a scratch copy of the sources and fails when
  that copy does not pass `stores check`, a tracked document is not declared, or it tracks
  something other than the local store. `stores declare --write` writes the declaration the
  current index implies, to adopt the layout. Tracking or untracking a document through the
  API keeps the declaration current (a file outside the project is not declared), `stores
  check` notes a declared store whose `.sldb/core/` is versioned rather than ignored, and a
  declared file that is gone is reported by `build` as `missing`. `declare --write` writes
  the declaration the index implies: a model whose source is outside the project
  (sldb's own, from the installed package) is declared by `model_ref` alone, and a glob is
  written only for a folder with more than one tracked file, all of one model. Design:
  `docs/architecture/derived-store-boundary.md`.
- An inherited model whose owner uses a `src/` layout imports again. The import root was the
  owner's project root, so pron's models, which live under its `src/` directory, stayed unimportable in a
  store that inherits them; it is now the directory the owner's registered path puts the
  package in (`sldb.store.model_import_root`). sldb's own store inherits AnchorDoc,
  ProjectionDoc and MoveDoc from pron through a relative link (`../pron/.sldb`) instead of
  registering copies pinned to an absolute path that no longer existed.
- **Python 3.12 or newer is required** (`requires-python >=3.12`; it was `>=3.10`). Python
  3.10 reaches end of life this month, and the whole suite (sldb, deskops, spec2viz, graph_ui)
  moves to the same floor. CI tests 3.12 and 3.13. The compatibility code for 3.10 is gone:
  the `tomllib`/`tomli` fallback in the `tools/check_*.py` gates and the conditional `tomli`
  dev dependency. `uv.lock` is regenerated for the new floor.
- The pre-redesign singular groups `sldb store`, `sldb model` and `sldb doc` run again: they
  were parsed (and listed by `sldb doc --help`) but had no handler, so `sldb doc untrack`
  answered `Unknown command: doc`. The plural groups (`stores`, `models`, `docs`) remain the
  documented spelling.
- A change to a model's contract now rebuilds the edges of its documents. Adding
  `__reference_models__` to a model and running `stores update` used to reuse every document's
  edges shard (its hashes had not moved), so the new references never reached the index and
  `edges rebuild` walked nothing until the shards were deleted by hand. Each shard now records
  the contract it was built under; the first rebuild after upgrading rewrites every shard once.
- A store link can be removed or pointed elsewhere: `sldb.api.unlink_store(store, name)` /
  `sldb stores remove <name>`, and `link_store(..., replace=True)` / `stores add --replace`.
  Removing a link a model here is inherited from is refused (replace it instead). A link to a
  directory that is gone was only fixable by editing `store_index.yaml`; `stores check` now
  notes it (`broken_links` in `check_store`).
- A scalar list item reads back as written. An item whose text markdown reads as block syntax
  was lost or mangled on extract: `validation: ["```bash", "pytest", "```"]` came back as
  `["pytest"]` (so any rewrite of the document deleted the fence lines), and `# x`, `> x`,
  `- x`, `1. x`, `***`, `<b>` or a leading space lost their syntax. Such an item is now rendered
  with one leading backslash (a CommonMark escape) and extracted without it; only a value that
  opens its item (`- ⸢rev,list•x⸥`) is escaped. A hand-written item that already began with
  `\` before such syntax now reads without that backslash.
- Extracting and validating no longer re-parse the model's template each time: a template's
  recipes are computed once per template, `validate` renders once instead of twice, and the
  sections index reuses one markdown-it parser. On sldb's own store, extracting 153 documents
  went from ~420 ms to ~275 ms and their sections from ~205 ms to ~175 ms.
- The markdown AST keeps what a token carries beyond its text, in `SLDBNode.metadata`: a
  fence's language (`info`), its opening markup (`markup`) and its attributes.
- `sldb edges show <name>` with something that is no node of the index fails, and suggests the
  document's export id (`Did you mean PillDoc:pill-008?`), instead of printing `[]` as for a
  real node without edges.
- `models show`, `models template show` and `docs update` take `--format text|json|yaml`
  (`models show` keeps YAML as its default; the template comes wrapped as
  `{model, draft, path, template}`; `docs update` reports `{updated, model, path}`). An
  argument a subcommand does not know is reported with that subcommand's usage, not the
  root's.
- A model's `__family__` changed in the class reaches the store: `stores update` and
  `models update` re-read it (it was written only at `models add`).
- `sldb.api.registered_models(store)` and `is_model_registered(store, model)` (by name,
  `module:Class` or `module.Class`), and `sldb models check <model>...`, which reports each as
  registered or missing and exits 1 if any is missing.
- `stores check` notes ignore rules that break the store's split (`.sldb/core` ignored, or
  `.sldb/runtime` not ignored); `check_store` returns it as `gitignore_policy`.
- A registered model that does not import here no longer takes the store's AST down: it is
  listed with `resolved: false` and the error (a healthy model's entry is unchanged), so `models show` and `ast show` of the rest
  answer (in an environment without `pron`, `models show TaskDoc` failed).
- `models template show` (and every draft operation) finds a model's source by importing its
  `model_ref` when the recorded path is not a file here: a store copied without its models,
  an absolute path from another machine, or an inherited model, whose path is empty and
  failed with `Is a directory`. When neither works, the error names the model and the store.
- A template's literal paragraph (deskops' `_Describe the incoming message..._`) anchors only a
  paragraph with that text. A document written without the placeholder had its first real
  paragraph taken for it and dropped on extract, so any rewrite deleted it (the first
  paragraph of inbox notes; `why`, `goal` and `done_when` of a task). Documents that lacked
  the placeholder now extract more: `stores check` reports them as `data_mutation` until
  `sldb models update <Model>` re-extracts the model (`stores update` trusts a document whose
  text did not move). Headings still anchor by position.
- A document that ends before its template does keeps its last section: a field of a section
  the document does not have (`## When`, after a document that stops at `## Why`) no longer
  claims the last section's paragraph, which came out empty and was erased by any rewrite.
  Past a missing heading, only later headings end a section. The `purpose` of three of
  sldb's rituals came back (`models update RitualDoc`).
- `stores check` names the documents a rewrite would lose content from: blocks of the file
  that do not survive `render(extract(text))`, because the model does not read them (written
  by hand, or by an older template). Their hashes are consistent over the poor extraction, so
  nothing else showed it. Sections the template fills only with `render`/`py` markers are
  regenerated and not counted. `check_store` returns it as `rewrite_loss`.
- `stores check --quiet` prints the PASS/FAIL line alone, as documented: it printed the
  per-document notes too, and now also skips the scans behind them.
- A `data_mutation` over text that did not move (and an unchanged contract) is explained as
  what it is, sldb reading the same file differently after an upgrade, and points to
  `sldb models update <Model>`: `stores check` said `stores update` would accept it, but
  `stores update` trusts unchanged text and did nothing. It no longer asks for a decision.
- `stores check` says, for a document whose text disagrees with its index, where the indexed
  text sits in the file's git history: `stale` (an earlier committed version, with the commit:
  the index fell behind), `unmatched` (no committed version has it: an edit indexed and never
  committed, or damage), `orphan` (the file is gone) or `undetermined` (not a git work tree),
  with the `git log` command that shows it. The JSON report carries it as `history`.
- `sldb.store` imports the rest of sldb through three seams only: `store/exceptions.py`
  (errors), `store/runtime_codec.py` (extraction) and `store/model_contract.py` (what a model
  class declares, and the built-in relation types); it imports nothing from `sldb.api`, `cli`
  or `selfdoc`, and `tests/test_store_seams.py` keeps it so. `describe_field` and the field
  kinds moved to `sldb.models.field_schema` (still importable from `sldb.api.schema`), which
  closes the store → api edge R4 in `contracts/layers.toml`.
- `selfdoc python-check` and `python-sync` work again: a property with a setter (or an
  `@overload`) was two symbols with one document id, and both commands failed with "Python
  symbols collide". A name redefined in its scope is now one symbol.
- kgdb is part of sldb, and nothing invokes an external `kgdb` any more. `selfdoc python-sync`
  writes the source graph with sldb's own graph IO instead of running `kgdb ingest` (it failed
  once the separate package was gone). `--kgdb-command` and `--kgdb-output` were removed and
  are refused with a clear error; the graph goes to `--graph-output`, by default
  `.sldb/runtime/graphs/python-source.graph.json` (it was `.kgdb/python-source.graph.json`).
  `sldb.selfdoc.kgdb_sync` is now `sldb.selfdoc.source_graph_file` (`write_source_graph`), and
  the selfdoc report's `kgdb_stale` is `graph_stale`. The data contract
  `sldb_kgdb_semantic_export` keeps its name (see the entry on kgdb names below).
- Docstring metadata is parsed strictly (`sldb.selfdoc.docstring_metadata`, spec section 2):
  only an opening line exactly `---` starts it, a closing `---` is required, and the block is a
  YAML mapping with unique keys among `id` (required), `kind` and `tags` (`namespace:value`,
  deduplicated). Malformed metadata and an id declared twice are reported as `path:line:
  problem` in the selfdoc report's `metadata_errors`, and `selfdoc python-sync` writes nothing
  while any remain; they were silently ignored and the declaration lost its identity.
- The source graph gives every module and symbol node its `local_tags` and `effective_tags`,
  inherited along the lexical chain package -> module -> class/function -> nested declaration
  within the scan (spec section 3): `system:*` and `workspace:*` from the nearest declaration,
  `topic:*` as a union, any other tag local only; nothing through imports, base classes or
  siblings. Each effective tag names the declaration and `path:line` it comes from. Two
  `system:` (or `workspace:`) tags on one declaration are a metadata error.
- An import in the source graph follows explicit re-export chains to the definition
  (`from sldb.api import open_store` reaches `sldb.api.stores.open_store:open_store`), through
  module-level imports only, with the chain in the edge's `via`; `from pkg import submodule`
  reaches the submodule. A star import, a cycle or a module outside the scan stays
  unresolved. A relative import inside a package's `__init__.py` resolves against that
  package (it was resolved against the parent: `pkg.impl` for `pkg.inner.impl`).
- `stores check` reuses its per-document content scans (rewrite loss and structural noise)
  while a document's text, its model's contract and the sldb that reads it have not moved, in
  the user's cache directory; the rewrite-loss scan also reuses the extraction the check
  already has instead of extracting again. On sldb's store (2775 documents) a full check went
  from 43 s to 23 s cold and 7 s warm, with the same findings.
- The source graph keeps the condition an import lives under (`context`: `type_checking`,
  `conditional`, `try`), and marks an import a later same-scope binding shadows
  (`shadowed_at`); a reference after the shadowing no longer resolves to the import.
- `selfdoc python-check` reports, apart from errors and drift, the declarations without
  metadata (`undeclared`), the declared ones without an explanation (`unexplained`) and the
  annotation references nothing resolves (`unresolved_references`, which were dropped).
- A symbol document's `purpose` is generated from the first paragraph of its docstring when it
  is a placeholder or was generated before; an authored purpose is kept and listed in
  `purpose_conflicts` for a decision.
- `selfdoc python-sync` reports on what is on disk after writing: it reported the plans made
  before writing, so a sync that wrote everything returned 1.
- Deleting `.sldb/runtime/` and rebuilding brings the sections and semantic indexes back. The
  user cache (`~/.cache/sldb/runtime-cache-built/`) and the in-process dirty set vouched for
  shards that were gone, so a rebuild wrote only the edges and a graph snapshot lost
  `has_section` and `semantic_parent` (reported by graph-ui).
- The last kgdb names in sldb's public surface are sldb's now (kgdb merged into sldb):
  - `sldb.store.export.export_kgdb_semantic_payload` is `export_semantic_payload`;
  - the semantic export contract keeps its name, `sldb_kgdb_semantic_export` version 1, and so
    do its schema and fixture (`contracts/schemas/sldb_kgdb_semantic_export.schema.json`,
    `contracts/fixtures/sldb_kgdb_semantic_export.v1.json`). It is a frozen data identifier,
    like the `sldb://...` node ids: renaming a data contract breaks every reader of files
    already written, so a format change goes behind a new contract version, never a rename.
    Main wrote `sldb_semantic_export` for a while before release; an export under that name is
    still read, never written. `tests/store/test_export_contract_frozen.py` pins the contract,
    the ids and the keys of the store index and of the document entries. The reading function is `sldb_semantic_export_to_snapshot`;
  - `stores semantic-export --format kgdb` is `--format sldb`;
  - the `sldb serve` route `/kgdb/snapshot` is `/semantic-export`;
  - the store's tracked relation types moved from `kgdb/relation_types/` to
    `sldb/relation_types/`, where `edges init` already wrote the new ones.
- `stores init` fails cleanly: what a failed init wrote is removed, the message says where it
  failed and what to check (instead of `Unexpected: [Errno 13] ...`), and the exit code tells
  a caller what happened: 0 created or already there, 2 the place refused it (permissions),
  1 failed half-way. `init_store` raises `StoreInitError` (an `SLDBStoreError`).

## 0.1.12 - 2026-10-18 — declared references resolve bare ids and paths, and report what names nothing

- Declared references resolve bare ids and paths. A value of a `__references__` or
  `__containment__` field names its document as an export id, as the path a tracked document
  lives at, or as a bare id tried against the models the field allows — the new
  `__reference_models__ = {"field": ["Model", ...]}`, or the containment list; one match
  resolves, several are `ambiguous`. It is decided when the index is composed, so tracking the
  target later resolves it. What names nothing is reported, never an edge:
  `sldb.api.unresolved_references(store)` / `sldb edges unresolved` /
  `EdgeIndex.unresolved_references` (`UnresolvedReference`: source, model, field, target,
  target_export_id, relation, reason, source_path). A free reference field only reports export
  ids. `EDGE_INDEX_VERSION` is 4: shards rebuild. `__reference_models__` enters the contract
  hash only for a model that declares it.
- An edge sldb derives (structural, schema, alias) is checked against sldb's own definition of
  its builtin type, even where the store authored a type under that name (selfdoc's code
  `contains` / `references`).
- `edges check` of a store that links others fails only on its own edges: what only a linked
  store's edges commit (an owner's stale shards, its cardinality violations) is reported apart
  (`EdgeCheckReport.linked_errors`, `linked_stale`; a `note:` line in the CLI). Edges read
  from a linked store carry `metadata["from_store"]`.
- Inheriting a model into a store (`models inherit`, or `alias:Model` on first use) signs its
  empty roster, so `stores check` passes without a `stores update` first.
- A section no longer counts as the owner of a path: a bare composition or reference value
  equal to a heading path resolved to that section instead of a document.

## 0.1.11 - 2026-10-18 — models are defined once and inherited; a free `attributes` on relations

- `RelationDoc.attributes`: a free dict of the edge's own attributes (a multiplicity, a role, a
  transition's action), written in the frontmatter and copied to the index edge as
  `metadata["attributes"]`. A RelationDoc written before has none. Its contract moved: run
  `sldb stores update` in a store that tracks RelationDoc documents.
- `sldb.api.StructuredNLDoc`: the base class of models, from the public surface.
- `sldb.api.graph.query_snapshot(snapshot, query)`: a StructuredQuery over a GraphSnapshot held
  in memory, no store needed. `sldb.api.graph` also exports `Edge` and `SystemIdentity`.
- `models inherit` and the `stores check` note tell a copy by its class, not by the reference
  string: `deskops.models.atom:AtomDoc` is a copy of `deskops.models:AtomDoc` when the package
  re-exports it. A converted copy takes the owner's `model_ref`.
- `edges check` over linked stores: one edge that two stores both emit (a shared model's
  `has_field`) counts once for cardinality; `has_model` is many-to-many, since stores share a
  model they inherit; `links_to` is a builtin relation type. `sldb edges init` now also
  rewrites a tracked builtin relation type whose spec moved (`updated` in its report), and no
  longer writes a builtin over an authored relation type of the same name.
- Models are defined once, in the store that owns them, and inherited by the others.
  `sldb models inherit alias:Model` / `sldb.api.inherit_model` registers an inherited entry
  (`origin: <alias>`, no source path) or converts a local copy in place, keeping its documents,
  roster and signed contract. Using `alias:Model` as a model name now inherits instead of
  copying. An inherited model imports from the owner's project root, so no `--pythonpath` is
  needed and a moved owner is one link to update; with the owner unreachable the store keeps
  working on its own signature. `stores check` notes a local model under a name a linked store
  owns (a convertible copy, or an override to rename). The graph gains `links_to` between
  stores and `origin_store` on `has_model`. A store with no inherited models writes no
  `origin` key, so existing indexes do not change.
- `stores update` re-signs the roster of a model whose class does not import. It used to skip
  the model whole, so a stale roster (a merge that brought its shards in, say) stayed
  `roster stale` in `stores check`. Its documents are still not rehashed, it is still reported
  as skipped, and it keeps the contract it signed.
- `stores check` no longer reports a moved contract for a model with `extra="allow"` (deskops'
  TaskDoc) whose documents carry undeclared frontmatter keys. Such a key is still produced by
  the current class, so it is not a field the model dropped; the check only counts a key the
  current extraction of the same document no longer yields. `stores update` could never clear
  the old finding.
- A template whose frontmatter is one `dict` placeholder (`⸢rev,dict•frontmatter⸥`) declares
  every key: `docs track` and `docs create` no longer refuse a document's extra keys, which that
  dict carries back on re-render.
- `producer.version` in a semantic export is the real package version: read from the source
  checkout's `pyproject.toml`, else from the installed `structuredLanguageDB` metadata. It
  asked for a distribution named `sldb`, which never exists, and always fell back to `0.1.0`.
- `click` is an optional extra (`pip install structuredLanguageDB[click]`), imported only when
  `ClickScanner` is used; it was imported unconditionally without being declared.
- `sldb.examples.pandoc_cv` ships in the wheel, with its Markdown files.
- `tools/check_identity.py` reads `git ls-files -z`: a quoted non-ASCII path no longer shows
  up as a top-level entry named `"docs`.

## 0.1.10 - 2026-10-17 — references to a relation type reach it; a document by absolute path

- A `__references__` field that points at `RelationTypeDoc:<doc>` now lands on the
  `sldb://relation_type/<name>` node. The index stores relation types under that node, so the
  schema edge used to point at a document node that does not exist and was dropped silently
  while `doc_exists` said yes. `resolve_edges` moves that end to the relation-type node.
- `find_doc` (behind untrack and delete) accepts a document's absolute path as well as the path
  relative to the project root.
- Design notes for the surface in `docs/surface/`, with tests for the MachineDoc editor and an
  optimistic-lock client. The editor test compiles on Python 3.10/3.11 (no nested PEP 701
  f-string).

## 0.1.9 - 2026-10-16 — a dropped field is a contract move, and `stores update` fixes it

- A document whose `field_hashes` name a field its model no longer declares was signed under
  another contract. Any write of another document of the model re-stamps the model's contract,
  so the model looked unmoved: `stores check` blamed the untouched document (`data_mutation`,
  "confirm the change was intended") and `stores update` trusted its unchanged text and never
  re-extracted it, so the check stayed red. Now the model reads as `contract moved` (safe to
  run: `stores update`) and `stores update` re-extracts those documents.

## 0.1.8 - 2026-10-16 — a deleted model class no longer locks the store

- Derived-index rebuilds skip a model whose class does not import instead of raising; the
  semantic rebuild names it in `models_unresolved`, as the edge rebuild already did, and its
  documents keep their last tags. `untrack_document` (and every write that rebuilds) works
  while another registered model's class is gone.
- `sldb models remove <name> --with-documents` / `remove_model(..., untrack_documents=True)`:
  drops a model and its tracked documents without importing the class; the Markdown files stay.
- A write that raises halfway leaves no trace: `untrack_document` puts the document's shard,
  the models index and the store index back as they were; `remove_model` changes the registry
  first and deletes the model's files only once every rebuild succeeded.

## 0.1.7 - 2026-10-16 — `models remove`

- `sldb models remove <name>` / `sldb.api.remove_model(store, name)`: unregisters a model that
  tracks no documents, with its indexes and shards; the class is never imported, so a model
  whose code was deleted can go. A model that still tracks documents is refused (untrack them
  first). `stores check` already passes with such a model registered (0.1.5); its note now
  names the unimportable models with no documents as removable.

## 0.1.6 - 2026-10-16 — the graph as a state machine

- `--where` joins predicates with ` and ` (outside literals; no `or`, no parentheses), and
  `nonempty(f)` is `has(f)` that also rejects `[]` and `{}` (`has` keeps its meaning).
- `sldb.api.where_matches(expression, payload, subject=None)`: a `--where` predicate on a plain
  payload, tracked or not; `{field}` fills from `subject` (default: the payload). An unparseable
  part raises `WherePredicateError`, now exported from `sldb.api`.
- `sldb.api.edges_holding(store, node, subject, relation=None)`: the edges leaving a node whose
  condition (the edge's, else its type's) holds on the subject; `sldb edges show <node>
  --holds-for <doc>` is the same from the CLI. A self-loop is a valid edge (a terminal
  transition).

## 0.1.5 - 2026-10-16 — an unimportable model is named, not blamed on its documents

- `stores check`: when a model's class cannot be imported (a clean clone without the model's
  package, a consumer's CI with another `sldb` first on PATH), its fields cannot be
  re-extracted. Every document used to read as a `data_mutation` ("decide first", restore the
  file). Intact text now stands for intact fields, and the report names the unresolved models;
  changed text still fails. JSON: `models[].resolved`.
- CI: the structural gates pass (`legacy_contract` mapped to the `migracion` axis, unit coupling
  updated; the surface gate no longer compares the five-consumer total with a partial view),
  and `selfdoc check` passes (knowledge/ synced with the CLI, the store committed with it).

## 0.1.4 - 2026-10-16 — `fields update` leaves the store passing

- A field write (`fields update|append`, `sldb.api.save_document_payload`) rewrote the Markdown
  and the model's roster but not the document's record, so `stores check` failed with a
  `data_mutation` on the write sldb had just made. The shard cache handed out its own instance:
  the caller edited it in place and the save, comparing against the cache, saw no change and
  skipped the write. Loads now return a copy (`sldb.store.io.shards`), which also covers the
  semantic, sections and edges shards.

## 0.1.3 - 2026-10-16 — upgrading sldb no longer fails unchanged stores

Found on Governance's `pulse`, which installs sldb from git: both checks failed on a store whose
content had not changed.

- `stores check`: a model whose stored contract hash equals the formula sldb used before
  cecd97b (fields and template only) passes, with a note naming those models, instead of
  "contract moved" on every model. A class that really changed still fails. `stores update`
  re-seals the hash under the current formula. JSON: `models[].legacy_contract`.
- `edges check`: in a store that ran `edges init`, an edge sldb derives itself whose builtin
  type was added later (`composes`) is checked against the definition sldb ships and reported in
  `untracked_builtins`, not as an error. A store that never ran `edges init` still fails;
  authored edges still need a tracked type.

## 0.1.2 - 2026-10-16 — referencing documents of linked stores

- `stores add` links were recorded but no document lookup read them: `docs show
  alias:doc` answered `Unknown document target`. `docs show` (and `sections show|fields`,
  serve's document routes) now take `alias:ref` — name, `Model/name` or tracked path — and
  read only the store linked directly as `alias`. A bare ref still reads only the local store;
  a prefix that names no link leaves the ref whole, so existing refs resolve as before.
- Add `docs exists <[alias:]ref>` and `sldb.api.doc_status|doc_exists`: whether a reference
  resolves, from the indexes alone (no model import, nothing written). Exit 0 ok, 1 missing,
  2 ambiguous, 5 `link-missing` / `link-broken`, so a missing document is told apart from a
  sibling repo that is not there.
- `stores list` (and `sldb.api.store_links`) report each link's state: `ok`, `missing` or
  `not-a-store`; a broken link is reported, never raised.
- `stores add` records the link relative to the project root (it was absolute outside it), and
  refuses linking a store to itself, aliases outside `[A-Za-z0-9][A-Za-z0-9._-]*` and the
  reserved `local`. Links already written are read as before.
- `stores init` seals the root hash over the empty model layer: a new store, or one that
  only links others, passes `stores check` without a `stores update`.
- `docs show` of a linked doc reads its file from the linked project (`absolute_path` was
  built from the local root).

## 2026-10-01 — SLDB is the substrate again

- The README no longer calls this generation frozen: the v2 seed (`knowledge`) was frozen in
  turn and its evaluator moved to `pron`, so nothing supersedes this package. SLDB is the
  store every surface (`surface/`, `tools/graph_ui`, `tools/sldb-ui`) is a view over. <!-- gone -->
- New README section "Serving and surfaces": `sldb serve` routes grouped by what a UI needs,
  and where the surfaces and their design docs live.

## 2026-09-07 — v1 frozen

- The README marks this generation frozen, with `knowledge` as its successor. Earlier modularization and v0.6 removal plans are historical and do not promise further v1 releases.

## Working tree — `docs delete`

- Add `docs delete` (and `sldb.api.delete_document`): untrack a document **and** remove
  its Markdown file. `docs untrack` was the only way to drop a document, and it keeps
  the file on purpose — so "delete this document" meant untrack, then `rm` by hand, then
  remember that `runtime/cache/extracted.json` still describes the deleted path until
  some later full load rewrites it. `delete` does the three.
- Confirms before removing the file unless `--yes` is given; a non-interactive stdin
  answers no.
- Add `runtime_cache_disk.forget(store, predicate)` so cache entries can be dropped
  without a full store load.

## Working tree — self-documentation follow-up

- Add `selfdoc scan|sync|check` to derive CLI facts from argparse, preserve authored explanations, and synchronize tracked command/surface documents from the selected store root.
- Report obsolete documents without deleting them; check freshness without writing documents or indexes.
- Expose public parser help for the supported `init` and `example` commands.
- Split knowledge document definitions into one class per file, keeping public import references and resolving re-exported definitions for template editing.
- Separate follow-up work into self-documentation, store context/federation, and AST ownership/section contracts. No package version bump or publication is included.

## Historical pending changes

- Add reversible `rev,table[...]` template markers for rendering and extracting Markdown tables backed by `list[dict]` fields.
- Add generic cross-store document writes through linked store aliases and federated model namespaces for workflow tools such as `deskops`.

## 0.2.0 - 2026-05-16

- **Store write concurrency**: atomic writes + advisory `fcntl` locks on all index write paths; `--wait` flag for `stores update`
- **Rebuild auditability**: `RebuildReport` dataclass tracks missing docs, empty sections, and unparseable headings in both semantic and section rebuilds; `--verbose` flag for details
- **CLI deprecation surface**: old singular commands (`store`, `model`, `doc`, `ls`, `get`, etc.) emit deprecation warnings; v0.6 was the historical removal target (see freeze note above).
- **Read-side hot path**: `sections show` and `sections fields` prefer persisted index over full IR rebuild; `--rebuild` flag available on `find`/`sections find`
- **Marker ownership robustness**: field name from the canonical `parse_marker()` is validated against known payload paths; unknown markers log a warning

## 0.1.2 - 2026-04-24

- Reorganize the package into `core`, `models`, `runtime`, `cli`, `assets`, and `examples` subpackages while keeping compatibility re-exports
- Add explicit link recovery and transclusion composition with `recover` and `compose`
- Add structural store queries under `st` with `ls`, `get`, `glob`, and `find --where`
- Add store-local semantic indexing under `se` and explicit federated semantic navigation under `gse`
- Add model semantic metadata, canonical model registration, semantic equivalence mapping, and bundled tests for the new workflows

## 0.1.1 - 2026-04-24

- Add current-system architecture docs and diagrams under `docs/architecture/`
- Add feature proposal docs under `desk/` for future SLDB features: link/recover/compose, store tree indexing, semantic DAG indexing, canonical/global-local semantics
- Add desk workspace with task board, self-docs, and operating procedures

## 0.1.0 - 2026-04-21

- Rename the package and CLI from `nldb` to `sldb`
- Add safe-by-default Python marker execution with configurable unsafe mode
- Ship the SLDB example bundle and CLI workflows for extract, render, validate, init, and example
- Add release basics: MIT license, package metadata, and CI

FILE:tests/test_rules_language_spec.py
"""Spec tests for ``docs/architecture/rules-language.md`` (GO02).

Each test states the example documented for one construction and marks it ``xfail`` until
GO05 implements the language. ``EXPECTED_XFAIL`` is the number of documented constructions
fixed by this file (p9); it must stay >= 25.

The evaluator module does not exist yet, so the imports live inside the test bodies (via the
helpers below): collection must not break, and every test currently fails for the real
reason "module not found". The concrete module path, call signature and graph fixture are
recorded as hypotheses in the document (§8, H1-H4).
"""

from __future__ import annotations

import hashlib

import pytest

from sldb.store.query_engine.where_parse import WherePredicateError

EXPECTED_XFAIL = 52


# --- provisional spec adapter (see rules-language.md §8, H1-H4) -------------------------

def _parse(text: str):
    from sldb.store.query_engine.rules import parse_predicate

    return parse_predicate(text)


def _findings(text: str, graph: dict, subject: str | None = None) -> list:
    from sldb.store.query_engine.rules import eval_predicate, parse_predicate

    return eval_predicate(parse_predicate(text), graph, subject=subject)


def _value(finding, key: str):
    return finding[key] if isinstance(finding, dict) else getattr(finding, key)


def _norm(value) -> str:
    if value is True:
        return "true"
    if value is False:
        return "false"
    return str(value).lower()


def _one(text: str, graph: dict, subject: str | None = None):
    findings = _findings(text, graph, subject)
    assert len(findings) == 1, findings
    return findings[0]


def _holds(text: str, graph: dict, subject: str | None = None) -> str:
    return _norm(_value(_one(text, graph, subject), "holds"))


def _contract_hash(model_type, field_hashes: dict[str, str]) -> str:
    from sldb.store.query_engine.rules import contract_hash

    return contract_hash(model_type, field_hashes)


def _expected_contract(fields, field_hashes: dict[str, str]) -> str:
    lines = [
        f"{name}={field_hashes.get(name, '')}"
        for name in sorted(fields, key=lambda name: name.encode("utf-8"))
    ]
    return hashlib.sha256("\n".join(lines).encode("utf-8")).hexdigest()


# --- graph fixture builders (see rules-language.md §8, H2) -----------------------------

def _doc(model: str = "TaskDoc", **payload):
    return {"model": model, "payload": payload}


def _graph(nodes: dict, edges=()) -> dict:
    return {"nodes": dict(nodes), "edges": list(edges)}


def _edge(source: str, type_: str, target: str, field: str | None = None, **extra) -> dict:
    edge = {"source": source, "type": type_, "target": target, **extra}
    if field is not None:
        edge["field"] = field
    return edge


# --- (a) grammar ------------------------------------------------------------------------

@pytest.mark.xfail(strict=True, reason="GO05: lenguaje de reglas no implementado")
def test_precedence_not_over_and_over_or():
    graph = _graph({"Task:a": _doc(note="x")})
    assert _holds('has(status) and status = "open" or has(note)', graph, "Task:a") == "true"


@pytest.mark.xfail(strict=True, reason="GO05: lenguaje de reglas no implementado")
def test_not_binds_tighter_than_and():
    graph = _graph({"Task:a": _doc(note="x")})
    assert _holds("not has(status) and has(note)", graph, "Task:a") == "true"


@pytest.mark.xfail(strict=True, reason="GO05: lenguaje de reglas no implementado")
def test_parentheses_group_expression():
    graph = _graph({"Task:b": _doc()})
    assert _holds("not (has(a) or has(b))", graph, "Task:b") == "true"


@pytest.mark.xfail(strict=True, reason="GO05: lenguaje de reglas no implementado")
def test_left_associativity_with_parentheses():
    graph = _graph({"Task:c": _doc(a=1, c=2), "Task:d": _doc(b=1)})
    assert _holds("(has(a) or has(b)) and has(c)", graph, "Task:c") == "true"
    assert _holds("(has(a) or has(b)) and has(c)", graph, "Task:d") == "false"


@pytest.mark.xfail(strict=True, reason="GO05: lenguaje de reglas no implementado")
def test_comparison_equal():
    graph = _graph({"Task:a": _doc(status="open")})
    assert _holds('status = "open"', graph, "Task:a") == "true"


@pytest.mark.xfail(strict=True, reason="GO05: lenguaje de reglas no implementado")
def test_comparison_not_equal():
    graph = _graph({"Task:a": _doc(status="closed")})
    assert _holds('status != "open"', graph, "Task:a") == "true"


@pytest.mark.xfail(strict=True, reason="GO05: lenguaje de reglas no implementado")
def test_comparison_less_than():
    graph = _graph({"Task:a": _doc(priority=2)})
    assert _holds("priority < 3", graph, "Task:a") == "true"


@pytest.mark.xfail(strict=True, reason="GO05: lenguaje de reglas no implementado")
def test_comparison_less_or_equal():
    graph = _graph({"Task:a": _doc(priority=3)})
    assert _holds("priority <= 3", graph, "Task:a") == "true"


@pytest.mark.xfail(strict=True, reason="GO05: lenguaje de reglas no implementado")
def test_comparison_greater_than():
    graph = _graph({"Task:a": _doc(priority=4)})
    assert _holds("priority > 3", graph, "Task:a") == "true"


@pytest.mark.xfail(strict=True, reason="GO05: lenguaje de reglas no implementado")
def test_comparison_greater_or_equal():
    graph = _graph({"Task:a": _doc(priority=3)})
    assert _holds("priority >= 3", graph, "Task:a") == "true"


@pytest.mark.xfail(strict=True, reason="GO05: lenguaje de reglas no implementado")
def test_in_list_membership():
    graph = _graph({"Task:a": _doc(statuses=["draft", "open"])})
    assert _holds('"draft" in statuses', graph, "Task:a") == "true"


@pytest.mark.xfail(strict=True, reason="GO05: lenguaje de reglas no implementado")
def test_in_substring():
    graph = _graph({"Task:a": _doc(title="draft spec")})
    assert _holds('"raf" in title', graph, "Task:a") == "true"


@pytest.mark.xfail(strict=True, reason="GO05: lenguaje de reglas no implementado")
def test_in_other_type_is_false():
    graph = _graph({"Task:a": _doc(priority=5)})
    assert _holds('"x" in priority', graph, "Task:a") == "false"


@pytest.mark.xfail(strict=True, reason="GO05: lenguaje de reglas no implementado")
def test_scalar_in_literal_list():
    graph = _graph({"Task:a": _doc(status="draft")})
    assert _holds('status in ["open", "draft"]', graph, "Task:a") == "true"


@pytest.mark.xfail(strict=True, reason="GO05: lenguaje de reglas no implementado")
def test_regex_search_semantics():
    graph = _graph({"Task:a": _doc(title="alpha beta")})
    assert _holds('title ~ "beta"', graph, "Task:a") == "true"


@pytest.mark.xfail(strict=True, reason="GO05: lenguaje de reglas no implementado")
def test_invalid_regex_raises_where_predicate_error():
    with pytest.raises(WherePredicateError):
        _parse('title ~ "("')


@pytest.mark.xfail(strict=True, reason="GO05: lenguaje de reglas no implementado")
def test_model_less_or_equal_family():
    graph = _graph({"Task:a": _doc("ChildDoc")})
    assert _holds("model <= BaseDoc", graph, "Task:a") == "true"


@pytest.mark.xfail(strict=True, reason="GO05: lenguaje de reglas no implementado")
def test_has_present_and_nonempty_value():
    graph = _graph({"Task:a": _doc(status="open"), "Task:b": _doc(status="")})
    assert _holds("has(status)", graph, "Task:a") == "true"
    assert _holds("has(status)", graph, "Task:b") == "false"


@pytest.mark.xfail(strict=True, reason="GO05: lenguaje de reglas no implementado")
def test_nonempty_rejects_empty_collections():
    graph = _graph({"Task:a": _doc(tags=["x"]), "Task:b": _doc(tags=[])})
    assert _holds("nonempty(tags)", graph, "Task:a") == "true"
    assert _holds("nonempty(tags)", graph, "Task:b") == "false"


# --- (b) paths, quantifiers, count and substitution -------------------------------------

@pytest.mark.xfail(strict=True, reason="GO05: lenguaje de reglas no implementado")
def test_any_quantifier():
    graph = _graph(
        {"Task:a": _doc(), "Task:b": _doc(status="open"), "Task:c": _doc(status="closed")},
        [_edge("Task:a", "references", "Task:b", "depends_on"),
         _edge("Task:a", "references", "Task:c", "depends_on")],
    )
    assert _holds('any(depends_on: status = "open")', graph, "Task:a") == "true"


@pytest.mark.xfail(strict=True, reason="GO05: lenguaje de reglas no implementado")
def test_all_quantifier():
    graph = _graph(
        {"Task:a": _doc(), "Task:b": _doc(status="closed"), "Task:c": _doc(status="closed")},
        [_edge("Task:a", "references", "Task:b", "depends_on"),
         _edge("Task:a", "references", "Task:c", "depends_on")],
    )
    assert _holds('all(depends_on: status = "closed")', graph, "Task:a") == "true"


@pytest.mark.xfail(strict=True, reason="GO05: lenguaje de reglas no implementado")
def test_none_quantifier():
    graph = _graph(
        {"Task:a": _doc(), "Task:b": _doc(status="closed"), "Task:c": _doc(status="closed")},
        [_edge("Task:a", "references", "Task:b", "depends_on"),
         _edge("Task:a", "references", "Task:c", "depends_on")],
    )
    assert _holds('none(depends_on: status = "open")', graph, "Task:a") == "true"


@pytest.mark.xfail(strict=True, reason="GO05: lenguaje de reglas no implementado")
def test_count_in_comparison():
    graph = _graph(
        {"Task:a": _doc(), "Task:b": _doc(status="closed")},
        [_edge("Task:a", "references", "Task:b", "depends_on")],
    )
    assert _holds('count(depends_on: status = "open") = 0', graph, "Task:a") == "true"


@pytest.mark.xfail(strict=True, reason="GO05: lenguaje de reglas no implementado")
def test_count_omits_missing_document_reference():
    graph = _graph(
        {"Task:a": _doc()},
        [_edge("Task:a", "references", "Doc:missing", "depends_on")],
    )
    assert _holds("count(depends_on: has(status)) = 0", graph, "Task:a") == "true"
    assert _holds("all(depends_on: status = \"closed\")", graph, "Task:a") == "true"


@pytest.mark.xfail(strict=True, reason="GO05: lenguaje de reglas no implementado")
def test_count_with_incomplete_element_is_incomplete():
    graph = _graph(
        {"Task:a": _doc()},
        [_edge("Task:a", "external_link", "Other:Doc:x", unavailable=True)],
    )
    assert _holds("count(rel:external_link: status = \"open\") = 0", graph, "Task:a") == "incomplete"


@pytest.mark.xfail(strict=True, reason="GO05: lenguaje de reglas no implementado")
def test_substitution_from_subject_payload():
    graph = _graph({"Task:a": _doc(capacity=6, party_size=4)})
    assert _holds("capacity >= {party_size}", graph, "Task:a") == "true"


@pytest.mark.xfail(strict=True, reason="GO05: lenguaje de reglas no implementado")
def test_substitution_missing_field_makes_false():
    graph = _graph({"Task:a": _doc(capacity=6)})
    assert _holds("capacity >= {party_size}", graph, "Task:a") == "false"


@pytest.mark.xfail(strict=True, reason="GO05: lenguaje de reglas no implementado")
def test_substitution_non_scalar_makes_false():
    graph = _graph({"Task:a": _doc(capacity=6, party_size=[4])})
    assert _holds("capacity >= {party_size}", graph, "Task:a") == "false"


@pytest.mark.xfail(strict=True, reason="GO05: lenguaje de reglas no implementado")
def test_substitution_not_applied_inside_quoted_literal():
    graph = _graph({"Task:a": _doc(label="{party_size}", party_size=4)})
    assert _holds('label = "{party_size}"', graph, "Task:a") == "true"


@pytest.mark.xfail(strict=True, reason="GO05: lenguaje de reglas no implementado")
def test_field_step_follows_references():
    graph = _graph(
        {"Task:a": _doc(), "Task:b": _doc(status="open")},
        [_edge("Task:a", "references", "Task:b", "depends_on")],
    )
    assert _holds('any(depends_on: status = "open")', graph, "Task:a") == "true"


@pytest.mark.xfail(strict=True, reason="GO05: lenguaje de reglas no implementado")
def test_undeclared_reference_field_is_empty_set():
    graph = _graph({"Task:a": _doc(), "Task:b": _doc(status="open")})
    assert _holds('any(no_declarado: status = "open")', graph, "Task:a") == "false"
    assert _holds('all(no_declarado: status = "open")', graph, "Task:a") == "true"


@pytest.mark.xfail(strict=True, reason="GO05: lenguaje de reglas no implementado")
def test_rel_type_step():
    graph = _graph(
        {"Task:a": _doc(), "Task:b": _doc(status="active")},
        [_edge("Task:a", "task_activates", "Task:b")],
    )
    assert _holds('any(rel:task_activates: status = "active")', graph, "Task:a") == "true"


@pytest.mark.xfail(strict=True, reason="GO05: lenguaje de reglas no implementado")
def test_inverse_field_step():
    graph = _graph(
        {"Task:a": _doc(), "Review:r": _doc(verdict="accepted")},
        [_edge("Review:r", "references", "Task:a", "subject")],
    )
    assert _holds('any(^subject: verdict = "accepted")', graph, "Task:a") == "true"


@pytest.mark.xfail(strict=True, reason="GO05: lenguaje de reglas no implementado")
def test_transitive_closure_field():
    graph = _graph(
        {"Task:a": _doc(), "Task:b": _doc(status="closed"), "Task:c": _doc(status="closed")},
        [_edge("Task:a", "references", "Task:b", "depends_on"),
         _edge("Task:b", "references", "Task:c", "depends_on")],
    )
    assert _holds('all(depends_on+: status = "closed")', graph, "Task:a") == "true"


@pytest.mark.xfail(strict=True, reason="GO05: lenguaje de reglas no implementado")
def test_transitive_closure_cycle_terminates():
    graph = _graph(
        {"Task:a": _doc(status="closed"), "Task:b": _doc(status="closed"), "Task:c": _doc(status="closed")},
        [_edge("Task:a", "references", "Task:b", "depends_on"),
         _edge("Task:b", "references", "Task:c", "depends_on"),
         _edge("Task:c", "references", "Task:a", "depends_on")],
    )
    assert _holds("count(depends_on+: has(status)) = 2", graph, "Task:a") == "true"


@pytest.mark.xfail(strict=True, reason="GO05: lenguaje de reglas no implementado")
def test_transitive_closure_rel_type():
    graph = _graph(
        {"Task:a": _doc(), "Task:b": _doc(), "Task:c": _doc(status="done")},
        [_edge("Task:a", "task_activates", "Task:b"),
         _edge("Task:b", "task_activates", "Task:c")],
    )
    assert _holds('any(rel:task_activates+: status = "done")', graph, "Task:a") == "true"


@pytest.mark.xfail(strict=True, reason="GO05: lenguaje de reglas no implementado")
def test_transitive_closure_inverse():
    graph = _graph(
        {"Task:a": _doc(), "Review:r1": _doc(), "Review:r2": _doc(verdict="accepted")},
        [_edge("Review:r1", "references", "Task:a", "subject"),
         _edge("Review:r2", "references", "Review:r1", "subject")],
    )
    assert _holds('any(^subject+: verdict = "accepted")', graph, "Task:a") == "true"


@pytest.mark.xfail(strict=True, reason="GO05: lenguaje de reglas no implementado")
def test_linked_store_unavailable_is_incomplete():
    graph = _graph(
        {"Task:a": _doc()},
        [_edge("Task:a", "external_link", "Other:Doc:x", unavailable=True)],
    )
    assert _holds('any(rel:external_link: status = "open")', graph, "Task:a") == "incomplete"


# --- (d) explanation and (f) eval signature ---------------------------------------------

@pytest.mark.xfail(strict=True, reason="GO05: lenguaje de reglas no implementado")
def test_finding_shape_and_seen_for_false_clause():
    graph = _graph({"Task:a": _doc(status="closed")})
    finding = _one('status = "open"', graph, "Task:a")
    assert _norm(_value(finding, "holds")) == "false"
    assert _value(finding, "node") == "Task:a"
    assert 'status = "open"' in _value(finding, "clause")
    assert _value(finding, "seen") == {"status": "closed"}


@pytest.mark.xfail(strict=True, reason="GO05: lenguaje de reglas no implementado")
def test_seen_and_first_false_branch():
    graph = _graph({"Task:a": _doc(status="closed", priority=5)})
    finding = _one('status = "open" and priority > 3', graph, "Task:a")
    assert _norm(_value(finding, "holds")) == "false"
    assert set(_value(finding, "seen")) == {"status"}


@pytest.mark.xfail(strict=True, reason="GO05: lenguaje de reglas no implementado")
def test_seen_or_first_true_branch():
    graph = _graph({"Task:a": _doc(status="open", priority=5)})
    finding = _one('status = "open" or priority > 3', graph, "Task:a")
    assert _norm(_value(finding, "holds")) == "true"
    assert set(_value(finding, "seen")) == {"status"}


@pytest.mark.xfail(strict=True, reason="GO05: lenguaje de reglas no implementado")
def test_seen_not_negated_leaf():
    graph = _graph({"Task:a": _doc(status="open")})
    finding = _one("not has(status)", graph, "Task:a")
    assert _norm(_value(finding, "holds")) == "false"
    assert set(_value(finding, "seen")) == {"status"}


@pytest.mark.xfail(strict=True, reason="GO05: lenguaje de reglas no implementado")
def test_seen_quantifier_witness():
    graph = _graph(
        {"Task:a": _doc(), "Task:b": _doc(status="closed"), "Task:c": _doc(status="open")},
        [_edge("Task:a", "references", "Task:b", "depends_on"),
         _edge("Task:a", "references", "Task:c", "depends_on")],
    )
    finding = _one('all(depends_on: status = "closed")', graph, "Task:a")
    assert _norm(_value(finding, "holds")) == "false"
    assert _value(finding, "seen") == {"status": "open"}


@pytest.mark.xfail(strict=True, reason="GO05: lenguaje de reglas no implementado")
def test_eval_with_subject_returns_one_finding():
    graph = _graph({"Task:a": _doc(status="open"), "Task:b": _doc(status="closed")})
    assert len(_findings("has(status)", graph, "Task:a")) == 1


@pytest.mark.xfail(strict=True, reason="GO05: lenguaje de reglas no implementado")
def test_eval_without_subject_returns_all_domain_documents():
    graph = _graph(
        {"Task:a": _doc(status="open"), "Task:b": _doc(status="closed"), "Task:c": _doc()}
    )
    findings = _findings("has(status)", graph)
    assert {_value(f, "node") for f in findings} == {"Task:a", "Task:b", "Task:c"}


@pytest.mark.xfail(strict=True, reason="GO05: lenguaje de reglas no implementado")
def test_top_level_model_conjunction_restricts_domain():
    graph = _graph(
        {"Task:a": _doc("ChildDoc", status="open"),
         "Task:b": _doc("ChildDoc", status="closed"),
         "Task:c": _doc("OtherDoc", status="open")}
    )
    findings = _findings('model <= BaseDoc and status = "open"', graph)
    assert {_value(f, "node") for f in findings} == {"Task:a", "Task:b"}


@pytest.mark.xfail(strict=True, reason="GO05: lenguaje de reglas no implementado")
def test_nested_model_does_not_restrict_domain():
    graph = _graph(
        {"Task:a": _doc("ChildDoc", status="open"),
         "Task:b": _doc("OtherDoc", status="closed"),
         "Task:c": _doc("OtherDoc")}
    )
    findings = _findings("has(status) or model <= BaseDoc", graph)
    assert {_value(f, "node") for f in findings} == {"Task:a", "Task:b", "Task:c"}


@pytest.mark.xfail(strict=True, reason="GO05: lenguaje de reglas no implementado")
def test_two_top_level_model_constraints_intersect_domain():
    graph = _graph(
        {"Task:a": _doc("OnlyOne", status="open"),
         "Task:b": _doc("OnlyTwo", status="open"),
         "Task:c": _doc("Both", status="open")}
    )
    findings = _findings("model <= BaseOne and model <= BaseTwo", graph)
    assert {_value(f, "node") for f in findings} == {"Task:c"}


# --- (e) contract hash ------------------------------------------------------------------

class _NoContract:
    pass


class _EmptyContract:
    __contract__: list[str] = []


class _TwoFieldContract:
    __contract__ = ["title", "goal"]


class _Utf8Contract:
    __contract__ = ["á", "z", "A"]


@pytest.mark.xfail(strict=True, reason="GO05: lenguaje de reglas no implementado")
def test_contract_absent_uses_all_payload_fields():
    field_hashes = {"title": "t", "goal": "g"}
    assert _contract_hash(_NoContract, field_hashes) == _expected_contract(
        ["title", "goal"], field_hashes
    )


@pytest.mark.xfail(strict=True, reason="GO05: lenguaje de reglas no implementado")
def test_contract_empty_list_is_load_error():
    with pytest.raises(ValueError):
        _contract_hash(_EmptyContract, {"title": "t"})


@pytest.mark.xfail(strict=True, reason="GO05: lenguaje de reglas no implementado")
def test_contract_absent_field_contributes_empty_hash():
    field_hashes = {"title": "t"}
    assert _contract_hash(_TwoFieldContract, field_hashes) == _expected_contract(
        ["title", "goal"], field_hashes
    )


@pytest.mark.xfail(strict=True, reason="GO05: lenguaje de reglas no implementado")
def test_contract_order_is_utf8_bytes():
    field_hashes = {"A": "a", "z": "z", "á": "aacute"}
    assert _contract_hash(_Utf8Contract, field_hashes) == _expected_contract(
        ["á", "z", "A"], field_hashes
    )

FILE:instruccion
Cold-bundle de la tarea task-go05-lenguaje-de-predicados-unificado: con el TaskDoc, los rituales enrutados por el Board, las pills ligadas, los átomos ligados y los archivos que el TaskDoc nombra, reformula el encargo, lista ambigüedades con cita textual del input y da el DRY-RUN sin ejecutar nada. No ejecutes nada.

Sección de validación del TaskDoc:
- TMPDIR=/dev/shm pytest tests/test_rules_language_spec.py sin xfail ni skipped (los 52 pasan a verdes, sin marca xfail)
- tests de equivalencia contra los goldens de where_parse y FieldCondition capturados antes de tocar codigo
- test que cuenta cero llamadas a Validator.extract al evaluar un --where sobre todos los documentos de un modelo de este repo
- tests de DeprecationWarning (where_parse, compile_where, FieldCondition), de warnings en el envelope de sldb graph query con filtros dict, y de --where sin aviso
- sldb docs find --where con any()/all() sobre una relacion y --explain probado por CLI con envelope
- TMPDIR=/dev/shm pytest tests/test_clean_code_rules.py tests/test_store_seams.py en verde
- suite completa sin rojos (una vez, al final del nodo, la corre el supervisor)

