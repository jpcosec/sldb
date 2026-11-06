"""Atoms with syntax of their own: `has`, `nonempty`, `model <=`, the quantifiers and `count`.

Anything else is a term operation (`in`, `~`, a comparison; `predicate_terms`).
"""

from __future__ import annotations

from sldb.store.graph.language.predicate_cursor import expect_ident, expect_op, is_op, keyword, peek, span, take
from sldb.store.graph.language.predicate_paths import parse_path
from sldb.store.graph.language.predicate_terms import comparison_operator, operation, term

_QUANTIFIERS = ("any", "all", "none")


def atom(cur: list) -> tuple:
    """One atom at the cursor."""
    token = peek(cur)
    if token.kind == "ident" and is_op(cur, "(", 1):
        handler = _CALLS.get(token.value)
        if handler is not None:
            return handler(cur)
    if keyword(cur, "model") and is_op(cur, "<=", 1):
        return _model(cur)
    return operation(cur)


def _field_call(cur: list) -> tuple:
    """`has(field)` or `nonempty(field)`."""
    start, kind = peek(cur).start, take(cur).value
    expect_op(cur, "(")
    field = expect_ident(cur).value
    expect_op(cur, ")")
    return ("leaf", span(cur, start), kind, (field,))


def _model(cur: list) -> tuple:
    """`model <= Base`."""
    start = take(cur).start
    expect_op(cur, "<=")
    base = expect_ident(cur).value
    return ("leaf", span(cur, start), "model", (base,))


def _quantifier(cur: list) -> tuple:
    """`any(path: p)`, `all(path: p)`, `none(path: p)`."""
    start, kind = peek(cur).start, take(cur).value
    path, body = _path_and_body(cur)
    return ("quant", span(cur, start), kind, path, body)


def _count(cur: list) -> tuple:
    """`count(path: p) cmp term`: a count only appears as one side of a comparison."""
    start = take(cur).start
    path, body = _path_and_body(cur)
    op = comparison_operator(cur)
    right = term(cur)
    return ("count", span(cur, start), path, body, op, right)


def _path_and_body(cur: list) -> tuple:
    expect_op(cur, "(")
    path = parse_path(cur)
    expect_op(cur, ":")
    body = cur[3](cur)
    expect_op(cur, ")")
    return path, body


_CALLS = {"has": _field_call, "nonempty": _field_call, "count": _count, **{q: _quantifier for q in _QUANTIFIERS}}
