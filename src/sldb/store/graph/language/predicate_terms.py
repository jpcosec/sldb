"""Term operations: `a in b`, `f ~ "re"`, `a cmp b`, and the terms they read.

A term is a field, a string or number literal, a list of literals, or `{field}` (a value of
the subject, rules-language.md §2). An invalid regular expression is rejected here, at parse
time, as `WherePredicateError`.
"""

from __future__ import annotations

import re

from sldb.store.graph.language.predicate_cursor import expect_ident, expect_op, fail, is_op, keyword, peek, span, take

COMPARISONS = ("=", "!=", "<", "<=", ">", ">=")


def operation(cur: list) -> tuple:
    """A term followed by `in`, `~` or a comparison."""
    start = peek(cur).start
    left = term(cur)
    if keyword(cur, "in") and take(cur):
        kind, args = "in", (left, term(cur))
    elif is_op(cur, "~") and take(cur):
        kind, args = "regex", (left, _pattern(cur))
    else:
        kind, args = "cmp", (left, comparison_operator(cur), term(cur))
    return ("leaf", span(cur, start), kind, args)


def comparison_operator(cur: list) -> str:
    """One of `= != < <= > >=`, consumed."""
    token = peek(cur)
    if token.kind != "op" or token.value not in COMPARISONS:
        fail(cur)
    return take(cur).value


def term(cur: list) -> tuple:
    """A field, a literal, a literal list, or `{field}`."""
    token = take(cur)
    if token.kind in ("literal", "number"):
        return ("literal", token.value)
    if token.kind == "ident":
        return ("field", token.value)
    if token.kind == "op" and token.value == "[":
        return ("literal", _list(cur))
    if token.kind == "op" and token.value == "{":
        return _substitution(cur)
    fail(cur)


def _substitution(cur: list) -> tuple:
    """`{field}`, the `{` already consumed."""
    name = expect_ident(cur).value
    expect_op(cur, "}")
    return ("subst", name)


def _list(cur: list) -> list:
    """Scalar literals between brackets, comma-separated; the `[` is already consumed."""
    values: list = []
    while not is_op(cur, "]"):
        if values:
            expect_op(cur, ",")
        token = take(cur)
        if token.kind not in ("literal", "number"):
            fail(cur)
        values.append(token.value)
    take(cur)
    return values


def _pattern(cur: list):
    """The compiled right-hand side of `~`: a string literal that is a valid regex."""
    token = take(cur)
    if token.kind != "literal":
        fail(cur)
    try:
        return re.compile(token.value)
    except re.error:
        fail(cur)
