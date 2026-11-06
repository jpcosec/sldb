"""The cursor a recursive-descent parse carries: tokens, position, source text, and the
expression parser itself (so atoms can parse a quantifier's body without a circular import).
"""

from __future__ import annotations

from typing import Any, Callable

from sldb.store.exceptions import WherePredicateError


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
