"""One grammar for sldb's `--where` predicates: parsed once per query, matched per document.

`compile_where` raises `WherePredicateError` when no evaluator understands the predicate,
so an unparseable expression is a loud error instead of a silent empty result.
"""

from __future__ import annotations

import re
from typing import Any, Callable

from sldb.core.exceptions import SLDBError

Predicate = Callable[[Any, Any, Any], bool]  # (doc, resolve_model_ref, pythonpath) -> bool


class WherePredicateError(ValueError, SLDBError):
    """A --where predicate that no evaluator can parse."""

    def __init__(self, expression: str):
        super().__init__(f"no evaluator understands the predicate: {expression!r}")


def compile_where(expression: str) -> Predicate:
    """Parses one --where predicate; raises WherePredicateError if no evaluator does."""
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


# A string literal: '"', then non-quote/non-backslash chars or a backslash escaping
# any char, then '"'. The value unquotes \" -> " and \\ -> \.
_LITERAL = r'"(?:[^"\\]|\\.)*"'
_LITERAL_NONEMPTY = r'("(?:[^"\\]|\\.)+")'


def _unquote(raw: str) -> str:
    """The literal's value: the quotes off, the two escapes resolved; any other
    backslash survives verbatim."""
    body, out, i = raw[1:-1], [], 0
    while i < len(body):
        if body[i] == "\\" and i + 1 < len(body) and body[i + 1] in ('"', "\\"):
            out.append(body[i + 1])
            i += 2
        else:
            out.append(body[i])
            i += 1
    return "".join(out)


# same order the old evaluator tried them: has, in, regex, model family, comparison
_EVALUATORS = [
    (re.compile(r"has\(([^)]+)\)"), _build_has),
    (re.compile(_LITERAL_NONEMPTY + r"\s+in\s+([A-Za-z_][\w]*)"), _build_contains),
    (re.compile(r'([A-Za-z_][\w]*)\s*~\s*' + _LITERAL_NONEMPTY), _build_regex),
    (re.compile(r"model\s*<=\s*([A-Za-z_][\w]*)"), _build_model),
    (
        re.compile(r'([A-Za-z_][\w]*)\s*(=|!=|>=|<=)\s*(' + _LITERAL + r'|\d+(?:\.\d+)?)'),
        _build_compare,
    ),
]
