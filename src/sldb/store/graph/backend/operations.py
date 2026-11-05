"""Term operations: `in`, `~`, comparisons, and the terms and literal lists they compare."""

from __future__ import annotations

from sldb.store.graph.backend.checks import comparison_check, membership_check, regex_check
from sldb.store.graph.backend.state import expect_op, ident, is_op, peek, previous, take
from sldb.store.query_engine.where_parse import WherePredicateError

_COMPARISONS = ("=", "!=", "<", "<=", ">", ">=")
_PATH_OPS = (":", "^", "+")


def _operation(state: list, text: str, expression: str):
    """A term followed by `in`, `~` or a comparison."""
    start = peek(state).start
    left = _term(state, text, expression)
    _reject_path_suffix(state)
    for handler in (_membership_op, _regex_op, _comparison_op):
        node = handler(state, text, expression, start, left)
        if node is not None:
            return node
    raise WherePredicateError(expression)


def _membership_op(state: list, text: str, expression: str, start: int, left: tuple):
    if not ident(state, "in"):
        return None
    take(state)
    right = _term(state, text, expression)
    return _leaf(text, start, previous(state).end, membership_check(left, right))


def _regex_op(state: list, text: str, expression: str, start: int, left: tuple):
    if not is_op(state, "~"):
        return None
    take(state)
    right = _term(state, text, expression)
    return _leaf(text, start, previous(state).end, regex_check(left, right, expression))


def _comparison_op(state: list, text: str, expression: str, start: int, left: tuple):
    operator = peek(state).value
    if peek(state).kind != "op" or operator not in _COMPARISONS:
        return None
    take(state)
    right = _term(state, text, expression)
    return _leaf(text, start, previous(state).end, comparison_check(left, operator, right))


def _term(state: list, text: str, expression: str) -> tuple:
    """A field, a string/number literal, or a literal list."""
    token = take(state)
    if token.kind in ("literal", "number"):
        return ("literal", token.value)
    if token.kind == "ident":
        return ("field", token.value)
    if token.kind == "op" and token.value == "[":
        return ("literal", _list(state, expression))
    if token.kind == "op" and token.value in _PATH_OPS:
        raise NotImplementedError("los caminos no están implementados en GO03")
    raise WherePredicateError(expression)


def _list(state: list, expression: str) -> list:
    """A list of scalar literals between brackets."""
    values: list = []
    if is_op(state, "]"):
        take(state)
        return values
    while True:
        values.append(_literal_value(take(state), expression))
        if not _more(state):
            break
    expect_op(state, "]", expression)
    return values


def _more(state: list) -> bool:
    if not is_op(state, ","):
        return False
    take(state)
    return True


def _literal_value(token, expression: str):
    if token.kind in ("literal", "number"):
        return token.value
    raise WherePredicateError(expression)


def _reject_path_suffix(state: list) -> None:
    token = peek(state)
    if token.kind == "op" and token.value in _PATH_OPS:
        raise NotImplementedError("los caminos no están implementados en GO03")


def _leaf(text: str, start: int, end: int, check):
    return ("leaf", start, end, text[start:end].strip(), check)
