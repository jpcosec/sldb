"""The cursor a recursive-descent parse carries: the token list and the current position."""

from __future__ import annotations

from sldb.store.query_engine.where_parse import WherePredicateError


def peek(state: list, offset: int = 0):
    """The token at the cursor plus `offset`, clamped to the final `eof` token."""
    tokens, position = state
    return tokens[min(position + offset, len(tokens) - 1)]


def take(state: list):
    """Consume and return the token at the cursor."""
    token = peek(state)
    state[1] += 1
    return token


def previous(state: list):
    """The last consumed token."""
    return state[0][max(state[1] - 1, 0)]


def ident(state: list, name: str) -> bool:
    """Whether the token at the cursor is exactly this keyword."""
    token = peek(state)
    return token.kind == "ident" and token.value == name


def is_op(state: list, value: str) -> bool:
    """Whether the token at the cursor is exactly this operator."""
    token = peek(state)
    return token.kind == "op" and token.value == value


def expect_op(state: list, value: str, expression: str):
    """Consume this operator, or report the predicate as unparseable."""
    token = take(state)
    if token.kind != "op" or token.value != value:
        raise WherePredicateError(expression)
    return token


def expect_ident(state: list, expression: str):
    """Consume an identifier, or report the predicate as unparseable."""
    token = take(state)
    if token.kind != "ident":
        raise WherePredicateError(expression)
    return token
