FILE:desk/tasks/task-go10-retiro-de-where-parse-y-fieldcondition.md
---
id: task-go10-retiro-de-where-parse-y-fieldcondition
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
- src/sldb/store/query_engine/where_parse.py
- src/sldb/store/query_engine/__init__.py
- src/sldb/store/graph/language/field_condition.py
- src/sldb/store/graph/language/field_condition_translation.py
- src/sldb/store/graph/language/facet_filter.py
- src/sldb/store/graph/language/__init__.py
- src/sldb/store/graph/language/predicate_cursor.py
- src/sldb/store/graph/language/predicate_tokens.py
- src/sldb/store/graph/payload_match.py
- src/sldb/store/graph/facet_match.py
- src/sldb/store/graph/__init__.py
- src/sldb/core/exceptions/where_predicate_error.py
- src/sldb/core/exceptions/__init__.py
- src/sldb/core/finding.py
- src/sldb/cli/commands/graph.py
- src/sldb/api/__init__.py
- src/sldb/api/graph/__init__.py
- src/sldb/api/notations/__init__.py
- src/sldb/notations/where_check.py
- contracts/layers.toml
- contracts/queries/sldb/sections_for_taskdoc_document.json
- contracts/queries/sldb/semantic_neighborhood_integration_kgdb.json
- contracts/queries/sldb/documents_tagged_domain_contract.json
- contracts/queries/sldb/documents_near_domain_workflow_task_tag.json
- contracts/queries/sldb/documents_near_taskdoc_model.json
- docs/architecture/graph-backend.md
- docs/architecture/rules-language.md
- docs/architecture/superseded-code-audit.md
- docs/architecture/code-docstring-indexing-handoff.md
- docs/architecture/code-docstring-indexing.spec.md
- docs/architecture/notations-and-views.md
- docs/requests/sldb-knowledge-graph-integration.md
- docs/user-manual.md
- CHANGELOG.md
- tests/store/test_predicate_language.py
- tests/store/test_where_retired.py
task_type: task.code
inherits_from: []
inherit_acceptance_context: false
atoms: []
---

# GO10: Retiro de where_parse y FieldCondition

## Rationale

_Explain why this task exists or the business driver behind it._

Nodo GO10 del plan desk/drawer/plans/grafo-operable (dag.yaml rev 9), hijo de PK04; regla 4 de alcance.md: el retiro de los lenguajes viejos es un nodo explicito. GO05 (8be66bde) dejo where_parse/compile_where y FieldCondition como shims deprecados detras de la API unica; GO06-GO09 ya usan solo el lenguaje nuevo. GO10 los borra de src/ y de docs/.

## Goal

_Describe the concrete result this task must produce._

Sin los identificadores where_parse ni FieldCondition en src/ ni en docs/ (salvo la tabla historica de rules-language.md bajo 'Historico'); sin los ocho operadores viejos en bloques de codigo de docs/ fuera de esa tabla; cada mencion reescrita con la construccion equivalente; goldens conservados como tests del lenguaje nuevo; CHANGELOG en la seccion en curso.

## Scope

_State what is in scope and what is out of scope._

En alcance: borrar where_parse.py (y compile_where), field_condition.py, field_condition_translation.py y el codigo muerto de facet_match (drawer task-tras-go05-quedan-sin-uso-las-funciones-de-facet-match-y-el-retiro-de-los-shims); los importadores residuales de src/; los JSON de contracts/queries/sldb que usan FieldCondition; los Markdown de docs/ listados en files (obtenidos por grep al promover); CHANGELOG.md; tests. Fuera: cambios de semantica del lenguaje; el resto de deudas del drawer.

PRINCIPIO DEL DUENO (2026-11-05): invariantes de un documento como validadores pydantic; los tests solo prueban rechazo. Aplicado aqui: (q1) el formato nuevo de FacetFilter se valida con pydantic: un StructuredQuery con la clave vieja conditions es rechazado con ValidationError que nombra el campo (un test de rechazo); no se agregan tests que reafirmen lo que ya prueban los existentes.

PRECISIONES AL PROMOVER (2026-11-07):
r1 (WherePredicateError): sale de where_parse.py a src/sldb/core/exceptions/where_predicate_error.py (capa 0; misma clase: ValueError y SLDBError, mismo mensaje) y se reexporta desde sldb.core.exceptions, sldb.store.graph.language y sldb.api; la importacion publica es from sldb.api import WherePredicateError. Sin alias ni modulo puente where_parse (decision del coordinador de proyecto, 2026-11-07). Consumidor externo afectado: pron importa sldb.store.query_engine.where_parse.WherePredicateError (pron/src/pron/world/storage/structural_query.py, pron/src/pron/sexpr/resolving/pending_match.py, pron/tests/test_layer_contract.py); el coordinador le avisa por inbox al integrar; GO10 no toca pron. Si con esto la arista models->store de R6 desaparece (RuleDoc ya no importa nada de store), se quita la entrada upward y el pending R6 de contracts/layers.toml; si no, quedan.
r2 (graph query): FacetFilter pierde conditions (list[FieldCondition]) y gana where: str, un predicado del lenguaje evaluado sobre la facet como hoy lo hace payload_match/facet_match con la traduccion de GO05; los cinco JSON de contracts/queries/sldb se reescriben con la columna nueva de la tabla de rules-language.md seccion 7 y tests/store/test_example_queries.py debe seguir devolviendo los mismos ids (si no, es un bug del reemplazo). sldb graph query deja de emitir el warning deprecated/field-condition; core/finding.py deja de nombrar FieldCondition. El CHANGELOG lo registra como cambio de contrato: el JSON de sldb graph query ya no acepta conditions; usa where con un predicado del lenguaje.
r3 (docs, grep mecanico): el grep de operadores se hace como lo fija la aceptacion (palabras completas dentro de bloques cercados y de codigo en linea de los .md de docs/). Toda aparicion en esos bloques se reescribe con la construccion equivalente de la tabla; si una aparicion no es un operador de FieldCondition (otra API, una palabra de un ejemplo ajeno), se reescribe el ejemplo para no usar la palabra sin cambiar su significado, y se reporta cada caso. La tabla historica se mueve bajo un encabezado que contenga la palabra Historico y queda integra.
r4 (goldens): tests/fixtures/where_goldens y los tests de equivalencia de tests/store/test_predicate_language.py se conservan como tests del lenguaje nuevo: la columna vieja queda como dato del golden (texto), sin importar los shims. tests/store/test_where_retired.py (nuevo) hace el grep de la aceptacion sobre src/ y docs/ y falla si aparece algo.
r5 (tests existentes): los tests que hoy ejercitan los shims (DeprecationWarning, compile_where, FieldCondition, warning de graph query) se borran o se reescriben al lenguaje nuevo; es la unica excepcion a 'tests existentes sin cambios' y se reporta archivo por archivo.

PRECISIONES (preflight de GO10, 2026-11-07):
r6 (codigo muerto): en src/sldb/store/graph/facet_match.py se borran matches_filters, facet_matches, condition_matches y las funciones ordered_* (las que nombra el drawer task); ademas, cualquier funcion o modulo de src/ que quede sin importador en src/ ni en tests/ tras retirar los shims (comprobado por grep) se borra y se reporta.
r7 (lista de docs): los Markdown de docs/ en files son la lista obtenida por grep al promover y es la de partida; si el grep de la aceptacion encuentra otro archivo, se agrega al trabajo y se reporta (no es desvio).
r8 (formato de goldens): no cambia: tests/fixtures/where_goldens/where_parse.json y field_condition.json siguen siendo listas de {old, matches} (old como string en where_parse.json y como dict {field, op, value} en field_condition.json; GO05 p13). Los nombres de archivo de fixtures y tests son libres (la aceptacion no hace grep en tests/). Los tests leen old como dato, sin importar ningun shim.
r9 (casos ajenos en docs): si la palabra aparece en un ejemplo que es un filtro, se reescribe con la construccion equivalente de la tabla; si aparece en codigo ajeno (otra API, un metodo de Python, un nombre de campo), se cambia lo minimo en el bloque para no usar esa palabra conservando lo que el ejemplo muestra (renombrar un campo de ejemplo, usar la expresion equivalente de Python). Cada caso se lista en el reporte; el coordinador los revisa al integrar.
r10 (R6): RuleDoc (src/sldb/models/rule_doc.py) importa de forma diferida el parser de store/graph/language; GO10 no mueve el parser, asi que la arista models->store sigue y las entradas [allow].upward [models, store] y [[pending]] R6 de contracts/layers.toml quedan como estan (su reparacion es el drawer task-r6-...). Mover solo WherePredicateError a core no la cierra.

## Implementation Path

_Outline the expected implementation route or affected surface._

CONTRATO DEL NODO (dag.yaml rev 9, GO10 scope): Borrar los shims de GO05 (where_parse y FieldCondition) y cualquier importador residual en src/ que el grep delate (el output_scope cubre todo src/ para eso), y, en docs/, toda mención de where_parse, FieldCondition y de los operadores eq, ne, gt, lt, contains, starts_with, is_null, is_not_null como sintaxis, es decir dentro de bloques de código cercados (```) o de código en línea (`...`) de los Markdown de docs/; la prosa queda excluida por construcción (el grep se restringe a esos bloques; lista obtenida al promover), reemplazada por el lenguaje nuevo: las menciones de los identificadores where_parse y FieldCondition se sustituyen por el nombre de la API única (where_matches y la gramática de rules-language.md) y las de operadores por la construcción equivalente de la tabla; la tabla histórica de rules-language.md se conserva íntegra bajo su encabezado. Los goldens viven en tests/, donde GO05 los dejó, y se conservan como tests del lenguaje nuevo; los nombres de archivos e identificadores de tests son libres (la aceptación no hace grep en tests/). La versión del CHANGELOG es la cabecera vigente del CHANGELOG (la sección en curso), no un número nuevo. Prerrequisito: todos los llamantes del repo usan la API única, lo que GO05 garantiza por su scope (enruta where_matches, edges_holding, StructuredQuery y --where) y GO10 comprueba mecánicamente con su grep; GO05, GO06, GO07 y GO09 son prerrequisitos transitivos vía GO08 (GO08 depende de GO06, GO07 y GO09; GO06 de GO05). Regla 4 de alcance.md: el retiro es un nodo explícito, este. Los goldens de equivalencia se conservan como tests del lenguaje nuevo. ACEPTACION: grep -r de los identificadores where_parse y FieldCondition en src/ y en todo docs/ (prosa incluida: son nombres de código, no palabras) no devuelve nada, con una única excepción nombrada: la tabla de equivalencia histórica de docs/architecture/rules-language.md, que se conserva bajo un encabezado "Histórico"; grep -rw de los ocho operadores restringido a bloques de código cercados y código en línea de los Markdown de docs/ no devuelve nada fuera de esa misma tabla (las equivalencias de GO02 no reutilizan esos nombres, así que el reemplazo no vuelve a dispararlo; la lista exacta de archivos se fija por grep al promover y queda en el TaskDoc); cada mención retirada se reescribe con la construcción equivalente de la tabla de GO02; la suite completa verde; CHANGELOG registra el retiro con la versión. OUTPUT_SCOPE: src/sldb/store/query_engine/, src/sldb/store/graph/language/, src/ (solo importadores residuales que el grep delate), tests/, docs/, CHANGELOG.md REGLAS COMUNES: alcance.md (regla 2: no cierra con tests rojos ni saltados; regla 4: retiro en nodo explicito, este; regla 6: hipotesis en el TaskDoc).

## Validation

_List the checks required before this task can close._

- grep -rn 'where_parse\|FieldCondition' src/ docs/ sin resultados fuera de la tabla historica de rules-language.md (bajo Historico)
- grep -rw de eq, ne, gt, lt, contains, starts_with, is_null, is_not_null en bloques de codigo de docs/*.md sin resultados fuera de esa tabla (tests/store/test_where_retired.py)
- StructuredQuery con conditions rechazado con ValidationError (test de rechazo); tests/store/test_example_queries.py devuelve los mismos ids con los JSON reescritos
- goldens de equivalencia verdes como tests del lenguaje nuevo
- TMPDIR=/dev/shm pytest tests/test_clean_code_rules.py tests/test_store_seams.py en verde y tools/check_layers.py PASS
- suite completa verde (una vez, al final del nodo, la corre el supervisor)
- CHANGELOG registra el retiro en la seccion en curso

## Done When

_Name the observable condition that makes the task complete._

Aceptacion de GO10 cumplida linea por linea, revision en frio aceptada, nodo integrado en main.

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

FILE:src/sldb/store/query_engine/where_parse.py
"""Deprecated (GO05): the old `--where` grammar, now a shim over the predicate language.

`WherePredicateError` stays here: it is the error every parse of the language raises. The
grammar itself lives in `sldb.store.graph.language` (`parse_predicate`), a superset of the
old one with the same operators and results (rules-language.md §7). `compile_where` and
`where_parse` still work and emit `DeprecationWarning`; GO10 retires them.
"""

from __future__ import annotations

import warnings
from typing import Any, Callable

from sldb.store.exceptions import SLDBError

Predicate = Callable[[Any, Any, Any], bool]  # (doc, resolve_model_ref, pythonpath) -> bool
_USE = "use sldb.store.graph.language.parse_predicate / document_matcher (rules-language.md)"


class WherePredicateError(ValueError, SLDBError):
    """A predicate that does not parse."""

    def __init__(self, expression: str):
        super().__init__(f"no evaluator understands the predicate: {expression!r}")


def compile_where(expression: str) -> Predicate:
    """Deprecated: the document matcher of the predicate language for `expression`."""
    warnings.warn(f"compile_where is deprecated: {_USE}", DeprecationWarning, stacklevel=2)
    from sldb.store.graph.language.predicate_documents import document_matcher

    return document_matcher(expression)


def where_parse(expression: str) -> Any:
    """Deprecated: `parse_predicate(expression)` of the predicate language."""
    warnings.warn(f"where_parse is deprecated: {_USE}", DeprecationWarning, stacklevel=2)
    from sldb.store.graph.language.predicate_parser import parse_predicate

    return parse_predicate(expression)

FILE:src/sldb/store/query_engine/__init__.py


FILE:src/sldb/store/graph/language/field_condition.py
"""Deprecated (GO05): one facet-field condition, now a shim over the predicate language.

Constructing a `FieldCondition` emits `DeprecationWarning`; `predicate()` is its translation
to the language (rules-language.md §7, rows 12-19): `eq`/`ne`/`gt`/`lt` are `= != > <`,
`contains` is `"x" in f` (also a substring now), `starts_with` is `f ~ "^x"` (x escaped),
`is_null` is `not has(f)` and `is_not_null` is `has(f)` (`has` also rejects `""`). GO10
retires it.
"""

from __future__ import annotations

import warnings
from typing import Any, Literal

from pydantic import BaseModel, Field, PrivateAttr

from sldb.store.graph.language.field_condition_translation import condition_predicate


class FieldCondition(BaseModel):
    """A single comparison condition on a facet field (deprecated: write the predicate)."""

    field: str = Field(description="Name of the field within the facet.")
    op: Literal["eq", "ne", "is_null", "is_not_null", "contains", "gt", "lt", "starts_with"] = Field(description="The comparison operator.")
    value: Any = Field(default=None, description="The value to compare against; ignored by the null operators.")

    _predicate: Any = PrivateAttr(default=None)

    def model_post_init(self, context: Any) -> None:
        self._predicate = condition_predicate(self.field, self.op, self.value)
        warnings.warn(f"FieldCondition is deprecated: write the predicate `{self._predicate.text}` (rules-language.md)", DeprecationWarning, stacklevel=2)

    def predicate(self) -> Any:
        """The condition in the predicate language (a parsed `Predicate`)."""
        return self._predicate

FILE:src/sldb/store/graph/language/field_condition_translation.py
"""`FieldCondition` → predicate tree, by the equivalence table (rules-language.md §7).

The value goes into the tree as a literal of any Python type (a bool, a list), so the
translation needs no literal syntax for it; the clause shows it written as the language would.
"""

from __future__ import annotations

import json
import re
from typing import Any

from sldb.store.graph.language.predicate_ast import Predicate
from sldb.store.query_engine.where_literal import quote, scalar_literal

_COMPARISON = {"eq": "=", "ne": "!=", "gt": ">", "lt": "<"}


def condition_predicate(field: str, op: str, value: Any) -> Predicate:
    """The parsed predicate equivalent to one `FieldCondition`."""
    root = _NULLS[op](field) if op in _NULLS else _VALUED.get(op, _comparison)(field, op, value)
    return Predicate(root[1], root)


def _has(field: str) -> tuple:
    return ("leaf", f"has({field})", "has", (field,))


def _contains(field: str, op: str, value: Any) -> tuple:
    return ("leaf", f"{written(value)} in {field}", "in", (("literal", value), ("field", field)))


def _starts_with(field: str, op: str, value: Any) -> tuple:
    pattern = "^" + re.escape(str(value))
    return ("leaf", f"{field} ~ {quote(pattern)}", "regex", (("field", field), re.compile(pattern)))


def _comparison(field: str, op: str, value: Any) -> tuple:
    symbol = _COMPARISON[op]
    return ("leaf", f"{field} {symbol} {written(value)}", "cmp", (("field", field), symbol, ("literal", value)))


_NULLS = {"is_not_null": _has, "is_null": lambda field: ("not", f"not has({field})", _has(field))}
_VALUED = {"contains": _contains, "starts_with": _starts_with}


def written(value: Any) -> str:
    """A value as the language writes it: a literal, a list of literals, else its JSON."""
    literal = scalar_literal(value)
    if literal is not None:
        return literal
    if isinstance(value, list) and all(scalar_literal(v) is not None for v in value):
        return "[" + ", ".join(scalar_literal(v) or "" for v in value) + "]"
    return json.dumps(value, default=str)

FILE:src/sldb/store/graph/language/facet_filter.py
"""A filter over the conditions on one facet."""

from __future__ import annotations

from pydantic import BaseModel, Field

from sldb.store.graph.language.field_condition import FieldCondition


class FacetFilter(BaseModel):
    """Filter nodes by conditions on a specific facet's fields."""

    facet: str = Field(description="The facet name to filter on (`identity`, `semantics`, `source`...).")
    conditions: list[FieldCondition] = Field(default_factory=list, description="Conditions to satisfy together.")

FILE:src/sldb/store/graph/language/__init__.py
"""The structured query language: facet filters, graph scope and relation filters."""

from sldb.store.graph.language.field_condition import FieldCondition
from sldb.store.graph.language.facet_filter import FacetFilter
from sldb.store.graph.language.graph_scope import GraphScope
from sldb.store.graph.language.relation_filter import RelationFilter
from sldb.store.graph.language.structured_query import StructuredQuery

__all__ = ["FacetFilter", "FieldCondition", "GraphScope", "RelationFilter", "StructuredQuery"]

FILE:src/sldb/store/graph/language/predicate_cursor.py
"""The cursor a recursive-descent parse carries: tokens, position, source text, and the
expression parser itself (so atoms can parse a quantifier's body without a circular import).
"""

from __future__ import annotations

from typing import Any, Callable

from sldb.store.query_engine.where_parse import WherePredicateError


def cursor(tokens: list, text: str, expression: Callable[[list], Any]) -> list:
    """`[tokens, position, text, expression]`."""
    return [tokens, 0, text, expression]


def peek(cur: list, offset: int = 0):
    """The token at the cursor plus `offset`, clamped to the final `eof` token."""
    return cur[0][min(cur[1] + offset, len(cur[0]) - 1)]


def take(cur: list):
    """Consume and return the token at the cursor."""
    token = peek(cur)
    cur[1] += 1
    return token


def previous(cur: list):
    """The last consumed token."""
    return cur[0][max(cur[1] - 1, 0)]


def span(cur: list, start: int) -> str:
    """The source text from `start` to the end of the last consumed token."""
    return cur[2][start:previous(cur).end].strip()


def keyword(cur: list, name: str, offset: int = 0) -> bool:
    """Whether the token at the cursor (plus `offset`) is exactly this name."""
    token = peek(cur, offset)
    return token.kind == "ident" and token.value == name


def is_op(cur: list, value: str, offset: int = 0) -> bool:
    """Whether the token at the cursor (plus `offset`) is exactly this operator."""
    token = peek(cur, offset)
    return token.kind == "op" and token.value == value


def expect_op(cur: list, value: str):
    """Consume this operator, or report the predicate as unparseable."""
    if not is_op(cur, value):
        fail(cur)
    return take(cur)


def expect_ident(cur: list):
    """Consume a name, or report the predicate as unparseable."""
    if peek(cur).kind != "ident":
        fail(cur)
    return take(cur)


def fail(cur: list):
    """The predicate does not parse: `WherePredicateError` naming the whole expression."""
    raise WherePredicateError(cur[2])

FILE:src/sldb/store/graph/language/predicate_tokens.py
"""Tokens of the predicate language: literals, numbers, names, keywords and operators.

A name may carry dots (`sldb.authority`, `tasks.0.title`): a field path for a leaf, or steps
joined by `.` inside a quantifier's path (rules-language.md §8, H5 and H9).
"""

from __future__ import annotations

import re
from collections import namedtuple
from typing import Any

from sldb.store.query_engine.where_literal import unquote
from sldb.store.query_engine.where_parse import WherePredicateError

_TOKEN = re.compile(
    r"""(?:
        (?P<literal>"(?:[^"\\]|\\.)*")
      | (?P<number>-?\d+(?:\.\d+)?)
      | (?P<ident>[A-Za-z_][\w.]*)
      | (?P<op>!=|<=|>=|[=<>~()\[\],{}:^+.])
    )""",
    re.VERBOSE,
)
Token = namedtuple("Token", "kind value raw start end")


def tokenize(text: str) -> list:
    """Every token of `text` with its source offsets, ended by an `eof` token."""
    tokens: list = []
    position = _skip_space(text, 0)
    while position < len(text):
        tokens.append(_token_at(text, position))
        position = _skip_space(text, tokens[-1].end)
    tokens.append(Token("eof", "", "", len(text), len(text)))
    return tokens


def _token_at(text: str, position: int) -> Any:
    match = _TOKEN.match(text, position)
    if match is None or match.end() == position:
        raise WherePredicateError(text)
    kind = match.lastgroup or ""
    raw = match.group(kind)
    return Token(kind, _value(kind, raw), raw, match.start(kind), match.end(kind))


def _skip_space(text: str, position: int) -> int:
    while position < len(text) and text[position].isspace():
        position += 1
    return position


def _value(kind: str, raw: str) -> Any:
    if kind == "literal":
        return unquote(raw)
    if kind == "number":
        return int(raw) if re.fullmatch(r"-?\d+", raw) else float(raw)
    return raw

FILE:src/sldb/store/graph/payload_match.py
"""Facet filters of a `StructuredQuery`, evaluated by the predicate language (GO05).

Each `FieldCondition` is translated to the language (`FieldCondition.predicate()`, rules-
language.md §7) and evaluated on the facet's fields; a null value is an absent field, as in a
projection (GO04). On the `payload` facet (a document node's projected fields): an absent
field only satisfies `is_null`; a list's `contains` is membership and its `eq`/`ne` compare
the whole list (Python equality, no coercion); a comparison Python cannot make is false. Only
document nodes carry the facet: any other node matches no payload filter.
"""

from __future__ import annotations

from typing import Any

from sldb.store.edge_index.node_ids import kind
from sldb.store.graph.facet_match import facet_value, resolve_field
from sldb.store.graph.language.predicate_documents import payload_holds

PAYLOAD = "payload"


def filters_hold(node, filters: list) -> bool:
    """Whether a node matches every facet filter of a query."""
    return all(_filter_holds(node, facet_filter) for facet_filter in filters)


def payload_matches(node, facet_filter) -> bool:
    """Whether a document node's projection satisfies every condition of the filter."""
    if kind(node.id) != "document":
        return False
    return all(payload_condition(node.payload, condition) for condition in facet_filter.conditions)


def payload_condition(payload: dict, condition) -> bool:
    """One FieldCondition over a projected payload, through the language."""
    present = {key: value for key, value in payload.items() if value is not None}
    return payload_holds(condition.predicate(), present)


def unprojected_fields(payload_fields: dict[str, list[str]], filters: list) -> list[str]:
    """Fields a payload filter names that no model projects, in the order named."""
    known = {f for fields in payload_fields.values() for f in fields}
    named = [c.field for f in filters if f.facet == PAYLOAD for c in f.conditions]
    return [f for f in dict.fromkeys(named) if f not in known]


def _filter_holds(node, facet_filter) -> bool:
    if facet_filter.facet == PAYLOAD:
        return payload_matches(node, facet_filter)
    value = facet_value(node, facet_filter.facet)
    return all(payload_condition(_field_of(value, c.field), c) for c in facet_filter.conditions)


def _field_of(value: Any, field: str) -> dict[str, Any]:
    return {field: resolve_field(value, field)}

FILE:src/sldb/store/graph/facet_match.py
"""Facet and condition matching for the executor."""

from __future__ import annotations

from typing import Any


def matches_filters(node, filters: list) -> bool:
    """Whether a node matches every facet filter of a query."""
    return all(facet_matches(node, facet_filter) for facet_filter in filters)


def facet_matches(node, facet_filter) -> bool:
    """Whether a node matches every condition of one facet filter; `payload` is read with its
    own null and list rules (`payload_match`)."""
    if facet_filter.facet == "payload":
        from sldb.store.graph.payload_match import payload_matches

        return payload_matches(node, facet_filter)
    value = facet_value(node, facet_filter.facet)
    return all(condition_matches(value, condition) for condition in facet_filter.conditions)


def facet_value(node, facet: str) -> object:
    """The facet payload a filter reads: identity, semantics, a document's projected payload, or
    a carried facet."""
    if facet == "identity":
        return {"node_id": node.id, "node_type": node.node_type}
    if facet == "semantics":
        return node.semantics
    if facet == "payload":
        return node.payload
    return node.facets.get(facet)


def condition_matches(value: object, condition) -> bool:
    """Whether one facet field value satisfies one FieldCondition."""
    if condition.op == "is_null":
        return resolve_field(value, condition.field) is None
    if condition.op == "is_not_null":
        return resolve_field(value, condition.field) is not None
    return ordered_compare(resolve_field(value, condition.field), condition)


def ordered_compare(actual: Any, condition) -> bool:
    """Evaluate the value-comparing operators that are not the null ones."""
    if condition.op == "eq":
        return actual == condition.value
    if condition.op == "ne":
        return actual != condition.value
    if condition.op == "contains":
        return isinstance(actual, list) and condition.value in actual
    if condition.op == "starts_with":
        return isinstance(actual, str) and actual.startswith(condition.value)
    return ordered_magnitude(actual, condition)


def ordered_magnitude(actual: Any, condition) -> bool:
    """Evaluate the greater-than and less-than operators."""
    if condition.op == "gt":
        return actual is not None and actual > condition.value
    if condition.op == "lt":
        return actual is not None and actual < condition.value
    return False


def resolve_field(value: object, field: str) -> Any:
    """Read a field from a facet payload: dict, list, or attribute-addressable object."""
    if value is None:
        return None
    if isinstance(value, list):
        return first_field(value, field)
    return read_field(value, field)


def first_field(values: list, field: str) -> Any:
    """The first non-null field value across a list payload."""
    for item in values:
        resolved = read_field(item, field)
        if resolved is not None:
            return resolved
    return None


def read_field(value: object, field: str) -> Any:
    """Read one field from a dict or attribute-addressable object."""
    if isinstance(value, dict):
        return value.get(field)
    return getattr(value, field, None)

FILE:src/sldb/store/graph/__init__.py
"""The graph layer: contracts, query language, executor, neighborhood,
portable snapshots and the semantic-export ingest route — all on top of the edge index."""

from sldb.store.graph.edge import Edge
from sldb.store.graph.executor import execute_query
from sldb.store.graph.facet import FacetPayload
from sldb.store.graph.graph_io import load_graph, save_graph
from sldb.store.graph.identity import SystemIdentity
from sldb.store.graph.ingest_sldb import sldb_semantic_export_to_snapshot
from sldb.store.graph.language import FacetFilter, FieldCondition, GraphScope, RelationFilter, StructuredQuery
from sldb.store.graph.neighborhood import collect_neighborhood, collect_neighborhood_by_direction
from sldb.store.graph.node import KnowledgeNode
from sldb.store.graph.node_view import GraphNode
from sldb.store.graph.query_result import QueryResult
from sldb.store.graph.snapshot import GraphSnapshot
from sldb.store.graph.vocabulary import VocabularyTerm

__all__ = [
    "Edge",
    "FacetFilter",
    "FacetPayload",
    "FieldCondition",
    "GraphNode",
    "GraphScope",
    "GraphSnapshot",
    "KnowledgeNode",
    "QueryResult",
    "RelationFilter",
    "StructuredQuery",
    "SystemIdentity",
    "VocabularyTerm",
    "collect_neighborhood",
    "collect_neighborhood_by_direction",
    "execute_query",
    "load_graph",
    "save_graph",
    "sldb_semantic_export_to_snapshot",
]

FILE:src/sldb/core/exceptions/__init__.py
from .sldb_error import SLDBError
from .sldb_model_error import SLDBModelError
from .sldb_model_draft_error import SLDBModelDraftError
from .sldb_model_edit_error import SLDBModelEditError
from .sldb_validation_error import SLDBValidationError
from .sldb_store_error import SLDBStoreError
from .sldb_conflict_error import ConflictError
from .sldb_ast_error import SLDBASTError
from .sldb_link_error import SLDBLinkError
from .sldb_payload_save_error import SLDBPayloadSaveError
from .sldb_graph_cycle_error import SLDBGraphCycleError
from .sldb_field_path_error import SLDBFieldPathError
from .sldb_field_type_error import SLDBFieldTypeError
from .sldb_document_target_error import SLDBDocumentTargetError
from .sldb_ambiguous_selection_error import AmbiguousSelectionError
from .sldb_graph_argument_error import SLDBGraphArgumentError
from .sldb_rule_violation_error import SLDBRuleViolationError

__all__ = [
    "SLDBError",
    "SLDBModelError",
    "SLDBModelDraftError",
    "SLDBModelEditError",
    "SLDBValidationError",
    "SLDBStoreError",
    "ConflictError",
    "SLDBASTError",
    "SLDBLinkError",
    "SLDBPayloadSaveError",
    "SLDBGraphCycleError",
    "SLDBFieldPathError",
    "SLDBFieldTypeError",
    "SLDBDocumentTargetError",
    "AmbiguousSelectionError",
    "SLDBGraphArgumentError",
    "SLDBRuleViolationError",
]

FILE:src/sldb/core/finding.py
"""What a command reports besides its output: an error or an alert (docs/architecture/anchoring.md, §4).

An **error** is something broken or a violated contract, and fails the command. An **alert**
is a source that moved against what was recorded: the state is valid, the command exits 0,
and the alert is never silent (`sldb.cli.alert_sink` prints it by every route). A **warning**
is a deprecated use (GO05: `FieldCondition` in `sldb graph query`): it travels with the alerts.
"""

from __future__ import annotations

from dataclasses import asdict, dataclass
from typing import Literal

Level = Literal["error", "alert", "warning"]


@dataclass(frozen=True)
class Finding:
    """One finding: its level, a stable `ns/name` code, whose it is, what moved, what to do."""

    level: Level
    code: str
    subject: str
    what: str
    fix: str = ""
    document: str | None = None

    def as_dict(self) -> dict:
        return asdict(self)

    def line(self) -> str:
        return f"{self.level}: [{self.code}] {self.subject}: {self.what}"


def alert(code: str, subject: str, what: str, fix: str = "", document: str | None = None) -> Finding:
    return Finding("alert", code, subject, what, fix, document)


def error(code: str, subject: str, what: str, fix: str = "", document: str | None = None) -> Finding:
    return Finding("error", code, subject, what, fix, document)


def split(findings: list[Finding]) -> tuple[list[Finding], list[Finding]]:
    """`(errors, alerts)`, each in the order given."""
    return [f for f in findings if f.level == "error"], [f for f in findings if f.level == "alert"]

FILE:src/sldb/cli/commands/graph.py
"""`sldb graph` handlers: thin printing wrappers over `sldb.api`'s graph functions."""

from __future__ import annotations

import json
import warnings
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
from sldb.cli import alert_sink
from sldb.cli.commands.graph_analysis import GraphAnalysisCLI
from sldb.core.finding import Finding
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
        with warnings.catch_warnings():  # the deprecation travels in the envelope's warnings
            warnings.simplefilter("ignore", DeprecationWarning)
            query = StructuredQuery.model_validate(json.loads(Path(args.query_file).read_text(encoding="utf-8")))
        _warn_field_conditions(query)
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


def _warn_field_conditions(query: StructuredQuery) -> None:
    """A query with `FieldCondition` filters reports the deprecation (GO05 p1, p12): one
    `warning` in the envelope naming the predicate that replaces them; the output is unchanged."""
    predicates = [c.predicate().text for f in query.filters for c in f.conditions]
    if not predicates:
        return
    what = "FieldCondition is deprecated; write the predicate instead: " + " and ".join(predicates)
    alert_sink.report([Finding("warning", "deprecated/field-condition", "graph query", what, "docs/architecture/rules-language.md")], text=False)

FILE:src/sldb/api/__init__.py
"""sldb's library API: the store, model and document operations the CLI performs, as functions.

Consumers (pron, deskops, graph_ui...) call these instead of instantiating `sldb.cli` command
classes with fake argparse namespaces. Each operation that names a store opens it the way a
CLI command does (`open_store`), returns a pydantic model instead of printing, and raises
`sldb.core.exceptions` errors instead of exiting. Layering: `sldb.cli` -> `sldb.api` ->
`sldb.store` / `sldb.runtime` / `sldb.core`; nothing here imports `sldb.cli`.
"""

from __future__ import annotations

from sldb.api.anchors.check_doc_anchors import check_doc_anchors
from sldb.api.documents.apply_batch import apply_batch
from sldb.api.documents.batch_report import BatchReport
from sldb.api.documents.create_document import create_document
from sldb.api.documents.delete_document import delete_document
from sldb.api.documents.move_document import move_document
from sldb.api.documents.transaction import RollbackError, Transaction, transaction
from sldb.api.documents import document_ast, build_document_ir_json, leaf_paths, runtime_document, extract_document_payload, render_document_markdown, render_model_template
from sldb.api.documents.runtime_documents import load_runtime_documents
from sldb.api.documents.select_documents import select_documents
from sldb.api.documents.selector import Selector
from sldb.api.documents.document_reference import DocumentReference
from sldb.api.documents.document_serialization import serialize_document
from sldb.api.documents.payload_path_reading import deep_get, ensure_list
from sldb.api.documents.payload_path_writing import deep_delete, deep_set
from sldb.api.documents.payload_save import save_document_payload
from sldb.api.documents.track_document_file import track_document_file
from sldb.api.documents.untrack_document import untrack_document
from sldb.api.edges.check_edges import check_edges
from sldb.api.edges.edge_check_report import EdgeCheckReport
from sldb.api.edges.edge_reading import edge_node, edge_nodes_of_type, edges_from, edges_to, load_edge_index
from sldb.api.edges.apply_effects import apply_effects
from sldb.api.edges.edge_effects import effects_of
from sldb.api.edges.edges_blocked import edges_blocked
from sldb.api.edges.edges_holding import edges_holding
from sldb.api.model_registry.remove_model import remove_model
from sldb.api.model_registry.inherit_model import inherit_model
from sldb.models.structured_doc import StructuredNLDoc
from sldb.models.notation_models import (
    GlyphDoc,
    LinkDoc,
    NotationDoc,
    PaletteDoc,
    SpecDoc,
    SpecNodeDoc,
    ViewDoc,
)
from sldb.api.notations import (
    evaluate_projection_view,
    list_projection_views,
    resolve_documents,
    resolve_view,
    save_projection_view,
    sync_notation,
    sync_palette,
)
from sldb.api.edges.unresolved_references import unresolved_references
from sldb.store.edge_index.unresolved_reference import UnresolvedReference
from sldb.api.edges.edge_serialization import serialize_edge_node_record, serialize_edge_node_records, serialize_edge_record, serialize_edge_records
from sldb.api.edges.init_relations import init_relations
from sldb.api.edges.rebuild_edges import rebuild_edges
from sldb.api.edges.relations_init_report import RelationsInitReport
from sldb.api.journal import journal, verify_journal
from sldb.api.model_drafts.draft_document_check import DraftDocumentCheck
from sldb.api.model_drafts.draft_validation import promote_model_draft, validate_model_draft
from sldb.api.model_drafts.draft_validation_report import DraftValidationReport
from sldb.api.model_drafts.field_drafts import add_model_field, remove_model_field
from sldb.api.model_drafts.model_draft import ModelDraft
from sldb.api.model_drafts.model_source import ModelSource
from sldb.api.model_drafts.source_location import locate_model_source
from sldb.api.model_drafts.template_drafts import edit_model_template
from sldb.api.model_drafts.metadata_drafts import edit_model_metadata
from sldb.api.model_create.create_model import create_model
from sldb.api.model_create.field_decl import FieldDecl
from sldb.api.model_create.model_check import ModelCheck
from sldb.api.model_registry.add_model import add_model
from sldb.api.search import search
from sldb.api.rules import on_check_findings, refuse_unknown_family, rules_check, rules_explain, rules_on_check, transition_findings
from sldb.api.where import where_matches
from sldb.store.query_engine.where_parse import WherePredicateError
from sldb.core.exceptions import AmbiguousSelectionError, ConflictError
from sldb.api.model_registry.describe_model import describe_model
from sldb.api.model_registry.load_registered_model import load_registered_model
from sldb.api.model_registry.model_description import ModelDescription
from sldb.api.model_registry.model_document_summary import ModelDocumentSummary
from sldb.api.model_registry.model_field_summary import ModelFieldSummary
from sldb.api.model_registry.model_reference import resolve_model_ref
from sldb.api.model_registry.model_registration import ModelRegistration
from sldb.api.model_registry.registered_model import RegisteredModel
from sldb.api.model_registry.reindex_model import reindex_model
from sldb.api.schema.describe_field import describe_field, describe_model_fields
from sldb.api.schema.field_description import FieldDescription
from sldb.api.segments import CompositionPiece, CompositionSpec, DocumentSegments, FieldSegment, LiteralSegment, Segment, SourceRef, build_document_segments
from sldb.api.stores.doc_ref import split_doc_ref
from sldb.api.stores.doc_ref_status import DocRefStatus
from sldb.api.stores.doc_status import doc_exists, doc_status
from sldb.api.stores.tracked_documents import tracked_documents
from sldb.api.stores.ambiguous_document import AmbiguousDocument
from sldb.api.stores.build_store import build_store
from sldb.api.stores.scaffold_report import ScaffoldReport
from sldb.api.stores.scaffold_store import scaffold_store
from sldb.api.stores.seed import Seed
from sldb.api.stores.store_declaration import StoreDeclaration
from sldb.api.stores.resolve_indexed_document import indexed_model_bases, resolve_indexed_document
from sldb.api.stores.init_store import init_store
from sldb.api.stores.link_store import link_store
from sldb.api.stores.unlink_store import unlink_store
from sldb.api.model_registry.registration_query import is_model_registered, registered_models
from sldb.api.stores.linked_store import LinkedStore
from sldb.api.stores.migrate_hash_names import migrate_store_hash_names
from sldb.api.stores.open_store import open_store
from sldb.api.stores.store_check import check_store
from sldb.api.stores.store_fingerprint import store_fingerprint
from sldb.api.stores.store_links import store_links
from sldb.api.stores.store_location import StoreLocation
from sldb.api.stores.store_update_report import StoreUpdateReport
from sldb.api.stores.update_store_indexes import update_store_indexes
from sldb.store.edge_index.edge_index import EdgeIndex
from sldb.store.edge_index.edge_rebuild_report import EdgeRebuildReport
from sldb.store.edge_index.node_ids import anchor_node_id, bare, doc_node_id, field_node_id, kind, model_node_id, relation_type_node_id, section_node_id, tag_node_id
from sldb.store.journal import JournalEntry, JournalVerifyReport
from sldb.store.models.edge_node_record import EdgeNodeRecord
from sldb.store.models.edge_record import EdgeRecord
from sldb.store.models.document_hashes import DocumentHashes
from sldb.store.models.store_fingerprint import StoreFingerprint
from sldb.api.corpus import (
    Corpus,
    CorpusEntry,
    FieldEntry,
    FieldHit,
    FieldProjection,
    Hit,
    IndexProjection,
    field_id,
    split_field_id,
)

__all__ = [
    "Corpus", "CorpusEntry", "FieldEntry", "FieldHit", "FieldProjection",
    "Hit", "IndexProjection", "field_id", "split_field_id",
    "CompositionPiece", "CompositionSpec", "DocumentSegments", "FieldSegment",
    "LiteralSegment", "Segment", "SourceRef", "build_document_segments",
    "DocumentHashes", "DocumentReference", "DraftDocumentCheck", "DraftValidationReport",
    "EdgeCheckReport", "EdgeIndex", "EdgeNodeRecord", "EdgeRebuildReport",
    "EdgeRecord", "FieldDecl", "FieldDescription", "JournalEntry",
    "JournalVerifyReport", "LinkedStore", "ModelCheck", "ModelDescription",
    "ModelDocumentSummary", "ModelDraft", "ModelFieldSummary", "ModelRegistration",
    "ModelSource", "RegisteredModel", "RelationsInitReport", "StoreFingerprint",
    "StoreLocation", "StoreUpdateReport", "add_model", "add_model_field",
    "create_model", "anchor_node_id", "bare", "check_doc_anchors", "check_edges", "check_store",
    "store_fingerprint", "create_document", "deep_delete", "deep_get", "deep_set",
    "delete_document", "describe_field", "describe_model", "describe_model_fields",
    "doc_node_id", "document_ast", "edge_node", "edge_nodes_of_type", "edges_from",
    "edges_to", "edit_model_metadata", "edit_model_template", "ensure_list", "extract_document_payload",
    "field_node_id", "init_relations", "init_store", "journal", "kind", "link_store", "unlink_store",
    "load_edge_index", "leaf_paths", "load_runtime_documents", "migrate_store_hash_names",
    "load_registered_model", "locate_model_source", "model_node_id", "open_store",
    "promote_model_draft", "rebuild_edges", "reindex_model", "relation_type_node_id",
    "remove_model_field", "render_document_markdown", "render_model_template",
    "resolve_model_ref", "runtime_document", "save_document_payload", "search",
    "section_node_id", "serialize_document", "serialize_edge_node_records",
    "serialize_edge_records", "tag_node_id", "track_document_file", "untrack_document",
    "update_store_indexes", "validate_model_draft", "verify_journal",
    "AmbiguousSelectionError", "Selector", "select_documents",
    "DocRefStatus", "doc_exists", "doc_status", "tracked_documents", "AmbiguousDocument", "indexed_model_bases", "resolve_indexed_document", "split_doc_ref", "store_links",
    "WherePredicateError", "apply_effects", "edges_blocked", "edges_holding", "effects_of", "on_check_findings", "refuse_unknown_family", "rules_check", "rules_explain", "rules_on_check", "transition_findings", "remove_model", "where_matches", "inherit_model", "is_model_registered", "registered_models",
    "StructuredNLDoc", "UnresolvedReference", "unresolved_references",
    "BatchReport", "ConflictError", "RollbackError", "Transaction", "apply_batch", "move_document", "transaction",
    "ScaffoldReport", "Seed", "StoreDeclaration", "build_store", "scaffold_store",
    "GlyphDoc", "LinkDoc", "NotationDoc", "PaletteDoc", "SpecDoc", "SpecNodeDoc", "ViewDoc",
    "resolve_view", "resolve_documents", "evaluate_projection_view", "list_projection_views", "save_projection_view", "sync_notation", "sync_palette",
]

FILE:src/sldb/api/graph/__init__.py
"""The graph layer as a library: query, traverse, analyse, and the portable snapshot format."""

from sldb.api.graph.analyze import (
    graph_central,
    graph_components,
    graph_cycles,
    graph_islands,
    graph_isolated,
    graph_layers,
    graph_order,
    graph_path,
    graph_paths,
    graph_similar,
)
from sldb.api.graph.execute import execute_query, graph_get, graph_list, query_snapshot
from sldb.api.graph.neighborhood import collect_neighborhood, collect_neighborhood_by_direction
from sldb.api.graph.snapshot import ingest_sldb, snapshot_load, snapshot_save
from sldb.api.graph.traverse import (
    bare,
    children,
    descendants,
    exists,
    kind,
    neighbors_via,
    parent,
    roots,
    sources,
    targets,
)
from sldb.store.graph.convert import index_from_snapshot, snapshot_from_index
from sldb.store.graph.graph_io import load_graph, save_graph
from sldb.store.graph.ingest_sldb import sldb_semantic_export_to_snapshot
from sldb.store.graph.language import FacetFilter, FieldCondition, GraphScope, RelationFilter, StructuredQuery
from sldb.store.graph.edge import Edge
from sldb.store.graph.identity import SystemIdentity
from sldb.store.graph.node import KnowledgeNode
from sldb.store.graph.node_view import GraphNode
from sldb.store.graph.query_result import QueryResult
from sldb.store.graph.snapshot import GraphSnapshot

FILE:src/sldb/api/notations/__init__.py
"""Notations and projection views API for SLDB."""

from __future__ import annotations

from sldb.api.notations.notation_sync import (
    NotationSync,
    PaletteSync,
    SyncReport,
    sync_notation,
    sync_palette,
)
from sldb.api.notations.notation_view import (
    FRAGMENT_KINDS,
    ViewError,
    flatten,
    fragment_kind,
    fragments_of,
    link_order,
    lookup,
    matches,
    render_keyword,
    render_template,
    resolve_documents,
    resolve_view,
)
from sldb.api.notations.projection_view import (
    evaluate_projection_view,
    list_projection_views,
    node_id,
    save_projection_view,
)

__all__ = [
    "resolve_view",
    "resolve_documents",
    "evaluate_projection_view",
    "list_projection_views",
    "save_projection_view",
    "sync_notation",
    "sync_palette",
    "ViewError",
    "SyncReport",
    "PaletteSync",
    "NotationSync",
    "flatten",
    "lookup",
    "render_template",
    "render_keyword",
    "matches",
    "link_order",
    "fragments_of",
    "fragment_kind",
    "FRAGMENT_KINDS",
    "node_id",
]

# `sldb.notations` es vocabulario (capa 0) y no puede importar `sldb.api`: le conectamos el parser.
from sldb.api.where import where_matches as _where_matches
from sldb.notations.where_check import set_where_parser as _set_where_parser

_set_where_parser(lambda expression: _where_matches(expression, {}))

FILE:src/sldb/notations/where_check.py
"""Comprobacion de que un `where` parsea: un puerto que `sldb.api.notations` conecta al parser."""

from __future__ import annotations

from typing import Callable

_parser: Callable[[str], object] | None = None


def set_where_parser(parser: Callable[[str], object] | None) -> None:
    """Conecta (o desconecta) el parser de `where`; sin parser no se comprueba."""
    global _parser
    _parser = parser


def _check_where(expression: str) -> None:
    """Un `where` tiene que parsear en la gramatica de sldb; sin parser conectado no se comprueba."""
    if not expression or _parser is None:
        return
    try:
        _parser(expression)
    except Exception as exc:  # WherePredicateError y afines
        raise ValueError(f"where {expression!r} does not parse: {exc}") from exc

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
paths = ["core/exceptions", "store/exceptions.py", "core/finding.py"]
external = []
does = "la jerarquía de excepciones del sistema, y el hallazgo (error o alerta) que reporta un comando"
identity = false
note = "la capa más baja que todas las demás necesitan nombrar; por eso R2 importaba"

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
id = "dos-lenguajes-de-consulta"
between = ["consulta", "grafo"]
what = """
`store/query_engine/where_parse.py` usa `=`, `!=`, `<=`, `>=`.
`store/graph/language/field_condition.py` usa `eq`, `ne`, `lt`, `gt`, `contains`,
`starts_with`, `is_null`, `is_not_null`.

Dos vocabularios para filtrar por campo. No es código duplicado: son dos
lenguajes que alguien tiene que aprender por separado para hacer lo mismo en dos
ejes, y un cambio en uno no llega al otro.
"""
repair = "un solo lenguaje de condiciones, compartido por los dos ejes"

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
parsea es un PUERTO (`where_check.set_where_parser`) que `api/notations` conecta al
parser del almacén; sin él no se comprueba, igual que cuando vivía fuera de sldb.
"""

[[axis]]
id = "vistas"
paths = ["api/notations"]
external = []
does = "resolver una notación sobre documentos del almacén y evaluar vistas de proyección; sincronizar notaciones y paletas (SV02)"
identity = false

[[unit]]
id = "nucleo"
axes = ["superficie", "representacion", "render", "contrato", "runtime", "identidad_y_hash", "errores", "codigo"]
needs = 4  # medido 2026-11-06 tras SV01/SV02: models reexporta notation_models; antes 3/35
needed_by = 39  # medido 2026-11-06 tras SV01/SV02: models reexporta notation_models; antes 3/35
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
needs = 19  # medido 2026-11-06 tras GO04 y SV02; antes 16/35
needed_by = 36  # medido 2026-11-06 tras GO04 y SV02; antes 16/35
why = "el centro de gravedad del sistema: 110 aristas entran desde los ejes de operación"

[[unit]]
id = "grafo"
axes = ["grafo"]
needs = 5  # GO03: eval de store/graph/backend reutiliza el parser where de store/query_engine
needed_by = 4  # GO05: consulta (query_engine.rules y los shims where_parse/where_subject) usa el lenguaje de store/graph/language
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
needs = 5
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
needs = 3  # medido 2026-11-06
needed_by = 2  # medido 2026-11-06
indivisible = false
why = """
Lo que spec2viz hacía fuera del repositorio, adentro: el vocabulario (capa 0) y
el resolvedor (capa 3) son una capacidad con una superficie propia (`sldb
notations`, `/notations/*`, `/views/projection*`). Las cuentas las dice la puerta.
"""

[[non_unit]]
id = "operacion"
axes = ["op_almacen", "op_documentos", "op_modelos", "op_aristas", "anclaje"]
needs = 47  # medido 2026-11-06 tras SV02: api/notations la necesita; antes 47/8
needed_by = 9  # medido 2026-11-06 tras SV02: api/notations la necesita; antes 47/8
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
needs = 2
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

FILE:contracts/queries/sldb/sections_for_taskdoc_document.json
{
  "scope": {
    "descendant_of": "sldb://document/TaskDoc:001-define-kgdb-semantic-export-payload"
  },
  "filters": [
    {
      "facet": "identity",
      "conditions": [
        {
          "field": "node_type",
          "op": "eq",
          "value": "sldb_section"
        }
      ]
    }
  ]
}

FILE:contracts/queries/sldb/semantic_neighborhood_integration_kgdb.json
{
  "scope": {
    "descendant_of": "sldb://semantic_tag/integration.kgdb"
  },
  "filters": [
    {
      "facet": "identity",
      "conditions": [
        {
          "field": "node_type",
          "op": "eq",
          "value": "semantic_tag"
        }
      ]
    }
  ]
}

FILE:contracts/queries/sldb/documents_tagged_domain_contract.json
{
  "scope": {
    "ancestor_of": "sldb://semantic_tag/domain.contract"
  },
  "filters": [
    {
      "facet": "identity",
      "conditions": [
        {
          "field": "node_type",
          "op": "eq",
          "value": "sldb_document"
        }
      ]
    }
  ]
}

FILE:contracts/queries/sldb/documents_near_domain_workflow_task_tag.json
{
  "scope": {
    "ancestor_of": "sldb://semantic_tag/domain.workflow.task"
  },
  "filters": [
    {
      "facet": "identity",
      "conditions": [
        {
          "field": "node_type",
          "op": "eq",
          "value": "sldb_document"
        }
      ]
    }
  ]
}

FILE:contracts/queries/sldb/documents_near_taskdoc_model.json
{
  "scope": {
    "descendant_of": "sldb://model/TaskDoc"
  },
  "filters": [
    {
      "facet": "identity",
      "conditions": [
        {
          "field": "node_type",
          "op": "eq",
          "value": "sldb_document"
        }
      ]
    }
  ]
}

FILE:docs/architecture/graph-backend.md
# GraphBackend: the seam under every graph analysis

Estado (2026-11-05): contrato del nodo GO03 del plan
`desk/drawer/plans/grafo-operable` (gate G_SEAM). Fija la costura `GraphBackend` sobre
networkx. Cualquier motor futuro —Kùzu, Neo4j, Datalevin— entra detrás de esta costura; las
reglas y los comandos no lo ven. La semántica de los predicados vive en
[`rules-language.md`](rules-language.md); la proyección llegó en GO04 y el evaluador
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
  sin ese id, `eval` levanta `ValueError("sin proyección para <id>")`. Sin sujeto, evalúa
  el dominio entero (sección «eval» más abajo).
- **`analyze`** responde una pregunta de grafo completo con los argumentos que las
  operaciones ya reciben. Hoy son las diez de `sldb.api.graph.analyze`: `path`, `paths`,
  `cycles`, `order`, `layers`, `components`, `islands`, `isolated`, `central` y `similar`;
  las seis de la CLI (`path`, `cycles`, `order`, `components`, `central`, `similar`) son el
  subconjunto que el contrato del nodo nombra.

El backend **nunca expone su grafo interno**. Se guarda en un atributo privado y las
operaciones lo usan dentro; no hay accesor público ni fuga del `MultiDiGraph` de networkx.

La implementación actual, `NetworkXBackend`, envuelve `sldb.store.graph.analysis` sin
cambiar ninguna respuesta.

## eval (GO03, completo desde GO05)

Evalúa el lenguaje entero de [`rules-language.md`](rules-language.md): booleanos, caminos
(`campo`, `rel:<tipo>`, `^`, clausura `+`), cuantificadores `any`/`all`/`none`, `count`,
sustitución `{campo}` desde el sujeto e `incomplete` en el borde de links. El predicado llega
como texto (se parsea, `WherePredicateError` si no parsea) o ya parseado (`Predicate`, de
`sldb.store.graph.language`).

`NetworkXBackend` arma sobre el índice cargado la vista mínima del lenguaje
(`backend/index_view.py`): los documentos por `export_id`, su payload (la proyección de
`load`, o la que el shard lleva), su familia (`base_models` de los nodos de modelo,
transitivamente) y las aristas del índice (`field` y `declared` de `metadata`; `unavailable`
marca un elemento `incomplete`). El mismo evaluador corre sobre el grafo de los tests
(`eval_predicate`) y da los mismos findings.

- **Con sujeto** (payload o `export_id`): un finding. Un `export_id` sin proyección cargada
  sigue siendo `ValueError("sin proyección para <id>")`.
- **Sin sujeto:** un finding por documento del dominio (`rules-language.md` §6): los de la
  proyección cargada, o todos los nodos de documento del índice si `load` recibió `None`.
- Al atravesar un campo `F` del origen cuyo payload trae `F__anchor_state`, cada elemento
  alcanzado expone esa entrada como `anchor_state` (lista: el elemento `i`; escalar: el valor).
  Al atravesar `^F`, la entrada se lee del elemento alcanzado, que es el que tiene el campo `F`
  (GO07: `any(^subject: anchor_state = "intact")` desde el sujeto de una Review).

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
evalúa sobre lo que dice el shard: nunca se re-extrae un documento. Desde GO05 cada
`FieldCondition` (deprecado) se traduce al lenguaje por la tabla de `rules-language.md` §7 y
lo evalúa el mismo evaluador; por eso `contains` sobre una cadena es subcadena e `is_null` /
`is_not_null` tratan `""` como ausente. Solo los nodos de documento
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

FILE:docs/architecture/rules-language.md
# Lenguaje de reglas de sldb

Estado (2026-11-06): contrato de semántica del nodo GO02 del plan
`desk/drawer/plans/grafo-operable`, implementado por GO05. Fija la gramática, los caminos,
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
- **H13. `doc ~ "re"`.** Como el `~` de `where_parse`, `doc ~` lee el nombre del documento
  (no un campo `doc`).
- **H14. Ausencia en comparaciones.** Un campo ausente no cumple ninguna comparación, `in`
  ni `~`, con literal de cadena o de número. `where_parse` dejaba cumplir `f != <número>`
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
  arista) y `StructuredQuery` (cada `FieldCondition` se traduce por la tabla de la sección 7).
- **CLI:** `sldb find ... --where <expr>` usa el lenguaje: un documento cumple solo si `holds`
  es `true`; un camino recorre el índice del store. `--explain` agrega a `data` la clave
  `findings`, un finding por documento evaluado (cumpla o no). Los registros de campo y de
  sección conservan su lectura propia de `--where`. `sldb --envelope graph query` con filtros
  `FieldCondition` lleva en `warnings` un `{level: "warning", code:
  "deprecated/field-condition", subject: "graph query", what: <el predicado de reemplazo>}`.
- **Shims (GO10 los retira):** `where_parse.compile_where` y `where_parse.where_parse`
  delegan en el lenguaje y emiten `DeprecationWarning`; construir un `FieldCondition` también.
  `--where` nunca avisa.
- **Equivalencia:** `tests/fixtures/where_goldens/` guarda el resultado de cada fila de la
  sección 7 con el código anterior a GO05; `tests/store/test_predicate_language.py` compara.
  Diferencias declaradas: fila 7 con número sobre campo ausente (H14), fila 16 (`in` también
  es subcadena), filas 18 y 19 (`has` rechaza `""`).

FILE:docs/architecture/superseded-code-audit.md
# Auditoría de código superseded en `src/sldb/`

Inventario con evidencia, sin refactor y sin borrar nada. Complementa y extiende
[`edges-retirement-plan.md`](edges-retirement-plan.md): este documento cubre lo que el plan de
edges no tocó (kgdb↔sldb, islas muertas, compat bridges, derivados sections/semantic/cache).

> Nota 2026-10-18: el paquete externo `kgdb` ya no existe (fusionado en sldb, ver [sldb-absorbs-kgdb.md](sldb-absorbs-kgdb.md)). Las referencias a `kgdb` de este documento describen el estado al 2026-09-24; los tests de paridad contra kgdb se retiraron y sus ids esperados quedaron fijados en `tests/store/test_example_queries.py`. <!-- gone -->

- Base: `1d232ae`, rama `docs/superseded-audit`. <!-- gone -->
- Línea base de tests: `PYTHONPATH=src python -m pytest -q` → **1015 passed** (2026-09-24).
- Método: censo AST de importadores sobre `src/` + `tests/` (script propio, incluye imports
  relativos), greps dirigidos para cada símbolo sospechoso, diff entre pares duplicados.

Clasificación: **(i)** muerto de verdad, borrable · **(ii)** superseded con consumidores,
requiere migración · **(iii)** parece duplicado pero no lo es.

---

## 1. Inventario resumido

| # | Hallazgo | Evidencia (archivo:línea) | Lo que lo supersedió | Clase | Tamaño estimado del retiro |
|---|---|---|---|---|---|
| 1 | Capa `runtime/edges/` + sus lectores (la capa nueva lee a la vieja) | `store/edge_index/compose.py:21` (`compose_edge_index` → shards vía `shard_reading.read_store_contributions`, `compose.py:13,58`); `api/edges/edge_reading.py:14`; ver también [edges-retirement-plan.md §0](edges-retirement-plan.md) | `store/graph/` + snapshot portable: `store/export.py:18,43` (`sldb_kgdb_semantic_export` sin tocar edges) → `graph/ingest_sldb.py:20` (`sldb_semantic_export_to_snapshot`) → `cli/parsers/graph.py:70` (`graph ingest-sldb`) | i (capa) / ii (writes clase B, §4 del plan) | ≈ 1.613 líneas directas en 30+ módulos (ver §6.1) |
| 2 | `core/ingest/` completo: isla muerta e inimportable | 0 importadores: `grep -rn "core.ingest" src tests --include="*.py"` → vacío; `ingest/engine.py:3-8` importa `wiki_compiler`/`ontology`, no declarados en `pyproject.toml:21-28` ni instalados (import → `ModuleNotFoundError`); último toque `e83db87` | El ingestion real vive en `store/` (sync por shard, `store/semantic.py`, `store/section_sync.py`) y en `selfdoc/` (`selfdoc/python_scanner.py`); `wiki_compiler` era el producto anterior | i | 9 módulos, 328 líneas |
| 3 | `cli/graph/`: árbol sin `__init__.py`, sin importadores | No existe `cli/graph/__init__.py`; `grep -rnE "from sldb\.cli\.graph import|sldb\.cli\.graph\." src tests` → 0; código casi idéntico a `graph_old/` (`diff -r cli/graph cli/graph_old`); ambos nacidos en `73e4553` (refactor de subagente interrumpido) | `cli/graph_ops/` (único tree vivo: 22 importadores en `src`, p. ej. `commands/find.py:3`, `api/search.py:43-49`) + `cli/search_record.py` | i | 6 módulos, 134 líneas |
| 4 | `cli/graph_old/`: idem, con `__init__` roto | `graph_old/__init__.py:3-5` importa `.query`, `.search`, `.ast_target` que no existen → `import sldb.cli.graph_old` lanza `ModuleNotFoundError`; 0 importadores (`grep -rn "graph_old" src tests` → vacío) | ídem #3 | i | 4 módulos, 79 líneas |
| 5 | `cli/commands/doc_helpers.py`: muerto | `grep -rln "doc_helpers" src tests --include="*.py"` → **0 archivos** (ni el propio módulo se nombra) | Sus helpers (`parse_yaml_string`, `validate_and_render`) duplican `core.exceptions` + `runtime.validation` que los callers reales importan directo | i | 1 módulo, 100 líneas |
| 6 | `cli/commands/legacy.py` + `cli/parsers/legacy.py`: compat activa del "pre-redesign DSL" | `dispatcher.py:58-75` (docstring "pre-redesign spelling", alias `ls|get|glob|raw-find|recover|compose` registrados); `parsers/core.py:8,28`; `parsers/hidden.py:3-8` | El redesign: `QueryCLI`/`LinkCLI` a los que `legacy.py:5-18` re-despacha; el surface per se quedó para no romper el DSL viejo | ii (sus consumidores son el destino del alias, no código nuevo) | 2 módulos, 79 líneas |
| 7 | `cli/commands/model_update.py`: superseded, solo tests | Sin importadores en `src` (`grep -rn "model_update" src --include="*.py"` excl. self → vacío); único uso es `tests/test_cli_v2.py:1664` (monkeypatch sobre un módulo que la ruta real no importa: `models update` va por `commands/models.py:37-39` → `ModelCLI`, no por `model_update.update_model`) | `api/model_registry/reindex_model` + `commands/model.py` (`ModelCLI`) | i (src) — el monkeypatch del test es inerte | 1 módulo, 67 líneas |
| 8 | `cli/commands/predicates_format.py`: muerto | `grep -rn "predicates_format" src tests` → 0 | Formateo implementado inline en el CLI vivo (`cli/commands/predicates.py` no lo referencia) | i | 1 módulo, 42 líneas |
| 9 | Compat bridges sin consumidores: `cli/commands/model_source.py`, `cli/federated_utils.py` | Docstrings "Compatibility bridge" (`model_source.py:1-3`, `federated_utils.py:1-3`); 0 importadores (`grep -rn "commands.model_source\|federated_utils" src tests` → solo docstrings de "moved here" en `api/model_drafts/source_location.py:3` y `api/model_registry/federated_lookup.py:3`) | `api/model_drafts/source_location.py:resolve_definition`; `api/model_registry/federated_lookup.py` | i (todos los consumidores ya migraron) | 2 módulos, 21 líneas |
| 10 | `kgdb/contracts/persistence.py`: muerto en kgdb, **sin** duplicado en sldb | sldb no tiene `PersistenceEntry`/`TransactionManifest` (`grep -rn "PersistenceEntry" src` → vacío); en kgdb solo lo exporta `contracts/__init__.py:10,13`; nadie lo importa (kgdb src, pron, deskops) | El contrato de persistencia de grafo murió con la fusión: no existe "before/after" durable del grafo en sldb | i (kgdb-side, se retira con el shim) | 55 líneas |
| 11 | 4 importaciones sldb→kgdb (el ciclo) | `core/ingest/scanner.py:5-6`, `core/ingest/python_scanner.py:4`, `core/ingest/typescript_scanner.py:3-4` — las 4 dentro del árbol muerto #2 | Nada: kgdb hoy solo debería importar sldb (shims) | i (mueren con #2) | 4 líneas de import |
| 12 | `api/__init__.py`: 47 de 76 símbolos del surface sin importadores internos | Censo: sin `from sldb.api import X` en src/tests para `load_edge_index`, `edge_node(s_of_type)`, `edges_from/to`, `check_edges`, `journal`, `verify_journal`, node-id helpers (`doc_node_id`…), `delete_document`, `deep_set/delete`, `ensure_list`, serializers de edges, reportes pydantic, etc. | Contrato público declarado (`api/__init__.py:3-7`: "Consumers (pron, kgdb, deskops...)"), así que NO es muerto — pero el 100% de los símbolos de edges que exporta muere con #1 (listados ya en el plan, `api/__init__.py:22-28,62-65`) | iii (contrato) / ii (los símbolos de edges) | poda de `__all__` al retirar #1 |
| 13 | `runtime/sections/`, `runtime/semantic/`: **no** hay formato duplicado | `store/io/sections_index.py:8-12` ("no longer written to (PLAN 15 capa 5), still the key"); `semantic_index.py:26-30` (compone shards, legado solo si no hay shards) y `:40-46` (save shardea y unlinkea el legacy); `store/migration.py:69` (`migrate_store_layout`, convertidor vivo, llamado desde `api/stores/open_store.py:36-38`) | En edges el shard-per-doc es lo *viejo*; en sections/semantic el shard-per-doc es lo *nuevo* (PLAN 15 capa 5). Lo único "viejo" es el fallback de lectura para stores no migrados (`sections_index.py:33-37`, `semantic_index.py:26-30`), que `migration.py` elimina en la próxima apertura | iii — no duplicado; el fallback es transitorio y se va solo con la migración | 0 (no retirar) |
| 14 | `runtime/cache/`: dos archivos JSON, **no** dos formatos del mismo dato | `runtime_cache_disk.py:12-14` (`extracted.json`: payloads extraídos, clave por leaf + hash_b) vs `built_cache.py:7-8` (`built.json`: resultados derivados por modelo, clave por hash_b) | Son dos caches distintos (misma filosofía de clave, distinto contenido), cada una en un único formato, ambas derivadas y borrables (`runtime_cache_disk.py:5-7`) | iii | 0 (no retirar) |
| 15 | Analisis de grafo reimplementado a mano fuera de `store/graph/analysis` | No queda: `analysis/` (7 módulos nx) es la única casa (`cli/commands/graph_analysis.py:25`); `edge_index/acyclic.py:11` ya reusa `graph.analysis.cycles`; `graph/executor.py:18` y `neighborhood.py` hacen BFS propio sobre `EdgeIndex` — es la capa de query, no análisis | networkx (`pyproject.toml:28`) | iii | 0 |
| 16 | Parsers/serializadores duplicados entre `core/` y `store/` | No hay: `query_engine/where_parse.py:1-5` es la única gramática `--where` (usada por `cli/commands/find.py:6`, `query_engine/{structural_queries,filter,semantic}.py`, `api/search.py:31`); `core/renderer_engine/yaml.py` es renderizado, `store/io/utils.py` es serialización de índices — no coinciden | — | iii | 0 |

---

## 2. El ciclo kgdb↔sldb

Estado real de los imports entre los dos repos, hoy:

1. **La dirección correcta (kgdb → sldb) ya está instalada.** Los tres shims son re-exports:
   `kgdb/contracts/node.py:7`, `io.py:5`, `base.py:5` importan desde `sldb.store.graph`
   (`KnowledgeNode` vive en `sldb/store/graph/node.py:12`, re-exportado en
   `store/graph/__init__.py:12`).
2. **El ciclo (sldb → kgdb) existe en 4 sitios y todos están dentro de un árbol muerto.**
   `core/ingest/scanner.py:5-6`, `python_scanner.py:4`, `typescript_scanner.py:3-4` importan
   desde el shim un tipo que vive en el propio sldb. Como `core/ingest/` no tiene ningún
   importador (hallazgo #2), el ciclo es 100% latente: borrar `core/ingest/` lo mata entero.
   Ningún otro módulo vivo de sldb importa `kgdb`.
3. **Un test depende del paquete kgdb real (parity), no del shim.** `tests/api/test_api_graph.py:78-81`
   importa `kgdb.ingest.typed`, `kgdb.query`, `kgdb.graph.utils` con `importorskip` — es el test
   de paridad intencional de la transición ("same ids"), y esa parte de kgdb (no-shim) sigue
   existiendo en el repo kgdb (`kgdb/src/kgdb/ingest/typed.py`). No es obsolescencia, es verificación.
4. **`kgdb/contracts/persistence.py` es el único contrato kgdb sin contraparte en sldb** — y no
   hay duplicación porque sldb no tiene equivalente: el concepto ("un update de grafo con hash de
   integridad") no sobrevivió a la fusión en ninguna de las dos formas. Dentro de kgdb es código
   muerto: solo lo referencia su propio `contracts/__init__.py:10,13`, nadie en kgdb/src, pron o
   deskops lo importa.

Qué habría que enderezar (sin hacerlo ahora):
- Borrar `core/ingest/` → elimina los 4 imports de vuelta (§2.2).
- Decidir el destino de `persistence.py` al retirar el shim kgdb: migrarlo a sldb (si el journal
  de escrituras `store/journal/` quiere el contrato) o retirarlo con el shim. Hoy no hay duplicado.
- El test de parity (#2.3) debería re-apuntarse a la ruta interna (`store/graph/ingest_sldb.py`)
  cuando kgdb deje de instalarse.

Volumen: shims kgdb = 55 líneas útiles (110 con `__init__` y `persistence`); ciclo sldb→kgdb = 4 imports en 328 líneas de código que de todas formas es muerto.

---

## 3. Derivados duplicados: sections / semantic / cache

Aplicado el criterio del plan de edges ("lo mismo guardado en dos formas"):

- **sections**: no hay dos formatos. El único formato vivo es el shard por documento
  `runtime/sections/<model>/<doc>.yaml`. El YAML por modelo `runtime/sections/<model>.yaml` ya
  **no se escribe** (`store/io/sections_index.py:8-12`); su lectura es un fallback para stores
  no migrados (`sections_index.py:33-37`) y `save` shardea (`sections_index.py:40-46`).
- **semantic**: idem. `SemanticIndexIO.load` compone shards y cae al archivo único solo si no hay
  shards (`store/io/semantic_index.py:26-30`); `save` shardea y **unlinkea** el legacy
  (`semantic_index.py:40-46`).
- **cache**: `extracted.json` (payloads) y `built.json` (resultados derivados) son dos caches con
  la misma técnica (clave hash de cadena, tier memoria + disco, derivadas y borrables), pero con
  contenido distinto; ninguna duplica a la otra. No hay un formato "viejo" y uno "nuevo".
- **Conclusión**: a diferencia de edges —donde el formato viejo (shards) sigue siendo producido y
  leído por la capa nueva—, aquí el shard es ya la fuente y solo sobrevive el código de
  **conversión** (`store/migration.py:69` `migrate_store_layout`, invocado en
  `api/stores/open_store.py:36-38`) y los **fallbacks de lectura**. Eso no es código superseded:
  es la guarda que hace que un store viejo se migre solo. Retirarlo exigiría garantizar que no
  queda ningún store pre-capa-5 en circulación (pron/deskops/kb_agent), o esperar al retiro de
  esos consumidores.

---

## 4. Cómo se verificó "nadie lo usa"

- Censo AST propio sobre `src/` + `tests/` (maneja imports absolutos y relativos) para cada
  módulo de sldb; los hallazgos #2-#10 se confirmaron con `grep` dirigido adicional porque el
  censo no ve `from sldb.store import <submodulo>` (patrón de `edge_sync.py:11`, `documents_hash.py:19`).
- Regla aplicada: un símbolo usado solo por tests sigue siendo candidato a muerto si el test lo
  referencia sin que la ruta real lo toque (caso `model_update`, #7: el monkeypatch de
  `tests/test_cli_v2.py:1664` cae sobre un módulo que `commands/models.py:37-39` jamás importa).
- El caso inverso: los 47 símbolos de `api/__init__.py` sin importadores internos (#12) **no** se
  marcan muertos porque el propio módulo declara ser contrato público para pron/kgdb/deskops
  (`api/__init__.py:3-7`), y hay consumidores externos que no viven en este repo.

---

## 5. Detalle de los hallazgos nuevos (no cubiertos por el plan de edges)

### 5.1 `cli/graph/` y `cli/graph_old/` — dos copias huérfanas de un refactor interrumpido

Ambos árboles nacen en el mismo commit (`73e4553`, "Massive subagent refactor interrupted by
quota limit"); `e83db87` limpió el resto pero dejó los dos. Ninguno tiene importadores.
`graph_old/__init__.py:3-5` importa módulos inexistentes (`from .query import …` →
`ModuleNotFoundError`). Sus piezas son casi idénticas entre sí (`diff -r` muestra solo
reordenamientos) y su contenido real sobrevive en `cli/graph_ops/` + `cli/search_record.py`
(22 importadores en src, p. ej. `api/search.py:43-49`). Son clase (i) pura: copias muertas que
nadie carga.

### 5.2 `core/ingest/` — la isla pre-ecosistema

328 líneas en 9 módulos que implementan "ingest de raw sources → draft nodes" con
`wikiignore`, manifest CSV (`ingest/manifest.py:16-30`) y un renderer propio
(`ingest/renderer.py`). Depende de `wiki_compiler` y `ontology` (paquetes que no están en
`pyproject.toml:21-28` ni instalados). Cero importadores en src y tests. Es el único sitio del
repo que importa `kgdb` (hallazgo #11). No está roto porque algo lo necesite: simplemente nunca
se cableó al producto sldb actual (el ingestion real lo hacen `store/section_sync.py`,
`store/semantic.py` y `selfdoc/python_scanner.py`).

### 5.3 Compat bridges sin consumidores

`cli/commands/model_source.py:1-3` y `cli/federated_utils.py:1-3` se autodenominan
"Compatibility bridge" y re-exportan desde `api/`. Todos sus destinatarios ya importan desde el
destino final (`api/model_drafts/source_location.py:3`, `api/model_registry/federated_lookup.py:3`
dicen "moved here from … which re-exports these names", pero ya nadie pasa por el re-export).
El motivo del bridge dejó de existir.

### 5.4 El surface público de edges en `api/__init__.py`

El plan ya lista los ~20 símbolos de edges; este censo cuantifica el tamaño del problema del
surface: de los 76 nombres en `__all__`, 47 no tienen ningún importador interno. Se conservan
por contrato, pero cuando #1 muera, la poda del `__all__` (plan §1, fila `api/__init__.py`) debe
avisar a pron/kgdb/deskops — no es un borrado silencioso.

---

## 6. Ranking final: qué retirar primero (impacto / riesgo)

| Orden | Qué | Tamaño | Justificación (una línea) |
|---|---|---|---|
| 1 | `core/ingest/` | 328 lín. | Cero riesgo (nadie lo importa, ni siquiera se importa a sí mismo bien): mata el ciclo kgdb↔sldb completo de un solo golpe |
| 2 | `cli/graph/` + `cli/graph_old/` | 213 lín. | Copias muertas del refactor interrumpido; borrado mecánico sin consumidores; elimina la única `__init__` rota del repo |
| 3 | Capa `runtime/edges/` (plan PR 1→5) | ≈ 1.613 lín. | El mayor volumen y el único con riesgo real (writes clase B + surface público): por eso ya tiene plan propio; aquí se confirma que no hay otra capa con el mismo patrón |
| 4 | `doc_helpers.py`, `predicates_format.py`, `model_source.py`, `federated_utils.py`, `model_update.py` | 230 lín. | Módulos sueltos sin importadores (o test-only); limpieza de bajo riesgo que reduce superficie de confusión |
| 5 | Compat bridges vivos (`legacy.py` x2) | 79 lín. | No urgente: es surface deliberado con alias activos; se retira solo si el mantenedor decide abandonar el DSL `ls/get/glob` |

Los 5 hallazgos más grandes suman ≈ **2.553 líneas** de las 22.390 de `src/sldb/` (≈ 11%):
1.613 (capa edges) + 328 (core/ingest) + 134 (cli/graph) + 100 (doc_helpers) + 79 (cli/graph_old).

---

## 7. Lo que sorprendió

1. **Los 4 imports sldb→kgdb están todos en un árbol que ni siquiera importa.** El "ciclo" que
   parecía un problema de arquitectura viva es en realidad el síntoma de una isla muerta: matar
   la isla mata el ciclo, no hay que "enderezar" nada en el código vivo.
2. **Dos refactors simultáneos dejaron dos copias casi idénticas (`graph/` y `graph_old/`) y una
   tercera que ganó (`graph_ops/`).** El commit interrumpido por cuota de subagente dejó un
   `__init__.py` roto en el repo sin que nadie lo notara — porque nadie lo importa.
3. **Donde el plan de edges ve "shards viejos", sections/semantic tienen exactamente el patrón
   invertido**: el shard-per-documento es lo nuevo y el archivo único es el legado. La lección
   del plan ("re-puntar la fuente, no borrar archivos") no aplica allá porque la migración ya
   está resuelta en vivo por `migration.py` — no hay segunda implementación conviviendo, solo un
   fallback de lectura para stores pre-capa-5.
4. **El contrato "persistencia de grafo" de kgdb no tiene heredero**: `PersistenceEntry`/
   `TransactionManifest` son el único contrato kgdb que no se movió ni se duplicó — simplemente
   quedó sin concepto equivalente en sldb y sin importadores en ningún repo del ecosistema.

FILE:docs/architecture/code-docstring-indexing-handoff.md
# Handoff: Continue Source Docstring Annotations

> History (2026-10-18): this handoff guided the delivery of the docstring indexing contract and is kept as its working record. The task closed in aca36681; strict metadata, tag inheritance, re-exports, shadowing and the spec2viz projection were implemented afterwards, and the current status and open items are in [the spec, section 7](code-docstring-indexing.spec.md). KGDB, named throughout, was a separate graph product at the time; it was merged into sldb as its graph layer (`sldb.store.graph`) and no external `kgdb` exists any more.

Continue the [docstring indexing specification](code-docstring-indexing.spec.md) in a small annotation-only batch. The specification is the authority; the two [PythonSymbol pilot declarations](../../src/sldb/selfdoc/python_symbol.py) demonstrate its syntax. The source-fact adapter now writes a regenerable KGDB graph, but strict docstring metadata interpretation and tag inheritance are not implemented. Do not report annotations as complete semantic classification.

## Assignment for the next agent

Read the spec completely, `standards.md`, the active task (`task-build-code-self-documentation`, closed in aca36681), and the execution pill (`pill-015-self-documentation-boundaries`, retired on 2026-10-18; its rules are in [self-documentation.md](../self-documentation.md)). Preserve unrelated working-tree changes; this checkout already contains extensive unfinished work. Do not reset, stage everything, commit, bump versions, or mark the overarching task done as part of this handoff.

The following batch-2 assignment is complete; do not repeat it. The next annotation assignment is the batch-3 proposal at the end of this handoff. Each batch annotates at most four declarations and requires reading consumers before describing behavior.

| Source | Declarations / proposed stable IDs | Evidence to read |
|---|---|---|
| `src/sldb/selfdoc/planned_document.py` | `sldb.selfdoc.planned_document`; `sldb.selfdoc.planned_document.PlannedDocument` | `selfdoc/materialize.py`, `selfdoc/python_materialize.py`, `cli/selfdoc_write.py` |
| `src/sldb/selfdoc/report.py` | `sldb.selfdoc.report`; `sldb.selfdoc.report.DocumentationReport` | `cli/selfdoc_inspect.py`, `cli/commands/selfdoc.py` |

Use module context tags `system:sldb`, `workspace:knowledge`, `topic:selfdoc`, and local class tag `type:code.symbol`, matching the pilots. Use `kind: core` only after confirming the data-contract responsibility from those consumers. Do not repeat inherited context on classes. Leave properties and methods for another batch; their source bodies still provide AST evidence without extra annotations.

The prose must explain what each declaration actually does, its input/output role, and relevant limits. `PlannedDocument` carries a validated payload and a before-image; it is not a filesystem transaction. `DocumentationReport.ok` currently ignores `semantic_gaps`; it does not certify semantic completeness. Record ambiguity here instead of inventing ownership or architecture. If a classification cannot be grounded, omit optional `kind` and record the reason.

Only edit these docstrings and the handoff/task progress notes, plus generated references/indexes resulting from the documented sync. Do not implement the adapter, rewrite business logic, annotate the whole tree, edit sibling KGDB/spec2viz repositories, or manually fill hundreds of generated `Purpose` / `Architecture` sections. Never add `edges` or `contains` to frontmatter.

Copy the pilot's blank line **before** the closing `---`. This is a temporary compatibility precaution, not a metadata requirement: without it, raw Markdown rendering treats the preceding YAML line as a setext heading and the materializer rejects the round trip. Safe literal rendering remains a separate implementation fix; do not relax the round-trip guard to bypass it.

## What exists versus what remains

The pilot delivery created the behavior spec first, then annotated one module and its class. `PythonSymbol` fields and executable behavior are unchanged. The current materializer can preserve the class's complete docstring as text; that is not metadata interpretation.

| Area | Current implementation / gap | Follow-up, outside the annotation batch |
|---|---|---|
| Frontmatter | Source-fact graph reads leading YAML opportunistically; generated symbol docs still retain raw docstrings | Typed profile, strict diagnostics, separate prose and metadata |
| Literal rendering | Compact frontmatter becomes a Markdown setext heading; `docstring` extracts as `---` and later fields shift | Safe literal-content representation; regression cases for compact frontmatter, headings, and fences |
| Context | Source graph emits module/symbol nodes and lexical containment; generated symbol inventory remains class/function-oriented | Package identity, selective inherited tags and provenance |
| Identity | Scan ID is qualified; materializer constructs a different normalized document ID | Explicit declared-ID mapping with collision checks and reviewed legacy migration |
| Existing scan config | Fixed 2026-10-18: the inventory uses `--source-root src` (no `--package`) and module names `sldb.*`; the `sldb.sldb.*` identities were migrated by renaming every symbol document | — |
| Relationships | Source graph emits `contains`, `imports`, and resolvable annotation `references` through KGDB; semantic export v1 remains unchanged | Registered typed relation vocabulary, re-exports/star imports/shadowing/type-checking resolution, spec2viz projection |
| Architecture | Optional spec path/hash only; no symbol-to-node association | KGDB identity-backed projection to the existing spec2viz component schema |
| Explanations | Generated `purpose`/`architecture` placeholders are preserved, not derived from prose | Source-owned extraction with explicit conflict handling for existing authored text |
| Check exit status | Python and CLI checks both return nonzero on `ok: false` | Keep regression coverage while adding report categories |
| Rename/removal | Candidates now require exactly one fact match, but still compare file hashes and assume default symbol paths | Complete-source and nondefault-output coverage; reviewed rename migration |

`semantic_gaps` counts placeholder fields only; it is not a test of docstring quality. A pinned architecture spec hash proves neither review nor graph connectivity. Annotation-only changes are not expected to reduce that counter. Do not hide it with manually copied prose.

## Validation and synchronization

Use Python 3.13 from `.venv` for the existing generated inventory. Repository style tests cap effective file length at 80 lines, including docstring lines; keep annotations concise and do not refactor working code merely to add prose.

1. Parse edited files with `ast.parse`. Extract each module/class docstring with `ast.get_docstring(clean=True)`, split its leading delimiters, and validate its YAML mapping and `tags` against `sldb.models.knowledge_tag.KnowledgeTag`. Check exact IDs against the pilot and this batch; no `edges` or `contains` keys. This is fixture validation, not proof that a production parser exists.
2. Run the existing focused suite:

```bash
PYTHONDONTWRITEBYTECODE=1 .venv/bin/python -m pytest -q tests/selfdoc tests/test_clean_code_rules.py
```

3. Synchronize once, retaining the current options and generated IDs. From the repository root:

```bash
PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=/home/jp/proyectos/hum-ecosystem/tools/deskops \
  .venv/bin/python -m sldb selfdoc python-sync --store .sldb \
  --source-root src --system sldb --output knowledge \
  --architecture-spec docs/architecture/spec2viz/python-ast.yml
```

The sibling `deskops` path lets the existing store load its registered desk models; adapt the absolute path if the checkout moves. Do not add external stores to resolve an import problem. Module docstrings affect the containing-file hash and therefore generated records from that file, although they are not indexed as module records yet.

4. Repeat the same invocation with `python-check` instead of `python-sync`. Inspect JSON `ok`, `missing`, `changed`, `untracked`, `stale_indexes`, `removed`, and `renamed`; exit status alone is unreliable. Preserve pre-existing findings and report them. No need to regenerate the full spec2viz AST artifact for docstring-only changes.
5. After editing tracked narrative/task notes, run `sldb stores update --store .sldb --pythonpath .` and `sldb stores check --store .sldb --pythonpath .` through the same `.venv` and `PYTHONPATH` environment. Review the diff: only intended annotations and their derived files should be newly changed by this batch. Do not confuse pre-existing modifications with your work.

Do not add redundant docstring-only test files. The later implementation slice needs the behavioral cases in spec section 7, especially YAML failures, lexical inheritance, ID migration, and preservation of authored KGDB facts.

## Implementation entry points for a separate agent

SLDB: `selfdoc/python_scanner.py`, `selfdoc/python_symbol.py`, `selfdoc/python_materialize.py`, `models/python_symbol_doc.py`, `models/knowledge_tag.py`, `store/semantic_tags.py`, `store/export.py`, and `cli/selfdoc_inspect.py` (all under `src/sldb`).

Graph-layer contracts (formerly the sibling kgdb package): `relation_doc.py`, `relation_type_doc.py`, and `builtin.py` under `src/sldb`. Python containment is not a currently shipped builtin; reuse the registry mechanism, not model-only `extends` for code classes.

spec2viz: run `spec2viz diagram schema --type component`. The local sibling source is `spec2viz/spec2viz/models/component.py`; existing curated examples are in `docs/architecture/spec2viz/`. Preserve node/edge meanings through an adapter; do not create a parallel semantic taxonomy or match curated nodes by fuzzy labels.

## Delivery checkpoint

Pilot validation on 2026-09-14:

- IDs: `sldb.selfdoc.python_symbol` and `sldb.selfdoc.python_symbol.PythonSymbol`. Both leading YAML mappings and local tags validated against the existing tag type; AST parsing succeeded.
- Both narrative documents passed `ArchitectureNarrativeDoc` extraction/render/extraction checks. The pilot class passed the production `plan_python_documents` round-trip guard with the blank-line precaution described above.
- Focused suite: 305 passed; two warnings about existing pytest configuration/parametrization.
- First compact-frontmatter sync attempt was rejected during planning, before writes. This reproduced the literal-rendering gap above; it was not bypassed by disabling validation.
- Final `python-sync`: JSON `ok: true`, 1,233 documents, one written (the pilot class reference), no missing/changed/untracked/stale/removed/renamed findings.
- Subsequent `python-check`: JSON `ok: true`, zero written, same empty findings. `semantic_gaps: 1233` remains expected under the current placeholder-only logic.

The next agent should append its four annotated IDs, commands/results, unresolved questions, and a next bounded batch. Completion of an annotation batch does not close the active self-documentation task or imply the spec is implemented.

## Batch 2 delivery checkpoint (2026-09-14)

Annotated the four assigned declarations; the two files now follow the pilot format with the blank line before the closing `---`.

- IDs: `sldb.selfdoc.planned_document`, `sldb.selfdoc.planned_document.PlannedDocument`, `sldb.selfdoc.report`, `sldb.selfdoc.report.DocumentationReport`.
- `kind: core` confirmed for all four from the consumer evidence: `PlannedDocument` is the typed data contract `materialize.py` / `python_materialize.py` produce and `selfdoc_write.py` / `selfdoc_inspect.py` consume; `DocumentationReport` is the typed findings contract those consumers fill and `cli/commands/selfdoc.py` prints as JSON. Recorded ambiguity: `DocumentationReport` also doubles as the CLI's stdout JSON surface, so a reviewer could argue `interface`; kept `core` because the command, not the model, is the user-facing surface.
- Prose limits recorded: `PlannedDocument` is a planning record, not a filesystem transaction (the write path re-verifies before-images in `write_documents`); `DocumentationReport.ok` ignores `semantic_gaps`. Review clarified that it means no checked findings were populated, not a guarantee of complete detection or semantic correctness.

Fixture validation: `ast.parse` plus `ast.get_docstring(clean=True)` on both files; each leading YAML mapping parsed, keys limited to `id`/`kind`/`tags`, no `edges`/`contains`, all four IDs matched this handoff, and every tag validated against `KnowledgeTag`.

- Focused suite: `PYTHONDONTWRITEBYTECODE=1 .venv/bin/python -m pytest -q tests/selfdoc tests/test_clean_code_rules.py` → 305 passed, the same two pre-existing pytest configuration/parametrization warnings.
- `python-sync` (same options and environment as the pilot): JSON `ok: true`, 1,233 documents, `written: 4`, empty `missing`/`changed`/`untracked`/`stale_indexes`/`removed`/`renamed`. Four writes, not two: annotating the module docstrings changed each file's `source_sha256`, so the class references plus the generated `model_name` and `ok` property references were refreshed. `semantic_gaps: 1233` unchanged, as expected under placeholder-only logic.
- `python-check` (identical invocation): JSON `ok: true`, zero written, all findings empty.
- After editing this handoff and the task progress note: `sldb stores update` and `sldb stores check` through the same `.venv` and `PYTHONPATH`; store integrity passed with no new unintended changes.

No adapter implementation was started; annotations are source text plus generated reference refreshes only. Unresolved questions carried forward: the compact-frontmatter rendering fix, module-record indexing, the `--source-root src --package sldb` identity migration, and the scanner's module/package record gap all remain outside annotation batches.

### Review corrections before batch 3

The batch-2 YAML and freshness checks passed, but the prose incorrectly promised one-to-one rename matches and universal command-exit gating by `ok`. `DocumentationReport` and the misleading `rename_candidates` helper docstring now describe the actual behavior: ambiguous rename matches can depend on plan order, and Python check/sync currently return zero independently of the JSON finding status. Their algorithms are unchanged; correcting the prose is not fixing those runtime limitations.

The import-versus-containment mistake in the next-batch instructions is corrected below. Spec sections 4.1–4.2 define typed import bindings, separate annotation-reference sites, scope/alias/resolution evidence, and acceptance cases grounded in `command.py`. The implemented source-fact graph covers direct static bindings and resolvable annotations; its deliberate limits are recorded in the specification.

Review validation: 305 focused tests passed with the same two warnings; all six existing annotated declarations passed AST/YAML/tag fixture checks; both narrative documents round-tripped through SLDB. The two import bindings and field annotation expressions in spec section 4.2 were checked against the actual AST. `python-sync` returned JSON `ok: true` with 11 references refreshed (the containing-file hashes affect all symbols in `report.py` and `selfdoc_inspect.py`); subsequent `python-check` returned `ok: true`, zero written, and empty findings. The placeholder-only `semantic_gaps` count remains 1,233.

### Source-fact implementation checkpoint (2026-09-14)

`python-sync` now writes `.sldb/runtime/graphs/python-source.graph.json` with sldb's own graph IO (originally, 2026-09-14, via KGDB's public ingest command; the external kgdb was removed 2026-10-18). It replaces only this generated graph and carries producer/source hashes, spans, lexical containment, import binding metadata, local/external targets, and annotation-reference evidence. `python-check` compares the expected AST projection with the saved graph and exposes `graph_stale`; a missing/stale graph is a nonzero check result. It does not mutate SLDB semantic export v1 or human-authored KGDB relations.

The Python exit-status and ambiguous-rename bugs are fixed. Full validation: 518 tests passed (two existing pytest warnings); a repository sync reported 1,273 documents and no findings, and the next check reported zero writes. The generated graph was queried with KGDB: `CommandRecord.arguments` has a `references` edge to `ArgumentRecord`, distinct from its module's `imports` and `contains` edges.

### Next bounded batch proposal (batch 3)

Four more declarations, same rules and consumers-first reading:

| Source | Declarations / proposed stable IDs | Evidence to read |
|---|---|---|
| `src/sldb/selfdoc/command.py` | `sldb.selfdoc.command`; `sldb.selfdoc.command.CommandRecord` | `selfdoc/materialize.py`, `selfdoc/projection.py`, `selfdoc/parser.py` |
| `src/sldb/selfdoc/parser.py` | `sldb.selfdoc.parser`; `sldb.selfdoc.parser.ParserScanner` | `cli/commands/selfdoc.py`, `cli/selfdoc_context.py`, `tests/selfdoc/test_parser.py` |

`ArgumentRecord` and `ExclusiveGroup` are imported from `argument.py` and `constraint.py`; they are not nested declarations. Leave their defining files and parser methods unchanged. Do not add import lists or edges to docstrings. Explain `CommandRecord` as a data contract and `ParserScanner` as an argparse-tree extractor, not as another record model. Keep `kind: core` only when the actual responsibility supports that classification; record ambiguity otherwise.

Before syncing, check every behavioral claim against executable statements in its producer/consumer, not merely existing docstrings or `Field` descriptions. The rename claim above demonstrates that those descriptions can themselves be wrong. AST/YAML validity and green freshness checks do not validate prose. Keep the scope to these four annotations, progress notes, and derived references/indexes; implementing sections 4.1–4.2 needs a separate implementation batch.

### Documentation-only delivery checkpoint (2026-09-14, Pron exposure)

Documentation-only pass against the Pron capability (iteration 4 closed in the Pron repo during this work; nothing under `src/`, `knowledge/`, or the store contents was modified):

- `self-documentation.md` example paragraph corrected and completed: the direct query `does CommandRecord reference` returns only the targets of the AST `references` relation (annotation references); import bindings are queried with `does ... import`. Facts are static and as of the last `python-sync`; Pron's freshness guard compares merged-graph hash against the source-fact artifact, `python-check` detects source-versus-artifact drift, and the remedy after changing source is `python-sync` (`pron refresh` alone only re-merges an already-current artifact). Agents never read `.kgdb/` artifacts.
- New spec section **4.3 "Query contract: Pron is the agent-facing surface"**: virtual read-only `PythonSymbol` (noun `python symbol(s)`), node kinds `python_symbol`/`python_module`/`python_external`, relations `contains`/`imports`/`references` plus base verb forms; four real commands with real outputs; `does ... <verb>` auxiliary rule limited to source relations; trace-as-provenance (`pron graph ...` + `kgdb edges_from/to ...`); exact-identity-first name resolution; stale-graph behavior and message; static limits (no runtime calls, re-export chains, star imports, shadowing).
- Exposure paragraph updated to the implemented iteration 4: `ProjectionDoc.source_symbols` is an explicit opt-in (`true` enables, `false` excludes, undeclared keeps previous behavior; the local `all` projection exposes it) and `source_relations` selects a subset of the three relations; source relations are read-only in every projection.
- Validation: `sldb stores update` (1,571 documents, 0 missing) and `stores check` PASS after each edit round.

Still pending (unchanged scope): federation of source symbols, curated aliases, strict metadata validation, inherited tags, legacy-ID migration, typed relation registration, spec2viz projection.

FILE:docs/architecture/code-docstring-indexing.spec.md
# Python Docstring Indexing Contract

> History: this contract was written while relationships were persisted by KGDB, a separate graph product. KGDB was merged into sldb ([ADR](sldb-absorbs-kgdb.md)) and is now its graph layer (`sldb.store.graph`, CLI `sldb graph ...`); no external `kgdb` package or executable exists any more. This document says "the graph layer" for it.

This specification records the agreed target behavior for code self-documentation: SLDB indexes declarations in source docstrings, the Python AST supplies structural evidence, sldb's graph layer owns persisted relationships, and spec2viz renders graph projections. Section 7 says which parts are implemented.

Status (2026-10-18): implemented. `python-sync` materializes the SLDB documents and writes a regenerable source graph; `python-check` reports drift without writing. The adapter validates docstring metadata strictly (section 2), computes inherited tags with their origin (section 3), emits containment, import bindings (resolved through explicit re-export chains, with conditional and `TYPE_CHECKING` context) and annotation references that account for shadowing (section 4), validates its edges against the registered relation types, and spec2viz projects the graph (`spec2viz diagram from-graph`, section 5). What remains open is listed in section 7. Consumers use the published store facts through their own normal interfaces; no consumer-specific vocabulary belongs in this adapter. The [handoff](code-docstring-indexing-handoff.md) records how the work was delivered.

## 1. Ownership

| Information | Source of truth | Consumer |
|---|---|---|
| Stable identity, local classification, local tags | Leading docstring frontmatter | SLDB code adapter and indexes |
| Purpose and behavioral explanation | Docstring body and code | Generated reference |
| Stored representation and source format | Model semantics | SLDB semantic index and every consumer |
| Declaration kind, location, lexical containment, resolvable dependencies | Python AST | Source-fact adapter |
| Effective tags and their inheritance provenance | Local declarations plus lexical context | SLDB indexes and the source graph |
| Persisted structural and reviewed semantic relationships | sldb graph layer | Pron graph queries and spec2viz projections |
| Diagram layout and presentation | spec2viz specification | Renderer |

No `edges`, `contains`, dependency lists, or graph copies belong in docstring frontmatter. Source extraction can emit relationship facts without becoming a second graph store. Hand-authored semantic relationships belong in the graph layer (as `RelationDoc` edges) when they cannot be established from source evidence.

Every tracked record is physically rendered as Markdown, so `representation.markdown` is a base semantic tag. This does not mean every record describes a Markdown source: the base source tag is `source.document.markdown`, while the Python adapter replaces it with `source.code.python`. Consumers filter these semantic tags instead of inferring format from a folder, filename, or model name.

## 2. Docstring profile

Use the same YAML frontmatter idiom as SLDB documents, at the start of the docstring returned by `ast.get_docstring(node, clean=True)`:

```python
"""---
id: example.module.Record
kind: core
tags: [type:code.symbol]

---
Represent the facts collected from one source declaration.

Describe responsibilities, inputs, outputs, and important limits here.
"""
```

The initial profile has exactly three allowed keys:

- `id`: required nonempty string, unique within the selected store; explicit identity survives a move or rename until intentionally changed.
- `kind`: optional nonempty string, using the same classification as the corresponding spec2viz component node. Existing SLDB diagrams use `core`, `interface`, and `boundary`; spec2viz accepts other strings, but an annotator must not invent a competing vocabulary without review.
- `tags`: optional list, default empty; each value validates as the existing `KnowledgeTag` (`namespace:value`, e.g. `topic:selfdoc`). Duplicate values normalize to one value.

This is a new code-adapter profile, not an assertion that every existing SLDB model accepts these keys. `kind` in this profile is semantic classification; the existing `PythonSymbol.kind` / `PythonSymbolDoc.kind` is an AST node kind such as `ClassDef`. An implementation must retain both without overwriting one with the other.

Only an opening line exactly `---` starts metadata; a later `---` in prose is ordinary content. Require a closing delimiter, safe YAML loading, a mapping, unique keys, correct types, and no unknown keys. Malformed metadata or duplicate IDs must produce source-located diagnostics before any writes; never silently discard invalid declarations. An empty body is a documentation gap, not permission to fabricate an explanation.

The blank line before the closing delimiter in the pilots is valid YAML and a rendering precaution: the materializer embeds raw docstrings as Markdown, where `tags: ...` immediately followed by `---` becomes a setext heading. The adapter accepts both forms (`tests/selfdoc/test_docstring_metadata.py`); whitespace is not a semantic requirement. Literal source content needs a safe rendering boundary rather than relying on author formatting.

Ordinary docstrings without frontmatter remain valid scan inputs. Keep their text and structural facts; report absent declared identity/classification separately. A qualified source reference may serve as a provisional identity, but must not be presented as stable across renames. Parse source statically: do not import or execute the target modules.

The first body paragraph supplies the generated purpose verbatim after whitespace normalization. The remaining body supplies the detailed explanation; source facts and declared context supply architectural placement. A missing role or ambiguous explanation is reported for review, not guessed from a filename. Do not require a second manually authored copy of this information in every generated Markdown record.

## 3. Lexical context and tag inheritance

Index package/module docstrings as well as classes, functions, async functions, methods, and nested declarations. A package's `__init__.py` supplies its package context; it must not create two competing identities for the same package. Modules without docstrings still supply structural context. Declarations inside conditional/try blocks retain their nearest lexical declaration owner, with conditional evidence where applicable.

Inheritance follows the lexical package → module → class/function → nested declaration chain within the selected store and source root. Do not inherit through imports, calls, Python base classes, sibling modules, or a parent store. Only ancestor contexts included in the selected scan participate; absence must not trigger an unbounded filesystem search.

| Namespace or field | Rule |
|---|---|
| `system:*`, `workspace:*` | Nearest declaration wins, independently per namespace. More than one distinct local value in either namespace is an error. |
| `topic:*` | Union of ancestor and local values, deduplicated. |
| Other tags, including `type:*` | Local only in this initial profile. |
| `id`, semantic `kind`, body | Local only; never copied from a parent. |

Keep `local_tags` and `effective_tags` distinct in the adapter contract. Every inherited value retains the ancestor identity and source location that supplied it. Never write derived tags back into descendant docstrings. Removing an ancestor declaration or changing a context tag must remove obsolete derived values on the next successful reconciliation.

Retain colon notation in tag payloads. The existing model `__semantics__` flattener's dotted paths are a separate representation; this specification does not authorize silently converting colon tags into dotted names or claiming that dotted semantic-parent edges already implement lexical inheritance.

## 4. Structural relationships and the graph layer

Containment is inferred from lexical ownership, not manually annotated. A module owns its top-level class; that class owns its methods. Imports and inheritance provide additional syntactic evidence, but not every reference resolves statically.

- Produce one immediate-parent containment fact per contained declaration; transitive containment is a query, not redundant authored data. A separate `defines` relation, if required by a consumer, must be a documented projection of those facts rather than an independently maintained list.
- Resolve dependencies using import bindings, aliases, relative import level, and lexical scope. Preserve unresolved/external references as diagnostics or explicit unresolved facts; do not create a supposedly resolved local edge by matching a short name.
- Emit inheritance or call-target edges only when the target can be resolved under documented static rules. Dynamic dispatch, decorators, conditional imports, and reflection must not be reported as certain runtime behavior. An import does not automatically imply a business-level `uses` relationship.
- Each derived fact carries source path, source span, containing-file hash, extraction version, and resolution status. File hashes establish source freshness, not individual-symbol equivalence or a complete runtime call graph.

Bind relation names and endpoint constraints through the store's `RelationTypeDoc` registry (`sldb/relation_types/`). The store registers `contains` (`python_module|python_symbol → python_symbol`), `imports`, and `references` (`python_module|python_symbol → python_module|python_symbol|python_external`), all directed and many-to-many. The adapter loads those tracked records (`sldb.selfdoc.python_relation_registry`) and validates every emitted endpoint before publication. The registry also has structural types such as `has_document` and model-only `extends`; do not misuse those for Python code endpoints. Do not add a private SLDB edge enum.

Persist through sldb's graph IO. Reconciliation replaces only facts owned by this extractor, in its store/source-root scope, after a successful scan. It is idempotent; failed/partial scans must not remove existing facts. Preserve manually reviewed relationships and other producers' edges. Disappearing endpoints and conflicts must be surfaced for review rather than deleting authored knowledge silently.

Explicit source IDs, current generated Markdown document IDs, and graph node IDs are different address spaces. Maintain an explicit mapping from `(store identity, declared source id)` to the tracked SLDB export address and then to its graph address. Reuse the graph layer's store-qualified addressing, not machine-local absolute paths or a second global-ID convention. Never silently rename existing tracked documents to match new source IDs.

The current `sldb_kgdb_semantic_export` v1 excludes source-code edges and raw bodies. The source adapter therefore writes a separate regenerable graph snapshot with sldb's own graph IO (`write_source_graph`; before the merge it went through `kgdb ingest`), by default `.sldb_cache/graphs/python-source.graph.json` (`.sldb/runtime/graphs/` until 2026-11-04); it does not mutate v1. Its `contains`, `imports`, and `references` edge tokens are source-fact projection vocabulary with `origin: python_ast`, not authored `RelationDoc` edges. The JSON artifact is a producer detail behind SLDB's publishing boundary, not a second source of truth. The edge tokens are the names registered in `RelationTypeDoc` and validated before writing; that validation does not alter this provenance boundary.

### 4.1. Import bindings and reference sites

An import introduces a name in a lexical scope; it does not define the imported declaration there. Extract one typed binding fact per imported name, not a single module-name string for the whole statement. This is AST-derived adapter data, never another docstring frontmatter key.

| Binding fact | Required meaning |
|---|---|
| Importer and scope | Source module and lexical owner of the import statement |
| Syntax | `Import` or `ImportFrom`, source module spelling, relative level, imported name, explicit alias if present |
| Local binding | The name introduced in that scope, separate from the requested module/symbol |
| Resolution | Canonical target reference when proven, otherwise explicit external/unresolved/ambiguous status; preserve the requested reference even without a target |
| Evidence | Source span, containing-file hash, extractor version, and conditional/type-checking context when present |

For `import a.b`, the local binding is `a`; for `import a.b as c`, it is `c`. For `from .argument import ArgumentRecord as AR`, retain module `argument`, relative level `1`, imported name `ArgumentRecord`, and local binding `AR`. Resolve relative imports against the importer's package, not its working directory. A binding to a proven local re-export must follow its explicit provenance chain or remain unresolved; never guess the definition from the imported name alone.

Star imports cannot be expanded into invented local names. Dynamic imports are not ordinary `Import`/`ImportFrom` bindings and must not be reported as resolved without a separately documented rule. Imports under conditions, inside functions, or under `TYPE_CHECKING` retain that context; their presence does not prove execution. Do not import target modules to resolve them.

Extract reference sites separately from imports. A reference fact identifies its lexical owner, source expression and span, context (such as a type annotation or call), and resolved binding/target when proven. Name rebinding or shadowing must be accounted for; uncertain resolution remains explicit. A syntactic annotation reference does not establish a runtime call, instantiation, containment, or business-level dependency. Importing alone does not establish use or intentional public re-export, and imported declarations do not inherit the importer's tags.

### 4.2. Acceptance example: imported field types

In `src/sldb/selfdoc/command.py`, `from .argument import ArgumentRecord` and `arguments: list[ArgumentRecord]` provide different evidence:

| Fact | Expected owner / target |
|---|---|
| Definition / containment | Module `sldb.selfdoc.argument` owns its `ArgumentRecord` declaration |
| Import binding | Scope `sldb.selfdoc.command` binds `ArgumentRecord` to `sldb.selfdoc.argument.ArgumentRecord` |
| Annotation reference | Field site `CommandRecord.arguments` references that binding in `list[ArgumentRecord]` |

The analogous `ExclusiveGroup` target is `sldb.selfdoc.constraint.ExclusiveGroup`. Neither imported class is nested in `CommandRecord` or defined by `command.py`. These qualified names identify expected source targets; they do not assign new declared frontmatter IDs to unannotated classes. A field reference site can be addressed by its owning declaration and source span without requiring a separate field docstring or graph node.

The integration binds these distinct meanings through the registered relation types and retains import/reference evidence. Do not substitute containment for importation or collapse an annotation reference into a generic `uses` edge. spec2viz consumes the resulting graph projection through section 5; it does not perform a second semantic interpretation.

Acceptance cases must include these two concrete imports, aliases, `import a.b` versus `import a.b as c`, multi-name statements, relative imports, nested scopes, shadowing, conditionals/`TYPE_CHECKING`, unused imports, unresolved/external targets, re-export chains, and star imports. Removing a reference while retaining its import removes only the reference fact. No case may introduce false containment or imported-tag inheritance.

The legacy `PythonScanner` still stores a simplified import string in generated Markdown records. The separate source-fact adapter preserves imported names, aliases, lexical owners, relative levels, spans, hashes, local/external targets, and annotation references in the source graph. Its resolution is lexical and static. It follows explicit module-level re-export chains and keeps the chain as evidence (`via`, `sldb.selfdoc.python_reexports`); a star import, a cycle or a module outside the scan ends the chain unresolved. It records `conditional` and `type_checking` context on bindings, and resolves a reference against the binding active at that point, so a rebound name is not attributed to the earlier import (`sldb.selfdoc.python_shadowing`). It does not infer star-imported names or prove runtime calls.

### 4.3 Consumer boundary

The adapter publishes store-owned facts, not a conversational language or a consumer-specific graph view. `PythonSymbolDoc` documents are ordinary tracked SLDB records; the source graph carries the derived structural facts and their AST provenance. Consumers—including Pron, spec2viz, an agent, or another UI—must consume those published records and relations through their normal sldb integration boundary. They must not depend on private artifact paths, add adapter-specific model names to their own runtime, or re-derive AST meaning from source.

`python-check` is the authority for source-to-publication freshness: it reports `graph_stale` when the persisted snapshot no longer represents the selected source root. The facts are static as of the last successful `python-sync`; they certify lexical containment, import bindings (through explicit re-export chains), and resolvable annotation references only, not runtime calls or star-imported names (section 4.1).

A consumer may add its own display aliases or query syntax only as ordinary consumer configuration over registered store identities and relation types. Such configuration is not part of the Python adapter and must not change or duplicate the graph facts.

## 5. spec2viz is a projection, not another semantic mapper

Use the existing component schema: `nodes[id].label`, `nodes[id].kind`, `nodes[id].contains`, and `edges[].from`, `to`, `relation`, `label`. `contains` in a generated diagram is a projection of the graph's containment; it is not source frontmatter. Adapter output must validate with `spec2viz diagram validate`.

Resolve projected node IDs from the explicit identity mapping. Labels come from source names or authored display text; `kind` comes from local classification; relation names come from the registered relation types. Translate the graph's `source_id`, `target_id`, and `relation_type` to the corresponding spec2viz fields without reclassifying their meaning. Projection filtering must not leave dangling `contains` entries or edge endpoints. spec2viz implements this as `spec2viz diagram from-graph` (spec2viz 8207dfe): labels from source names, `kind` declared or from the AST, `--module-prefix` filtering without dangling edges, relation names unchanged.

The current AST generator's `module_*` / `class_*` IDs and curated diagram IDs such as `CLICommands` are not automatically equivalent to declared source IDs. Linking code to a curated architectural group requires an explicit graph association, not fuzzy matching or another list in docstrings. Do not insert arbitrary metadata into component nodes: the current schema ignores unknown fields.

A reference to a spec file plus its hash establishes which artifact was referenced. It does not prove symbol-to-node membership, semantic review, or that the diagram is current against source.

## 6. Two pilot declarations and expected interpretation

The [module and class docstrings](../../src/sldb/selfdoc/python_symbol.py) are the pilot fixtures. They yield:

| Declaration | Declared ID | Semantic kind | Local tags | Effective tags |
|---|---|---|---|---|
| Module | `sldb.selfdoc.python_symbol` | `core` | `system:sldb`, `workspace:knowledge`, `topic:selfdoc` | Same as local tags |
| Class | `sldb.selfdoc.python_symbol.PythonSymbol` | `core` | `type:code.symbol` | `system:sldb`, `workspace:knowledge`, `topic:selfdoc`, `type:code.symbol` |

The AST supplies one immediate module → class containment fact. The class's AST kind remains `ClassDef`. The three inherited class tags cite the module as their origin; the class's ID, semantic kind, and `type:code.symbol` are local. Its base `BaseModel` is external to the selected SLDB source tree and must not be guessed to be a local class. No graph relation appears in either frontmatter block.

These results are normative and are checked by `tests/selfdoc/test_tag_inheritance.py::test_the_pilot_fixture_of_the_spec`. The module and class appear in the source graph under their declared IDs, with `local_tags` and `effective_tags` (each inherited value citing its origin). The generated Markdown records do not carry the effective tags, and the legacy `PythonScanner` emits no Markdown record for the module itself.

## 7. Acceptance and migration

Implementation is complete only after checks cover metadata parsing/diagnostics; ordinary docstrings; lexical scope including packages and nested/conditional definitions; inherited tag origin, override, removal, and store isolation; separate AST/semantic kinds; ID collisions and explicit legacy mappings; resolvable and unresolved dependencies; relation-type validation and producer-scoped reconciliation; and a validated spec2viz projection using the same identities and relation names.

Generated references must round-trip through SLDB, keep generated source facts distinct from authored graph knowledge, and synchronize idempotently. Existing authored `purpose`, `architecture`, and tags must not be silently overwritten: when migrating to source-owned prose, report differences and require an explicit reconciliation decision. A source docstring containing headings or fences must survive materialization without becoming an accidental document section.

Report missing declarations, missing explanation, unresolved mapping, and stale source separately. The current `semantic_gaps` counter only detects empty authored placeholders; it cannot establish that a source docstring lacks meaning or measure compliance with this contract.

Those checks are in place under `tests/selfdoc/` (metadata, tag inheritance, import context, re-exports, purpose, sync) and in spec2viz for the projection. Still open:

- The explicit mapping from a declared source ID to its generated Markdown document. Graph nodes use the declared ID; the Markdown records keep their qualified-name document IDs (`python-sldb-sldb-...`), which are not renamed silently (section 4).
- Effective tags and the module record in the generated Markdown, beyond the source graph.
- Broad annotation of the source tree. It should work in small reviewed batches, document only evidence-backed responsibilities, and record ambiguities instead of inventing architecture.

FILE:docs/architecture/notations-and-views.md
# Notaciones, Vocabularios Visuales y Vistas de Proyección en SLDB

## 1. Contexto y Justificación

Históricamente, los modelos de especificación visual de diagramas y proyección (`SpecDoc`, `SpecNodeDoc`, `NotationDoc`, `GlyphDoc`, `LinkDoc`, `PaletteDoc`, `ViewDoc`) y el motor de carga y validación de notaciones y paletas residían en la biblioteca `spec2viz`.

Esta separación causaba una dependencia circular y obligatoria hacia `spec2viz` en el ecosistema (por ejemplo, `graph_ui` o stores que alojan diagramas y vistas portables). Si `spec2viz` no estaba instalado en el entorno donde se ejecutaba `sldb` o un store se servía remotamente vía `sldb serve`, las operaciones sobre diagramas o la carga de modelos registrados degradaban o requerían adaptadores ad-hoc.

La absorción en `sldb` (iniciada en el nodo SV01 del plan `absorber-spec2viz-y-modelos-ui`) centraliza en `sldb` el vocabulario visual, las paletas, las 8 notaciones builtin y la capacidad de resolver referencias legacy sin depender de `spec2viz`.

---

## 2. Modelos de Vocabulario Visual (`sldb.models.notation_models`)

Los 7 modelos son subclases de `StructuredNLDoc` (`sldb.models.structured_nl_doc.StructuredNLDoc`) y se reexportan tanto en `sldb.models` como en `sldb.api`:

1. **`SpecDoc`**: Representa una especificación de diagrama completa como documento del almacén. Sus elementos hijos se vinculan mediante referencias hacia `SpecNodeDoc`, y apunta opcionalmente a una `NotationDoc`.
2. **`SpecNodeDoc`**: Elemento individual de un diagrama (nodo, componente, estado, clase, participante, actor). Declara contención (`__containment__ = {"contains": ["SpecNodeDoc"]}`) y referencias (`spec`, `refs`, `atom_refs`).
3. **`NotationDoc`**: Define una notación visual (tipo de diagrama, nivel `types`/`instances`/`both`, layout, marcadores, lista de `GlyphDoc` y `LinkDoc`, y paleta opcional).
4. **`GlyphDoc`**: Mapeo declarativo de un modelo del store (con predicado `where` opcional) a una forma visual primitiva (`shape`), compartimentos, etiquetas (`label`, `keyword`, `label_style`), y estilo (`kind`, `fill`, `stroke`, `icon`).
5. **`LinkDoc`**: Mapeo de una relación del store (arista o modelo reificado) a su representación gráfica (`line`, terminales `source_end` / `target_end`, rótulos y color).
6. **`PaletteDoc`**: Definición de paleta de colores (`backgrounds` e `ink` por tema claro/oscuro), catálogo de iconos y tokens de estilo semánticos por `kind`.
7. **`ViewDoc`**: Vista de proyección declarativa y portable sobre el grafo del almacén (`nodes`, `relations`, `direction`, `notation`, `layout`).

### Convergencia con GD25 en `ViewDoc` (SV-D3)
`ViewDoc` conserva los campos de proyección de grafo y añade soporte para vistas compuestas mediante dos campos opcionales:
- `params: dict = Field(default_factory=dict, description="Parametros opcionales de vista compuesta (GD25).")`
- `sections: list = Field(default_factory=list, description="Secciones opcionales de vista compuesta (GD25).")`

Ambos campos cuentan con validadores para inicializar `dict` y `list` respectivamente cuando se omiten en documentos existentes, preservando total compatibilidad hacia atrás en extracción y renderizado de plantillas.

---

## 3. Resolución y Retrocompatibilidad de Referencias (SV-D2)

Para garantizar compatibilidad inmediata con almacenes creados previamente cuyas configuraciones `.sldb/store.yaml` o `.sldb/core/store_index.yaml` registran modelos bajo el prefijo legacy:

```python
from sldb.api import resolve_model_ref

model = resolve_model_ref("spec2viz.sldb_models:NotationDoc")
# Retorna sldb.models.notation_models.NotationDoc
```

En `sldb.api.model_registry.model_reference`, cualquier referencia que utilice el módulo `spec2viz.sldb_models` se redirige transparentemente al módulo canónico `sldb.models.notation_models`.

---

## 4. Motor de Notaciones y Paletas (`sldb.notations`)

El submódulo `sldb.notations` expone:

- **Paletas (`palette.py`)**:
  - `PaletteSpec`, `ThemeColor`, `IconSet`, `KindStyle`.
  - Carga y validación semántica (`check_palette`) con verificación estricta de contraste WCAG:
    - Contraste gráfico WCAG 1.4.11 $\ge 3:1$ entre trazo y fondo por tema.
    - Contraste de texto WCAG 2.2 AA $\ge 4.5:1$ entre tinta y relleno por tema.
  - Resolución de colores (`resolve_color`) admitiendo tokens de paleta, pares `{light, dark}` o hex `#rrggbb`.
  - Paleta builtin `default` en `sldb/notations/palettes/default.yml`.

- **Notaciones (`notation.py`)**:
  - `NotationSpec`, `GlyphSpec`, `LinkSpec`, `MarkerSpec`.
  - Validación de formas primitivas (`SHAPES`), terminales (`TERMINALS`), tipos de diagrama (`DiagramType`) y relaciones esperadas por tipo (`KNOWN_RELATIONS`).
  - Las 8 notaciones builtin incluidas en `sldb/notations/builtin/`:
    - `uml-class.yml` (class)
    - `statechart.yml` (state)
    - `component.yml` (component)
    - `deployment.yml` (deployment)
    - `uml-sequence.yml` (sequence)
    - `activity.yml` (activity)
    - `component-view-matrix.yml` (component_view_matrix)
    - `reflection.yml` (reflection)

- **Resolución de Estilo (`styling.py`)**:
  - `resolve_style(glyph, kind, spec_kinds, palette)`: Resuelve propiedades visuales (`fill`, `stroke`, `icon`) aplicando la precedencia estricta:
    $$\text{Glifo de la notación} > \text{Spec kinds} > \text{Paleta de la notación}$$
  - `resolve_line_color(link, palette)`: Resuelve el color de línea en función de la paleta.

---

## 5. Resolvedor de Vistas y Vistas de Proyección (`sldb.api.notations`)

A partir de SV02, `sldb.api` provee los intérpretes canónicos del contrato de notación y de vistas proyectivas sin depender de librerías externas:

### 5.1 Resolvedor de Vistas (`notation_view.py`)
- `resolve_view(store, spec_ref, pythonpath=None)`:
  - Lee el `SpecDoc` del store, valida su coincidencia con `NotationDoc.diagram_type` y resuelve los nodos, aristas y leyendas.
  - Retorna `{spec, title, diagram_type, notation, palette, level, layout, nodes, links, fragments, skipped, legend}`.
- `resolve_documents(store, notation_ref, doc_refs, *, relation_refs=None, spec_style=None, pythonpath=None)`:
  - Aplica la notación a cualquier conjunto de documentos del store sin requerir un `SpecDoc`.
  - Casado de glifos por modelo + evaluación de predicado `where` sobre el payload aplanado (`flatten()`).
  - Extracción de compartimentos con rutas punto (`data.attributes`, `data.methods`).
  - Interpolación de plantillas `{campo}` y estereotipos `keyword` (`«{kind}»`) sin dejar variables huérfanas.
  - Detección y agrupamiento de fragmentos UML consecutivos (`fragments_of()`) por operador `data.group`.
  - Generación de leyenda completa (`glyphs`, `links`, `kinds`).

### 5.2 Vistas de Proyección (`projection_view.py`)
- `evaluate_projection_view(store, view_or_ref, pythonpath=None)`:
  - Evalúa la consulta de nodos (`[{model, where}]`) y aristas (`RelationFilter(relations, direction)`) sobre el grafo del almacén.
  - Si la vista especifica una `notation`, invoca `resolve_documents` y adjunta estilo para nodos (`styled_nodes`), aristas (`edge_styles`), `ink` de paleta por tema y `legend`.
- `list_projection_views(store, pythonpath=None)`:
  - Lista todos los `ViewDoc` registrados en el almacén.
- `save_projection_view(store, name, view, pythonpath=None, actor=None)`:
  - Guarda o actualiza un `ViewDoc` en el almacén bajo `sldb/views/<name>.md`.

### 5.3 Sincronización al Almacén (`notation_sync.py`)
- `sync_palette(store, name_or_path="default")`:
  - Escribe el `PaletteDoc` correspondiente en `sldb/palettes/` y registra modelos si hiciera falta.
- `sync_notation(store, name_or_path)`:
  - Escribe `NotationDoc`, `GlyphDoc`, `LinkDoc` y sus `RelationTypeDoc` asociados en `sldb/notations/<name>/`, además de su paleta vinculada.

---

## 6. Superficie CLI y HTTP Serve

### 6.1 CLI (`sldb notations`)
Disponible con envelope JSON (`sldb --envelope notations ...`):
- `sldb notations list [--views]`: Lista las notaciones y paletas builtin y registradas en el store (o las vistas proyectivas si se indica `--views`).
- `sldb notations sync [--notation <name|path>] [--palette <name|path>]`: Sincroniza notaciones o paletas en el store.
- `sldb notations view <spec> [--projection]`: Resuelve la vista de un `SpecDoc` o evalúa una proyección (`--projection`).
- `sldb notations resolve --notation <notation> --docs <Model:name ...>`: Resuelve un conjunto arbitrario de documentos bajo una notación.

### 6.2 HTTP Serve (`sldb serve`)
- `GET /notations`: Lista notaciones y paletas builtin y del store.
- `GET /notations/view?spec=<spec_ref>`: Resuelve un `SpecDoc`.
- `POST /notations/resolve`: Resuelve un conjunto de documentos `{notation, docs, [relations], [style]}`.
- `GET /views/projection`: Lista los `ViewDoc` del store.
- `GET /views/projection/evaluate?view=<ref>`: Evalúa una vista proyectiva por referencia.
- `POST /views/projection/evaluate`: Evalúa una vista proyectiva pasada en el body JSON.
- `POST /views/projection/save`: Guarda un `ViewDoc` `{name, view}`.

FILE:docs/requests/sldb-knowledge-graph-integration.md
---
status: open
priority: p1
assigned_to: sldb-team
created: 2026-04-22
labels:
  - feature-request
  - knowledge-graph
  - integration
  - reasoning
  - federation
---

# Feature Request: sldb ↔ Knowledge Graph Integration

## Context

We have two systems with complementary strengths:

**sldb:**
- Self-describing templates (`__template__`)
- Roundtrip validation (idempotency guarantee)
- Hash cascade (Merkle-style integrity)
- Federation (cross-repo stores)

**wiki_compiler (knowledge graph):**
- Graph traversal (50+ node types)
- Facets (compliance, git, source, semantics)
- OWL reasoning (implicit relationships)
- Energy audit (systemic health)
- Context routing (relevant docs for task)

Together they can do things neither can do alone.

## Clarification: Relationship with kg_db

**IMPORTANT:** This request and `extract-kg_db-from-hum.md` are **complementary, not contradictory**.

| Library | Scope |
|---|---|
| **sldb + graph/ (minimal)** | Edges between documents, cross-repo links, basic traversal |
| **kg_db (full)** | OWL reasoning, energy audit, context routing, cleansing |

**sldb gets MINIMAL graph capabilities. kg_db does FULL reasoning.**

### Division of Labor

```
sldb (minimal graph)
├── .sldb/documents/    ← documents
├── .sldb/models/      ← contracts
└── .sldb/graph/       ← edges + links ONLY
                         ← NO OWL
                         ← NO energy
                         ← NO context

kg_db (full reasoning)
├── knowledge_graph.json
├── graph/             ← full operations
├── reasoning/         ← OWL + SHACL
├── energy/           ← audit
├── context/          ← routing
└── cleansing/        ← proposals
```

### What sldb DOES NOT Get

This request does NOT add to sldb:
- OWL reasoner
- Energy audit
- Context routing
- Cleansing proposals
- Full graph operations

These belong to kg_db.

## What sldb Gets (Minimal Graph)

### 1. Graph Traversal for Cross-Doc Relationships

### 1. Graph Traversal for Cross-Doc Relationships

**Current in wiki_compiler:** `src/wiki_compiler/query_executor.py` <!-- gone -->

Documents are nodes in a directed graph with typed edges:

```python
class Edge(BaseModel):
    target_id: str
    relation_type: Literal[
        "contains",
        "depends_on",
        "reads_from",
        "writes_to",
        "documents",
        "transcludes",
        "extends",
        "implements",
    ]
```

**What sldb needs:**

```python
# In .sldb/documents/<Doc>.yaml
relationships:
  - target: analyzer:ConceptDoc.foo.md
    relation: extends
  - target: hum:ADRDoc.bar.md
    relation: documents
  - target: self:Chapter.1.md
    relation: contains
```

**Reference implementation:**
- `src/wiki_compiler/contracts.py:Edge` — typed edge model <!-- gone -->
- `src/wiki_compiler/graph_utils.py:add_knowledge_node()` — add edges to graph <!-- gone -->
- `src/wiki_compiler/query_language.py` — query DSL for graph traversal <!-- gone -->

**Command:**

<!-- gone -->
```bash
sldb doc link --from foo.md --to bar.md --relation documents
sldb doc links foo.md --relation documents
# Returns: bar.md

sldb doc tree --from foo.md --depth 2
# Shows full relationship tree
```

---

### 2. Facets: Multi-Dimensional Doc Metadata

**Current in wiki_compiler:** `src/wiki_compiler/contracts.py:KnowledgeNode` <!-- gone -->

Every node has optional facets:

```python
class KnowledgeNode(BaseModel):
    identity: SystemIdentity
    edges: list[Edge]
    semantics: SemanticFacet | None    # What does this do?
    ast: ASTFacet | None          # Code structure
    io_ports: list[IOFacet]      # Input/output
    compliance: ComplianceFacet | None  # Implementation status
    adr: ADRFacet | None          # Architecture decision
    test_map: TestMapFacet | None    # Testing strategy
    git: GitFacet | None          # Git metadata
    source: SourceFacet | None       # Provenance
```

**What sldb needs:**

```yaml
# .sldb/documents/foo.yaml
facets:
  compliance:
    status: implemented
    failing_standards: []
  git:
    blob_sha: abc123
    created_at_commit: def456
    last_modified: "2026-04-22"
  source:
    compiled_from: wiki-compiler
    compiled_at: "2026-04-22T14:00:00Z"
  test_map:
    test_type: unit
    coverage_percent: 85.0
```

**Reference implementation:**
- `src/wiki_compiler/contracts.py:ComplianceFacet` — implementation status <!-- gone -->
- `src/wiki_compiler/contracts.py:GitFacet` — git tracking <!-- gone -->
- `src/wiki_compiler/contracts.py:SourceFacet` — provenance <!-- gone -->
- `src/wiki_compiler/facet_injectors.py` — how facets are populated <!-- gone -->

---

### 3. OWL Reasoning: Implicit Relationships

**Current in wiki_compiler:** `src/wiki_compiler/owl_reasoner.py` <!-- gone -->

OWL ontology reasoner infers implicit relationships:

```python
from owlready2 import World, sync_reasoner

# If ConceptDoc extends Document
# And Document has a "readme" relationship
# Then ConceptDoc has a "readme" relationship (inferred)

# Run reasoner
world = World()
graph = world.get_ontology("https://hum.ai/")
sync_reasoner(graph)
```

**What sldb needs:**

<!-- gone -->
```bash
# Model inheritance as OWL axioms
sldb model owl ConceptDoc --output concept.owl
```

```turtle
# Generated OWL:
:ConceptDoc rdfs:subClassOf :Document .
:Document rdfs:subClassOf :StructuredNLDoc .

# If query asks for all subclasses of Document:
# OWL reasoner returns: ConceptDoc, ADRDoc, ReferenceDoc, ...
```

**Reference implementation:**
- `src/wiki_compiler/owl_reasoner.py` — owlready2 integration <!-- gone -->
- `src/wiki_compiler/owl_backend/owl_reasoner.py:run_owl_reasoner()` <!-- gone -->
- `src/wiki_compiler/shacl/validator.py` — SHACL shape validation <!-- gone -->

**Command:**

<!-- gone -->
```bash
sldb model subclasses ConceptDoc
# Returns: HowToDoc, ReferenceDoc, IndexDoc, ...

sldb model ancestors HowToDoc
# Returns: HowToDoc → ConceptDoc → Document → StructuredNLDoc

sldb doc infer-links foo.md
# Returns: inferred relationships from OWL reasoner
```

---

### 4. Energy Audit: Systemic Health

**Current in wiki_compiler:** `src/wiki_compiler/energy.py` <!-- gone -->

Systemic energy measures health of the entire knowledge base:

```python
class SystemicEnergy(BaseModel):
    energy_score: float
    node_count: int
    edge_count: int
    compliance_violations: int
    perturbations: int
    redundant_nodes: int
    boilerplate_ratio: float
```

**Energy breakdown:**

```python
structural_energy = redundancy_check(graph)     # Duplicate nodes
abstraction_energy = complexity_check()     # Long files, complex functions
violation_energy = compliance_violations    # Failing standards
perturbation_energy = git_drift()          # Uncommitted changes
```

**What sldb needs:**

<!-- gone -->
```bash
sldb store energy --report
```

```yaml
energy_score: 42.5
model_count: 7
document_count: 156
validated_documents: 142
unvalidated_documents: 14
hash_drift: 3
orphan_documents: 2
redundant_models: 1  # Model with >10 doc instances
boilerplate_ratio: 0.23
```

**Reference implementation:**
- `src/wiki_compiler/energy.py:run_energy_audit()` — full energy calculation <!-- gone -->
- `src/wiki_compiler/energy.py:calculate_redundancy()` — Jaccard similarity <!-- gone -->
- `src/wiki_compiler/perception.py:build_status_report()` — zone status <!-- gone -->

---

### 5. Context Routing: Relevant Docs for a Task

**Current in wiki_compiler:** `src/wiki_compiler/context.py` <!-- gone -->

Given a task, retrieve relevant docs:

```python
class ContextRequest(BaseModel):
    node_ids: list[str]
    task_hint: str | None
    depth: int = 1
    include_planned: bool = False

class ContextBundle(BaseModel):
    nodes: list[KnowledgeNode]
    edges: list[Edge]
    rationale: dict[str, str]
    scores: dict[str, float]
    prose: dict[str, str]
```

**What sldb needs:**

<!-- gone -->
```bash
sldb context "review architecture decision"
# Returns: relevant ADRs, their models, related concepts, ...
# Scored by relevance to task

sldb context "audit sldb store"
# Returns: store_index.yaml, models/, documents/
# Tracked in .sldb/context_cache/
```

**Reference implementation:**
- `src/wiki_compiler/context.py:build_context_bundle()` — context routing <!-- gone -->
- `src/wiki_compiler/query_executor.py:StructuredQuery` — structured queries <!-- gone -->
- `src/wiki_compiler/registry.py` — facet registry <!-- gone -->

---

### 6. Cleansing: Structural Optimization

**Current in wiki_compiler:** `src/wiki_compiler/cleanser.py` <!-- gone -->

Proposals to optimize the graph:

```python
class CleansingProposal(BaseModel):
    node_id: str
    operation: Literal["destroy", "relocate", "split", "merge"]
    rationale: str
    requires_human_approval: bool = True
```

**What sldb needs:**

<!-- gone -->
```bash
sldb cleanse --dry-run
# Proposes:
# - merge: redundant_concept_a.md + redundant_concept_b.md
# - split: large_adr.md into context.md + decision.md + consequences.md
# - relocate: orphan_docs/ → tracked/
# - destroy: duplicate_docs/
```

**With sldb validation:**

<!-- gone -->
```bash
sldb cleanse --apply --proposal merge
# sldb validate roundtrips the merged doc
# If fails: proposal rejected, fix required
# If passes: merge applied + committed
```

**Reference implementation:**
- `src/wiki_compiler/cleanser.py:detect_cleansing_candidates()` <!-- gone -->
- `src/wiki_compiler/cleanser.py:apply_proposal()` <!-- gone -->
- `src/wiki_compiler/validation.py:validate_model_input_roundtrip()` — sldb can use this directly <!-- gone -->

---

## Implementation Priorities

### Phase 1: Foundation (Take from wiki_compiler as-is)

| Feature | File | What to port |
|---|---|---|
| Typed edges | `contracts.py:Edge` | Copy to sldb |
| Facets | `contracts.py:ComplianceFacet` | Copy to sldb |
| Model registry | `registry.py` | Adapt for sldb models |

### Phase 2: Reasoning

| Feature | File | What to port |
|---|---|---|
| OWL reasoner | `owl_reasoner.py` | Port + adapt |
| SHACL shapes | `shacl/validator.py` | Port + adapt |

### Phase 3: Systemic View

| Feature | File | What to port |
|---|---|---|
| Energy audit | `energy.py` | Adapt for hash cascade |
| Context routing | `context.py` | Adapt for sldb docs |
| Cleansing | `cleanser.py` | Adapt for sldb |

---

## Specific Code References

### Edge Model (copy directly)

<!-- gone -->
```
src/wiki_compiler/contracts.py:12-29
```

```python
class Edge(BaseModel):
    target_id: str
    relation_type: Literal[
        "contains", "depends_on", "reads_from",
        "writes_to", "documents", "transcludes",
        "extends", "implements",
    ] = Field(description="...")
    metadata: dict[str, Any] = Field(default_factory=dict)
```

### Facet Models (adapt)

<!-- gone -->
```
src/wiki_compiler/contracts.py:145-205
```

Compliance, Git, Source, Semantic, AST, I/O, Test, ADR facets.

### OWL Reasoner (adapt)

<!-- gone -->
```
src/wiki_compiler/owl_reasoner.py:32-45
src/wiki_compiler/shacl/shapes.py:40-55
```

Uses owlready2 + SHACL shapes.

### Energy Audit (adapt)

<!-- gone -->
```
src/wiki_compiler/energy.py:150-250
```

Calculates structural, abstraction, violation, perturbation energy.

### Context Routing (adapt)

<!-- gone -->
```
src/wiki_compiler/context.py:75-120
```

```python
def build_context_bundle(request: ContextRequest) -> ContextBundle:
    nodes = query_graph(request)
    edges = get_edges_between(nodes)
    scores = calculate_relevance(nodes, request.task_hint)
    return ContextBundle(...)
```

---

## Questions for the Team

1. **Architecture:** Should sldb embed a mini-graph, or should it delegate to wiki_compiler?
2. **OWL integration:** Port owlready2, or use a lighter reasoner?
3. **Energy:** Use hash cascade (sldb-native) vs node count (wiki-native)?
4. **Federation:** Should federation links be graph edges?
5. **Backward compatibility:** How to add without breaking existing store?

---

Submitted by: hum team
Date: 2026-04-22
Repo: https://github.com/jpcosec/hum

FILE:docs/user-manual.md
# SLDB — Manual de usuario

Todo lo que aparece acá fue ejecutado contra un store real antes de escribirse.
Los errores que se muestran son los errores que salieron de verdad.

---

## 1. Qué es SLDB

**Un motor que mantiene un documento, una base de datos y un grafo como tres
caras de lo mismo, a partir de un solo contrato.**

Vos declarás un modelo: qué campos tiene un tipo de documento y dónde va cada uno
en la página. De ese contrato SLDB deriva:

| Cara | Para qué sirve |
|---|---|
| El documento `.md` | leerlo, editarlo, versionarlo en git |
| El store `.sldb/` | consultarlo por dirección, buscar, indexar |
| El grafo | ver qué se conecta con qué |

**Ninguna es la original.** No hay fuente y salida, no hay original y copia. Hay
un contrato y tres proyecciones equivalentes.

Si dos no calzan, no es que una mienta: es que el motor falló, y hay un
diagnóstico específico que te dice cuál y por qué.

### Qué NO es

- **No es un editor de Markdown.** El Markdown es cómo se guarda.
- **No es una base de datos con export.** No hay dos cosas que sincronizar.
- **No es un generador de documentación.** No hay "fuente" y "salida".

---

## 2. Quickstart

Siete pasos, de cero a un documento consultable.

### 2.1 · Definir el modelo

```python
# models.py
from pydantic import Field
from sldb.models.structured_doc import StructuredNLDoc

class NoteDoc(StructuredNLDoc):
    """A short note with a body and optional source."""
    __semantics__ = {"type": ["knowledge", "note"]}
    __template__ = """---
id: ⸢rev•id⸥
title: ⸢rev•title⸥
tags: ⸢rev,list•tags⸥
source: ⸢optrev•source⸥
---

# ⸢render•title⸥

## Body

⸢rev•body⸥
""".strip()

    id: str = Field(description="Stable note id.")
    title: str = Field(description="Note title.")
    tags: list[str] = Field(default_factory=list, description="Semantic tags.")
    source: str | None = Field(default=None, description="Where this came from.")
    body: str = Field(description="The note content.")
```

`Field(description=...)` es **obligatorio**. Sin descripción el modelo ni se
define: tira `TypeError`. No es estilo, es parte del contrato.

### 2.2 · Crear el store y registrar

```bash
python -m sldb stores init --path .
# Initialized store at /tmp/manual-test/.sldb

python -m sldb models add models:NoteDoc --store .sldb --pythonpath .
# Registered 'NoteDoc'
```

### 2.3 · Crear un documento

```yaml
# payload.yaml
id: nota-uno
title: Primera nota
tags: [demo, manual]
body: |
  Esto es el cuerpo de la nota.
```

```bash
python -m sldb docs create --model NoteDoc -o notas/nota-uno.md payload.yaml \
  --store .sldb --pythonpath .
# Created and tracked 'nota-uno'
```

Resultado en disco:

```markdown
---
id: nota-uno
title: Primera nota
tags:
- demo
- manual
---

# Primera nota

## Body

Esto es el cuerpo de la nota.
```

Dos cosas que pasaron solas:

- `source` era `None` y **su línea entera desapareció**. Eso es `optrev`.
- `title` aparece dos veces en el template (`rev` en frontmatter, `render` en el
  H1) y una sola vez como dato.

### 2.4 · Leer por dirección

```bash
python -m sldb ls st --store .sldb --pythonpath .
# st.{NoteDoc}

python -m sldb get st.{NoteDoc}.nota-uno.title --store .sldb --pythonpath .
# { "result": "Primera nota" }

python -m sldb get st.{NoteDoc}.nota-uno.tags.0 --store .sldb --pythonpath .
# { "result": "demo" }
```

Las listas se direccionan por índice. Los dicts por clave. Tan profundo como
llegue el payload.

### 2.5 · Escribir por dirección

```bash
python -m sldb fields append docs/nota-uno/tags nuevo --store .sldb --pythonpath .
# Updated field payload for 'nota-uno'
```

El `.md` se reescribió solo, y ambos hashes rotaron:

```
source_hash : 5ecfa5b2… → f450d203…
content_hash: ce2d3ad6… → baf72f1d…
```

**Nunca abrís el archivo para leer o cambiar un valor.**

---

## 3. Los marcadores

El template decide qué es cada campo.

| Marcador | Significa |
|---|---|
| `⸢rev•campo⸥` | va y vuelve. Es dato editable. |
| `⸢optrev•campo⸥` | igual, pero un valor `None` **puede borrar la línea entera** |
| `⸢render•campo⸥` | solo de ida. Se ve, no se extrae. |
| `⸢py•expr⸥` | expresión calculada al renderizar |

Traits: `⸢rev,list•tags⸥`, `⸢rev,markdown•description⸥`, `⸢rev,dict•meta⸥`.

### `optrev` con precision

La linea se borra **solo** si se cumplen las dos condiciones:

1. el valor es `None` - no cadena vacia, no `[]`, no `{}`
2. el marcador esta solo en su linea, o en la forma `clave: <optrev:clave>`

En cualquier otro caso el marcador se reemplaza por texto vacio y la linea
sobrevive:

| Valor | Que pasa |
|---|---|
| `None`, marcador solo en su linea | la linea desaparece |
| cadena vacia | renderiza `source: ''` - la linea queda |
| `[]` / `{}` | renderiza vacio - la linea queda |
| cualquiera, marcador compartiendo linea | se reemplaza por vacio, la linea queda |

Lo ultimo aplica a celdas de tabla, bullets y marcadores con texto al lado.

### Error real: un campo que solo es `render`

Primer intento del quickstart, con `title` únicamente en el H1:

```
title
  Field required [type=missing, input_value={'id': 'nota-uno', ...}]
```

El campo existía en el payload, pero `render` **no se extrae de vuelta**. Al
verificar el round-trip, `title` no aparecía. Un campo que es dato necesita una
declaración `rev` en algún lado.

---

## 4. El store

### Anatomía

```
.sldb/                                 ← se versiona entero en git
├── store.yaml                         ← la declaración del store
└── core/
    ├── store_index.yaml               ← modelos registrados
    ├── models/<Modelo>.yaml           ← el nodo del modelo: hashes y conteo
    └── documents/<Modelo>/<doc>.yaml  ← un archivo por documento
.sldb_cache/                           ← hermana de .sldb/, ignorada por git, se puede borrar
├── sections/       ← secciones por documento
├── edges/          ← shards del grafo
├── semantic/       ← indice semantico
├── graphs/         ← grafos generados (selfdoc)
├── locks/          ← exclusion mutua
├── edges.yaml      ← indice raiz de aristas
└── semantic_dag.yaml
```

(Hasta el 2026-11-04 la caché era `.sldb/runtime/`, con un `journal/` que ya no existe:
`sldb stores migrate-layout` la mueve. El pasado del store se consulta con
`sldb docs history <doc>`.)

**`.sldb` es estado, `.sldb_cache` es caché.** Si la caché se corrompe,
`stores build` (o `stores update`) la rehace desde los documentos.

Un archivo por documento ("shard"): dos ramas de git que tocan documentos
distintos no chocan.

### Qué guarda de un documento

```yaml
name: nota-uno
path: notas/nota-uno.md
source_hash: f450d203…
content_hash: baf72f1d…
semantic_tags: [demo, manual, type.knowledge.note, ...]
```

**No guarda el contenido.** Guarda dónde está, cómo verificarlo y cómo
encontrarlo.

### Los cuatro hashes

| Nombre | Alias viejo | Firma | Se mueve cuando |
|---|---|---|---|
| `store_hash` | `hash_a` | el store entero | cualquier write |
| `model_hash` | `hash_b` | un modelo | cualquier write de ese modelo |
| `source_hash` | `hash_c` | el **texto** markdown | cualquier reescritura |
| `content_hash` | `hash_d` | el **payload extraído** | solo si cambian los campos |

`model_hash` no es una hoja: se compone de **dos hijos** que se guardan por
separado en `ModelsIndex` justo para poder atribuirle la culpa a uno:

```
model_hash = hash(contract_hash + roster_hash)
```

| Hijo | Firma | Se mueve cuando |
|---|---|---|
| `contract_hash` | los campos del modelo (nombre, tipo, descripción) **+ el template** | tocás el modelo |
| `roster_hash` | la lista de documentos `(nombre, source_hash, content_hash)` | agregás, sacás o cambiás un documento |

Por eso `stores check` puede decirte "se movió el contrato" en vez de reportar un
mismatch pelado. Y por eso un campo agregado a la clase mueve el nodo del modelo
aunque ningún `.md` se haya tocado: el mismo texto ahora extrae otra cosa.

### Hash por field

Además del `content_hash`, cada documento guarda un hash **por campo**:

```yaml
content_hash: d43b4ed540a6…
field_hashes:
  id:    19eb5a8300ee…
  title: f6a129542311…
  tags:  87cff60a4a98…
  body:  1d10008a5a36…
```

`content_hash` sigue firmando el payload entero — es el token de concurrencia
optimista de `/save`. `field_hashes` va **al lado**, no lo reemplaza ni se deriva
de él. Sirve para saber *cuál* campo se movió:

```
what : fields changed under the model's contract (a real data change) … [fields: title]
```

Un mapa **vacío** significa "no se pudo calcular" (store escrito antes de que esto
existiera, o documento que ya no extrae), **nunca** "ningún campo cambió" — eso ya
lo responde `content_hash`. Ante un mapa vacío el diagnóstico no inventa
atribución y cae al documento completo.

Ojo con los nombres: `source` es el markdown fuente, `content` es el contenido
semántico. Es al revés de lo que suena.

Las claves persistidas en disco siguen siendo `hash_c`/`hash_d`: renombrarlas
invalidaría todos los stores existentes.

`content_hash` es **función pura del payload**. Mismo payload, mismo hash.
Por eso sirve como token de concurrencia optimista.

---

## 5. Diagnóstico

La distinción entre los dos hashes de documento es todo el veredicto.

### Reformateo: texto que se mueve, campos quietos

```bash
printf '\n' >> notas/nota-uno.md
python -m sldb stores check --store .sldb
```

```
PASS: store integrity — 1 documents in 1 models — 1 reformatted (ok)
```

Un salto de línea de más cambió `source_hash`, no `content_hash`. No hay
problema.

### Cambio real de datos

```bash
sed -i 's/^title: Primera nota/title: Titulo cambiado a mano/' notas/nota-uno.md
python -m sldb stores check --store .sldb
```

```
FAIL: store integrity — 1 documents in 1 models — 1 damaged

NoteDoc: 1 documents
  data_mutation: nota-uno
    what    : fields changed under the model's contract (a real data change) ... `stores update` accepts it, but confirm the change was intended first
    inspect : notas/nota-uno.md
    fix     : decide first: if the edit was intended, sldb stores update; if not, restore the file (git checkout -- <path>) before updating, because the index holds the previous hash and nothing else holds the previous value
    source_hash (text)  : on disk 9e52d372344f != in index f450d203bd21
    content_hash (fields): on disk a4e646979574 != in index baf72f1d0637

next: 1 finding(s) need a decision before any command is run (see 'fix:' above).
```

(En la salida real cada campo es UNA sola linea; aca van cortados para que entren.)

No dice "corrupto". Dice `data_mutation` y **"decide first"**.

`on_disk` es lo recalculado del archivo ahora. `in_index` es lo que el store
registró al último write. **Ninguno es autoritativo**: cuál está viejo es
justamente lo que estás averiguando.

---

## 6. El grafo

### Cómo se generan las aristas

Cinco fuentes, y **solo cinco**:

1. **Estructura** — todo documento aporta su nodo, sus secciones y sus tags
2. **Documentos especiales** — `RelationTypeDoc`, `RelationDoc`, y documentos
   con tag de anchor
3. **Modelos** — cada modelo aporta su nodo, un nodo por campo, `has_field`,
   `extends`
4. **Referencias declaradas** — `__references__` aporta `references` y
   `__containment__` aporta `contains`, una arista por id, con el nombre del
   campo en la arista
5. **Composiciones** — `__compositions__` aporta `composes`, una arista por ref,
   con el campo compuesto, el campo que guarda los refs y el ref tal como fue
   escrito

Las tres últimas son `origin: "schema"`, igual que `has_field` y `extends`:
apuntar a un documento que no está trackeado se descarta en `resolve_edges` en vez
de reportarse, porque el modelo declaró una forma y no una aserción autoral. Un
documento especial no aporta referencias declaradas: sus campos de id ya son la
arista que ese documento contribuye.

> **Cuidado:** el id declarado se escribe `Modelo:nombre`. Un nombre pelado es
> ambiguo entre modelos y se omite en vez de adivinarlo, así que un campo de
> `__references__` que guarde rutas no produce aristas.
>
> También se exponen por HTTP: `/schema` devuelve los dos; `fields_routes` expone
> únicamente `__references__`, como `is_reference`.

Un ref de composición sí es una ruta del proyecto, no un id. Qué documento es
dueño de una ruta no lo sabe un shard solo, así que la arista se emite con la ruta
en `metadata["ref_path"]` y el target se resuelve al componer el índice, donde ya
viven las reglas que cruzan documentos. `./sub/a.md` y `sub/a.md` son el mismo
documento; una ruta de la que nadie es dueño no deja arista.

Eso es lo que hace que el radio de impacto recorra la composición: con
`edges to` sobre un hijo salén los padres que lo componen y que quedaron rancios
al cambiarlo.

### Los nodos tienen tipo

```
sldb://document/NoteDoc:nota-uno
sldb://section/NoteDoc:nota-uno#body
sldb://model/NoteDoc
sldb://semantic_tag/type.knowledge.note
sldb://anchor/...
```

**Las secciones son nodos.** Por eso podés citar un fragmento, no solo un
archivo.

### Registrar el vocabulario

```bash
python -m sldb edges init --store .sldb --pythonpath .
# Initialized relations: models added: 2 · builtin relation types written: 11
#                        · predicates added: 11
```

Los 11 builtin: `has_document`, `has_section`, `has_field`, `has_model`,
`extends`, `tagged_as`, `names`, `applies_to_source`, `applies_to_target`,
`semantic_parent`, `semantic_equivalent`.

### Declarar un tipo de relación nuevo

Un tipo de arista **es un documento SLDB**:

```yaml
# rt.yaml
title: Comments On
name: comments_on
direction: directed
cardinality: many_to_one
axis: WHAT
source_types: [LinkedDoc]
target_types: [NoteDoc]
condition: ""
description: One note commenting on another.
```

```bash
python -m sldb docs create --model RelationTypeDoc -o rel/comments-on.md rt.yaml \
  --store .sldb --pythonpath .
# Created and tracked 'comments-on'
```

| Campo | Qué define |
|---|---|
| `name` | el verbo que llevará cada arista |
| `direction` | dirigida, o no dirigida (se materializa en ambos sentidos) |
| `cardinality` | validado al ingerir |
| `source_types` / `target_types` | qué modelos puede conectar |
| `axis` | eje predicativo: WHAT, WHY, HOW, WHERE, WHEN, PROVENANCE |
| `condition` | condición que heredan todas las aristas del tipo |

Las relaciones internas de SLDB también son `RelationTypeDoc`. **El grafo se
describe a sí mismo con el mismo mecanismo que usás vos.**

### Crear una arista

```yaml
# ed.yaml
title: enlace-uno comenta nota-uno
source_id: LinkedDoc:enlace-uno
target_id: NoteDoc:nota-uno
relation_type: comments_on
condition: ""
notes: Creada a mano para el manual.
```

```bash
python -m sldb docs create --model RelationDoc -o rel/edge-uno.md ed.yaml \
  --store .sldb --pythonpath .
python -m sldb edges rebuild --store .sldb --pythonpath .
```

Consultarla — **por node id, no por nombre de documento**:

```bash
python -m sldb edges show "sldb://document/LinkedDoc:enlace-uno" --store .sldb
```

```json
{
  "metadata": {
    "origin": "relation_doc",
    "relation_doc": "edge-uno",
    "condition": "",
    "axis": "WHAT"
  }
}
```

El `axis: WHAT` no estaba en la arista: **se heredó del tipo**.

### Análisis

```bash
python -m sldb graph path "sldb://document/LinkedDoc:enlace-uno" \
                         "sldb://document/NoteDoc:nota-uno" --store .sldb
# ["sldb://document/LinkedDoc:enlace-uno", "sldb://document/NoteDoc:nota-uno"]

python -m sldb edges check --store .sldb
# Edges OK
```

Doce comandos disponibles:

| Comando | Qué responde |
|---|---|
| `neighborhood` | vecinos hasta profundidad N |
| `path` | cómo se conecta A con B |
| `cycles` | ciclos donde debería ser un DAG |
| `order` | orden topológico de dependencias |
| `components` | qué anda junto y qué quedó suelto |
| `central` | de qué nodos depende el resto |
| `similar` | qué se parece a esto, por destinos compartidos |
| `snapshot` | exportar o cargar el grafo portable |
| `get` | un nodo del índice |
| `list` | todos los node ids |
| `query` | consulta estructurada desde un JSON |
| `ingest-sldb` | convertir un export semántico a node-link JSON |

Corre sobre networkx. PageRank pide scipy aparte.

---

## 7. Qué se puede representar

`StructuredNLDoc` declara dos ejes:

```python
__semantics__ = {
    "representation": ["markdown"],      # cómo se guarda — siempre markdown
    "source": ["document", "markdown"],  # qué describe — cualquier cosa
}
```

**El Markdown es el formato, no el tema.** Un subclase cambia `source` cuando
describe código, datos u otra fuente.

Modelos que vienen con SLDB:

| Modelo | `source` | Qué representa |
|---|---|---|
| `PythonSymbolDoc` | `code, python` | una función o clase |
| `CliCommandDoc` | — | un comando de CLI |
| `SurfaceDoc` | — | un subsistema completo |
| `RelationTypeDoc` | — | un tipo de arista |
| `RelationDoc` | — | una arista concreta |
| `AnchorDoc` | — | un alias de pron: una palabra y lo que nombra; resuelve pero no verifica (ver [anclaje](architecture/anchoring.md)) |
| `KnowledgeTag` | — | vocabulario |

Por eso SLDB se auto-documenta: hay un adaptador que lee argparse y genera
`CliCommandDoc`.

**El patrón:** cualquier cosa que puedas describir con campos estables se puede
representar.

---

## 8. Herencia

Los modelos heredan como clases pydantic normales. Ejemplo tomado de una KB
real (`knowledge_antonia-cobranza`); los modelos son del consumidor, no de SLDB:

```
DomainAtom → IndexProxies → StructuredNLDoc

DomainAtom   aporta: id, title, five_wh_one_plus, answer, tags, domain_ref, provenance
IndexProxies aporta: summary, summary_en
```

Y la herencia es **consultable**:

```bash
python -m sldb ls "st.{IndexProxies+}" --store .sldb --pythonpath .
```

El `+` significa "este modelo y todos sus descendientes". Recorre el MRO, así que
la clase base **ni necesita estar registrada**.

---

## 9. Proyección y composición

Dos ideas distintas que conviene no mezclar.

### Proyección — lo mismo desde otro ángulo

- **Las tres caras**: documento, store, grafo
- **`render` vs `rev`**: `title` vive en frontmatter y se proyecta al H1
- **`IndexProjection`**: qué documentos admite un consumidor y cómo lee el texto
  representativo de cada uno

`IndexProjection` tiene un detalle importante: `text_id` nombra la forma de leer,
*"so a change of representation invalidates the index the same way a change of
embedder does"*. Si cambiás qué parte del documento considerás "el texto", el
índice queda inválido. Por eso una cita nunca queda huérfana.

- **`FieldProjection`**: lo mismo, un piso más abajo — qué *fields* de cada
documento se indexan (por defecto excluye identidad y bookkeeping: `id`, `name`,
`slug`, `path`, `tags`, hashes) y cómo se lee el texto de uno.

Cada field es una unidad de indexación propia: dirección
`docs/<Modelo>/<doc>/<campo>` — la misma que acepta `sldb fields` — y hash de ese
field (`DocumentEntry.field_hashes`), no el del documento entero. Es el mismo
índice con clave más fina: editar un campo de un documento de cuarenta re-embebe
uno.

### Composición — varios documentos en uno

| Mecanismo | Qué hace | Vuelta atrás |
|---|---|---|
| `__compositions__` | un campo se arma formateando documentos hijos | ❌ |
| `![[transclusión]]` | expande el texto de otro documento | ❌ |
| `[[link]]` | referencia, no expande | — |

**Límites conocidos, documentados en `composition_modes.md`:**

- No hay edit-through: no se puede editar el hijo desde donde está compuesto
- No hay composición por query: `source_field` exige lista explícita de rutas

---

## 10. Las tres APIs

### CLI

`python -m sldb ...` — para humanos y scripts.

### Python (`sldb.api`) — la preferida para integrar

> *"the store, model and document operations the CLI performs, **as functions**.
> Consumers call these instead of instantiating `sldb.cli` command classes with
> fake argparse namespaces."*

- devuelve **modelos pydantic**, no imprime
- **lanza excepciones**, no hace `exit`
- capas: `cli → api → store/runtime/core`; nada en `api` importa `cli`

### HTTP (`sldb serve`)

`/document/ir`, `/save` (con `expected` → **409** en conflicto), `/edges/node`,
`/graph/*`, `/find`, `/models/detail`.

### Primitivos sueltos

```python
from sldb import AST_Handler, TemplateExtractor, DataExtractor, SLDBRenderer
```

Round-trip puro, sin store. Es lo que usan `render` / `extract` / `validate`.

---

## 11. Los cinco niveles de extender

| Nivel | Qué hacés | Requiere |
|---|---|---|
| 1 | Definir modelos | heredar de `StructuredNLDoc` |
| 2 | Declarar vocabulario: relaciones, predicados, DAG de tags | **escribir documentos** |
| 3 | Declarar consumo: `IndexProjection` | Python simple |
| 4 | Adaptadores de fuente (como `selfdoc`) | Python |
| 5 | Handlers de render (`list`, `table`, `yaml`, `python_expr`) | tocar el motor |

**La regla que se repite en todos: extendés declarando, no escribiendo
procedimientos.**

---

## 12. Ciclo de vida del contrato

Cambiar un modelo no es editar el `.py` y listo:

```
draft → validate → promote → stores update
```

```bash
python -m sldb models template edit <Modelo> --input tpl.md --store .sldb --pythonpath .
python -m sldb models fields add <Modelo> <campo> --type str --description "..." \
  --store .sldb --pythonpath .
python -m sldb models validate <Modelo> --store .sldb --pythonpath .
python -m sldb models validate <Modelo> --promote --store .sldb --pythonpath .
python -m sldb stores update --store .sldb --pythonpath .
```

(Si tenés el binario instalado, `sldb ...` es equivalente a `python -m sldb ...`.)

Porque cambiar el contrato cambia **las tres caras a la vez**, y hay documentos
existentes que tienen que seguir cumpliéndolo.

---

## 13. Fricciones operativas

Cosas que cuestan tiempo la primera vez:

- **`--store` quiere la ruta a `.sldb`**, no el directorio que lo contiene
- **`edges rebuild` dice `0 shard(s) written` cuando ya está todo hecho.** Es
  caché, no falla: revisá `.sldb_cache/edges/`.

---

## 14. Límites conocidos

- **Sin id estable de sección.** Se direccionan por slug jerárquico; headings
  repetidos se desambiguan por orden de aparición. Mover una sección cambia su
  dirección.
- **Composición de una sola vía.** Sin edit-through, sin composición por query.
  Lo que sí hay es la arista: `__compositions__` aporta `composes` (§6), así que el
  radio de impacto sí recorre la recursión, aunque escribir sobre la salida
  compuesta siga sin propagarse al hijo.
- **`Corpus` sí se exporta en `sldb.api`**, con `rank_fields()` para rankear
  campos. Lo que sigue sin cliente de CLI es el ranking: ni `rank()` (documento)
  ni `rank_fields()` (campo) tienen comando. Se integran por Python.
- **El índice de embeddings tiene dos granularidades.** La de documento
  (`Corpus.index`, clave = documento + su `content_hash`) y la de campo
  (`Corpus.field_index`, clave = `docs/<Modelo>/<doc>/<campo>` + el hash de ese
  field). La de campo vive en su propio archivo derivado
  (`fields.<text_id>.<embedder>.json`), nunca comparte con `docs.*`. Un field de
  un documento de cuarenta se re-embebe solo: medido `embedded=1, reused=3`.
  `api/matching/document_index.py` no cambió — ya keyeaba por hash.
- **Las secciones no tienen hash propio.** `DocSections` se estampa con el
  `source_hash` del documento padre: es clave de caché, no un nivel del Merkle.
  Si el documento cambia, todas sus secciones se reprocesan.

---

## 15. Anti-patterns

- **No edites a mano un documento trackeado.** Usá `fields` o la API.
- **No reimplementes composición, resolución de referencias, round-trip ni
  índice inverso.** SLDB ya los tiene.
- **No compares ids como strings.** Preguntale al grafo.
- **No infieras el contrato leyendo los artefactos de salida.** Leé el modelo.
- **No inventes jerarquía entre las tres caras.** Si divergen, es un bug con
  diagnóstico, no una decisión de diseño.
- **Si falta algo, registrá el gap** en vez de hacer un workaround local.

---

## 16. Verificacion de este manual

Todo el contenido fue ejecutado contra stores reales antes de escribirse, y
despues auditado por tres revisores independientes que re-verificaron cada
afirmacion contra `src/sldb/`.

Correcciones que salieron de esa auditoria:

| Seccion | Estaba mal | Ahora |
|---|---|---|
| 3 | "optrev borra la linea si queda vacio" | solo con `None` y en dos formas concretas |
| 4 | `runtime/cache/` en el arbol | no existe: los caches viven en `$XDG_CACHE_HOME/sldb` |
| 4 | `core/models/` = "documentos del modelo" | es el nodo del modelo: hashes y conteo |
| 5 | salida de `stores check` cortada en varias lineas | una linea por campo, con `(see 'fix:' above)` |
| 6 | tabla de 8 comandos de graph | son 12: faltaban `get`, `list`, `query`, `ingest-sldb` |
| 6 | "`__containment__`/`__references__` se exponen por /schema y fields_routes" | `fields_routes` solo expone `__references__` |
| 6, 14 | "`__containment__`/`__references__` no generan aristas" | sí las generan (`references`/`contains`, `origin: "schema"`): cuarta fuente del grafo |
| 6, 14 | "`__compositions__` no llega al grafo" | ya llega: aporta `composes`, con el target resuelto de ruta a documento al componer el índice |
| 13 | "resuelve por el `path` absoluto" | el path suele ser relativo y se re-ancla al project root |
| 14 | "`Corpus.rank()` no esta en el CLI" | y no se exportaba en `sldb.api`. Ya se exporta, con `rank_fields()`; lo que falta es el comando de CLI, no el cliente |
| 14 | "el indice de embeddings es por documento, no por campo" | tiene dos granularidades: `index` (documento) y `field_index` (`docs/<Modelo>/<doc>/<campo>`, con el hash del field) |
| 4 | los 4 hashes como si `model_hash` fuera hoja | `model_hash` se compone de `contract_hash` + `roster_hash`, guardados por separado |
| 4 | nada sobre granularidad por campo | `field_hashes` por documento, y que un mapa vacio es "no se pudo calcular" |
| 13 | ninguna friccion de performance | los dos re-parseos evitables de `validation.py` y `section_rebuild.py` |
| 13 | `models template show` fallaba si el `path` guardado no era un archivo aquí | busca el fuente importando el `model_ref`, y si tampoco importa nombra el modelo y el store |
| 13 | `ast show` con warnings antes del JSON; `--format json` rechazado por `models show`, `models template show` y `docs update`; `edges show` con un nombre de documento devolvía `[]`; los dos re-parseos | resueltos (2026-10-18): stdout limpio, `--format` en los tres (y un flag desconocido muestra el uso del subcomando), `edges show` rechaza lo que no es un nodo y sugiere el export id, template memoizado y un solo `MarkdownIt` |
| 14 | nada sobre los limites de indexacion | el indice de embeddings tiene granularidad de documento y de campo; las secciones no tienen hash propio |

Verificado en vivo y sin cambios: los 4 hashes y sus alias, `Field(description)`
obligatorio, `render` no se extrae, los 11 relation types builtin, los campos de
`RelationTypeDoc`, `{Modelo+}` recorriendo el MRO sin registrar la base, la cita
de `text_id`, los limites de composicion, los 6 endpoints HTTP, `/save`
devolviendo 409 real ante `expected` distinto, y las 5 fricciones de la seccion
13.

FILE:tests/store/test_predicate_language.py
"""GO05: the unified predicate language against the two old ones (rules-language.md §7).

`PAYLOADS` is the fixed set of payloads (p5): null, lists, an absent field, numbers and
strings. `tests/fixtures/where_goldens/` holds, for each row of the equivalence table, the old
expression (a `where_parse` string, or a `FieldCondition` as its JSON dict, p13) and the
sorted names of the payloads it matched, captured with the code of main before GO05 touched
`src/`. The goldens are never regenerated: `_capture` documents how they were taken. An old
evaluator that raised on a payload (where_parse ordering `None` or mixed types raises
TypeError) counted as "does not match".
"""

from __future__ import annotations

import json
from pathlib import Path
from types import SimpleNamespace

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


def _old_where(expression: str):
    from sldb.store.query_engine.where_parse import compile_where

    predicate = compile_where(expression)
    return lambda payload: predicate(SimpleNamespace(payload=payload, name="", model_type=None), None, None)


def _old_field_condition(row: dict):
    from sldb.store.graph.language import FieldCondition
    from sldb.store.graph.payload_match import payload_condition

    condition = FieldCondition(**row)
    return lambda payload: payload_condition(payload, condition)


def _capture() -> dict[str, list[dict]]:
    """How the goldens were taken, with main's code before GO05 changed `src/` (commit 4d090ee2)."""
    where = [{"old": old, "matches": _matching(_old_where(old))} for _, old in WHERE_ROWS]
    conditions = [{"old": old, "matches": _matching(_old_field_condition(old))} for _, old, _ in FIELD_CONDITION_ROWS]
    return {"where_parse": where, "field_condition": conditions}


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
        new = _matching(lambda payload: where_matches(old, payload))
        assert _changed(new, golden["matches"]) == WHERE_DIFFERENCES.get(old, set()), (row, old)


def test_field_condition_rows_translate_to_the_table_and_answer_their_goldens():
    from sldb.store.graph.language.predicate_documents import payload_holds

    for (row, old, construction), golden in zip(FIELD_CONDITION_ROWS, _golden("field_condition")):
        assert _old_field_condition_predicate(old) == construction, row
        through_the_shim = _matching(_old_field_condition(old))
        through_the_language = _matching(lambda p: payload_holds(construction, {k: v for k, v in p.items() if v is not None}))
        assert through_the_shim == through_the_language, row
        assert _changed(through_the_shim, golden["matches"]) == FIELD_CONDITION_DIFFERENCES.get(row, set()), row


def _old_field_condition_predicate(row: dict) -> str:
    import warnings

    from sldb.store.graph.language import FieldCondition

    with warnings.catch_warnings():
        warnings.simplefilter("ignore", DeprecationWarning)
        return FieldCondition(**row).predicate().text


# --- the shims warn; the new API does not (GO05 aceptación) ------------------------------

def test_calling_where_parse_and_compile_where_warns():
    import pytest

    from sldb.store.query_engine.where_parse import compile_where, where_parse

    with pytest.warns(DeprecationWarning, match="compile_where is deprecated"):
        assert compile_where("has(status)")(SimpleNamespace(payload={"status": "x"}, name="d", model_type=None))
    with pytest.warns(DeprecationWarning, match="where_parse is deprecated"):
        assert where_parse('status = "x"').text == 'status = "x"'


def test_constructing_a_field_condition_warns_naming_the_predicate():
    import pytest

    from sldb.store.graph.language import FieldCondition

    with pytest.warns(DeprecationWarning, match='write the predicate `status = "open"`'):
        FieldCondition(field="status", op="eq", value="open")


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


# --- the CLI: find --where (paths, --explain), graph query's warning, zero extractions ----

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


def test_graph_query_with_field_condition_dicts_warns_in_the_envelope(tasks, tmp_path):
    sp, py = tasks
    query = tmp_path / "query.json"
    query.write_text(json.dumps({"filters": [{"facet": "payload", "conditions": [{"field": "status", "op": "eq", "value": "closed"}]}]}), encoding="utf-8")
    plain_code, plain = _cli("graph", "query", "--query-file", str(query), "--store", str(sp), "--local")
    code, printed = _cli("--envelope", "graph", "query", "--query-file", str(query), "--store", str(sp), "--local")
    envelope = json.loads(printed)
    assert plain_code == code == 0 and envelope["data"] == json.loads(plain)
    assert [n["id"] for n in envelope["data"]] == ["sldb://document/Task:b"]
    warning = envelope["warnings"]
    assert [(w["level"], w["code"], w["subject"]) for w in warning] == [("warning", "deprecated/field-condition", "graph query")]
    assert 'status = "closed"' in warning[0]["what"]


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

FILE:instruccion
Cold-bundle de la tarea task-go10-retiro-de-where-parse-y-fieldcondition: con el TaskDoc, los rituales enrutados por el Board, las pills ligadas, los átomos ligados y los archivos que el TaskDoc nombra, reformula el encargo, lista ambigüedades con cita textual del input y da el DRY-RUN sin ejecutar nada. No ejecutes nada.

Sección de validación del TaskDoc:
- grep -rn 'where_parse\|FieldCondition' src/ docs/ sin resultados fuera de la tabla historica de rules-language.md (bajo Historico)
- grep -rw de eq, ne, gt, lt, contains, starts_with, is_null, is_not_null en bloques de codigo de docs/*.md sin resultados fuera de esa tabla (tests/store/test_where_retired.py)
- StructuredQuery con conditions rechazado con ValidationError (test de rechazo); tests/store/test_example_queries.py devuelve los mismos ids con los JSON reescritos
- goldens de equivalencia verdes como tests del lenguaje nuevo
- TMPDIR=/dev/shm pytest tests/test_clean_code_rules.py tests/test_store_seams.py en verde y tools/check_layers.py PASS
- suite completa verde (una vez, al final del nodo, la corre el supervisor)
- CHANGELOG registra el retiro en la seccion en curso

