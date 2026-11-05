"""The leaves of the GO02 subset: their checks, and how a term is read from a payload."""

from __future__ import annotations

import operator
import re
from typing import Any, Callable

from sldb.store.query_engine.where_lookup import _ABSENT, _lookup
from sldb.store.query_engine.where_parse import WherePredicateError

_COMPARE = {"=": operator.eq, "!=": operator.ne, "<": operator.lt, "<=": operator.le, ">": operator.gt, ">=": operator.ge}
_EMPTY = (str, list, dict, tuple, set)


def resolve(term: tuple, payload: dict[str, Any]) -> tuple[Any, dict[str, Any]]:
    """A term's value and the `seen` leaf; a field is read by dotted path."""
    if term[0] != "field":
        return term[1], {}
    value = _lookup(payload, term[1], _ABSENT)
    return value, {term[1]: None if value is _ABSENT else value}


def has_check(field: str) -> Callable[[dict[str, Any]], tuple[bool, dict[str, Any]]]:
    """`has(f)`: present and neither `None` nor the empty string."""
    def check(payload: dict[str, Any]) -> tuple[bool, dict[str, Any]]:
        value = _lookup(payload, field, _ABSENT)
        holds = value is not _ABSENT and value is not None and value != ""
        return holds, {field: None if value is _ABSENT else value}
    return check


def nonempty_check(field: str) -> Callable[[dict[str, Any]], tuple[bool, dict[str, Any]]]:
    """`nonempty(f)`: present and a collection with at least one element."""
    def check(payload: dict[str, Any]) -> tuple[bool, dict[str, Any]]:
        value = _lookup(payload, field, _ABSENT)
        empty = isinstance(value, _EMPTY) and len(value) == 0
        return (value is not _ABSENT and value is not None and not empty), _seen(field, value)
    return check


def model_check(base: str) -> Callable[[dict[str, Any]], tuple[bool, dict[str, Any]]]:
    """`model <= X`: the payload's model is X or names X among its base models."""
    def check(payload: dict[str, Any]) -> tuple[bool, dict[str, Any]]:
        model = payload.get("model")
        bases = payload.get("base_models") or ()
        return (isinstance(model, str) and (model == base or base in bases)), {"model": model}
    return check


def membership_check(left: tuple, right: tuple) -> Callable[[dict[str, Any]], tuple[bool, dict[str, Any]]]:
    """`a in b`: list membership or substring, false for any other right-hand type."""
    return lambda payload: _membership_terms(left, right, payload)


def regex_check(left: tuple, right: tuple, expression: str) -> Callable[[dict[str, Any]], tuple[bool, dict[str, Any]]]:
    """`f ~ "pattern"`, with `re.search` and an invalid pattern rejected at parse time."""
    pattern = _compiled(right, expression)
    return lambda payload: _regex_terms(pattern, left, payload)


def comparison_check(left: tuple, op: str, right: tuple) -> Callable[[dict[str, Any]], tuple[bool, dict[str, Any]]]:
    """`a cmp b` on present values; a missing field or mixed types does not hold."""
    return lambda payload: _comparison_terms(left, op, right, payload)


def compare(left: Any, op: str, right: Any) -> bool:
    """Apply one comparison operator."""
    return _COMPARE[op](left, right)


def _seen(field: str, value: Any) -> dict[str, Any]:
    return {field: None if value is _ABSENT else value}


def _membership_terms(left: tuple, right: tuple, payload: dict[str, Any]) -> tuple[bool, dict[str, Any]]:
    left_value, left_seen = resolve(left, payload)
    right_value, right_seen = resolve(right, payload)
    seen = {**left_seen, **right_seen}
    if left_value is _ABSENT or right_value is _ABSENT:
        return False, seen
    return (left_value in right_value if isinstance(right_value, (list, str)) else False), seen


def _compiled(right: tuple, expression: str):
    if right[0] != "literal" or not isinstance(right[1], str):
        raise WherePredicateError(expression)
    try:
        return re.compile(right[1])
    except re.error as invalid:
        raise WherePredicateError(expression) from invalid


def _regex_terms(pattern, left: tuple, payload: dict[str, Any]) -> tuple[bool, dict[str, Any]]:
    value, seen = resolve(left, payload)
    if value is _ABSENT or value is None:
        return False, seen
    return pattern.search(str(value)) is not None, seen


def _comparison_terms(left: tuple, op: str, right: tuple, payload: dict[str, Any]) -> tuple[bool, dict[str, Any]]:
    left_value, left_seen = resolve(left, payload)
    right_value, right_seen = resolve(right, payload)
    seen = {**left_seen, **right_seen}
    if left_value is _ABSENT or right_value is _ABSENT:
        return False, seen
    try:
        return compare(left_value, op, right_value), seen
    except TypeError:
        return False, seen
