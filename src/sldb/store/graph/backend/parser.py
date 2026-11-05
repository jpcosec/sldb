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
