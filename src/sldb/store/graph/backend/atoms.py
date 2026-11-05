"""Atoms that are syntax of their own: `has`, `nonempty`, `model <=`, and the path reject."""

from __future__ import annotations

from sldb.store.graph.backend.checks import has_check, model_check, nonempty_check
from sldb.store.graph.backend.operations import _operation
from sldb.store.graph.backend.state import expect_ident, expect_op, peek, previous, take


def atom(state: list, text: str, expression: str):
    """One atom; anything else is a term operation in `operations`."""
    token = peek(state)
    if token.kind == "ident":
        handler = _SPECIAL.get(token.value)
        if handler is not None and peek(state, 1).value == "(":
            return handler(state, text, expression)
        if token.value == "model" and peek(state, 1).value == "<=":
            return model_leaf(state, text, expression)
    return _operation(state, text, expression)


def has_leaf(state: list, text: str, expression: str):
    """`has(field)`."""
    start = take(state).start
    expect_op(state, "(", expression)
    field = expect_ident(state, expression).value
    end = expect_op(state, ")", expression).end
    return _leaf(text, start, end, has_check(field))


def nonempty_leaf(state: list, text: str, expression: str):
    """`nonempty(field)`."""
    start = take(state).start
    expect_op(state, "(", expression)
    field = expect_ident(state, expression).value
    end = expect_op(state, ")", expression).end
    return _leaf(text, start, end, nonempty_check(field))


def model_leaf(state: list, text: str, expression: str):
    """`model <= BaseDoc`."""
    start = take(state).start
    expect_op(state, "<=", expression)
    base = expect_ident(state, expression).value
    return _leaf(text, start, previous(state).end, model_check(base))


def reject_path(state: list, text: str, expression: str):
    """A quantifier is a path: GO05, not GO03."""
    name = take(state).value
    raise NotImplementedError(f"los caminos no están implementados en GO03: {name}(...)")


def _leaf(text: str, start: int, end: int, check):
    return ("leaf", start, end, text[start:end].strip(), check)


_SPECIAL = {
    "has": has_leaf,
    "nonempty": nonempty_leaf,
    "any": reject_path,
    "all": reject_path,
    "none": reject_path,
    "count": reject_path,
}
