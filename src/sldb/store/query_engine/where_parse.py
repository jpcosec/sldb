"""One grammar for sldb's `--where` predicates: parsed once per query, matched per document.

`compile_where` raises `WherePredicateError` when no evaluator understands the predicate,
so an unparseable expression is a loud error instead of a silent empty result. Predicates
join with ` and ` (outside literals); there is no `or` and no parentheses.
"""

from __future__ import annotations

import re
from typing import Any, Callable

from sldb.core.exceptions import SLDBError
from sldb.store.query_engine.where_literal import LITERAL as _LITERAL
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
        value = doc.payload.get(field)
        return value is not None and not (isinstance(value, (str, list, dict, tuple, set)) and len(value) == 0)

    return check


def _build_contains(m: re.Match) -> Predicate:
    needle, field = _unquote(m.group(1)), m.group(2)

    def check(doc: Any, resolve_model_ref: Any, pythonpath: Any) -> bool:
        value = doc.payload.get(field)
        return needle in value if isinstance(value, (list, str)) else False

    return check


def _build_regex(m: re.Match) -> Predicate:
    field, pattern = m.group(1), _unquote(m.group(2))

    def check(doc: Any, resolve_model_ref: Any, pythonpath: Any) -> bool:
        target = doc.name if field == "doc" else str(doc.payload.get(field, ""))
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
        if raw.startswith('"') and field not in doc.payload:
            return False  # an absent field matches neither "=" nor "!=" (string literals)
        return _apply_op(doc.payload.get(field), op, expected)

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
    (re.compile(_LITERAL_NONEMPTY + r"\s+in\s+([A-Za-z_][\w]*)"), _build_contains),
    (re.compile(r'([A-Za-z_][\w]*)\s*~\s*' + _LITERAL_NONEMPTY), _build_regex),
    (re.compile(r"model\s*<=\s*([A-Za-z_][\w]*)"), _build_model),
    (
        re.compile(r'([A-Za-z_][\w]*)\s*(=|!=|>=|<=)\s*(' + _LITERAL + r'|-?\d+(?:\.\d+)?)'),
        _build_compare,
    ),
]
