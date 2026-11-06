"""The predicate grammar of rules-language.md §1: `or` over `and` over `not` over atoms.

`not` binds tighter than `and`, and `and` tighter than `or`; both binaries associate to the
left and parentheses group. Whatever does not parse is `WherePredicateError` naming the whole
expression, the error `--where` has always raised.
"""

from __future__ import annotations

from functools import lru_cache

from sldb.store.graph.language.predicate_ast import Predicate
from sldb.store.graph.language.predicate_atoms import atom
from sldb.store.graph.language.predicate_cursor import cursor, expect_op, fail, is_op, keyword, peek, span, take
from sldb.store.graph.language.predicate_tokens import tokenize


@lru_cache(maxsize=512)
def parse_predicate(text: str) -> Predicate:
    """Parse one predicate; the whole text must be consumed."""
    cur = cursor(tokenize(text), text, expression)
    root = expression(cur)
    if peek(cur).kind != "eof":
        fail(cur)
    return Predicate(text, root)


def expression(cur: list) -> tuple:
    """`and` joined by `or`, left-associative."""
    return _chain(cur, "or", _conjunction)


def _conjunction(cur: list) -> tuple:
    """`not` joined by `and`, left-associative."""
    return _chain(cur, "and", _negation)


def _chain(cur: list, word: str, operand) -> tuple:
    start = peek(cur).start
    node = operand(cur)
    while keyword(cur, word):
        take(cur)
        right = operand(cur)
        node = (word, span(cur, start), node, right)
    return node


def _negation(cur: list) -> tuple:
    """`not` binds tighter than `and`."""
    if not keyword(cur, "not"):
        return _primary(cur)
    start = take(cur).start
    child = _negation(cur)
    return ("not", span(cur, start), child)


def _primary(cur: list) -> tuple:
    if not is_op(cur, "("):
        return atom(cur)
    take(cur)
    node = expression(cur)
    expect_op(cur, ")")
    return node
