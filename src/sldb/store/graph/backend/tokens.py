"""Tokens of the GO02 predicate subset: literals, numbers, fields, keywords and operators."""

from __future__ import annotations

import re
from collections import namedtuple
from typing import Any

from sldb.store.query_engine.where_literal import unquote
from sldb.store.query_engine.where_parse import WherePredicateError

_TOKEN = re.compile(
    r"""\s*(?:
        (?P<literal>"(?:[^"\\]|\\.)*")
      | (?P<number>-?\d+(?:\.\d+)?)
      | (?P<ident>[A-Za-z_][\w.]*)
      | (?P<op>!=|<=|>=|[=<>~()\[\],{}:^+])
    )""",
    re.VERBOSE,
)
_Token = namedtuple("_Token", "kind value raw start end")


def tokenize(text: str, expression: str) -> list:
    """Every token of `text`, with its source offsets, ended by an `eof` token."""
    tokens: list = []
    position = 0
    while (token := _next_token(text, position, expression)) is not None:
        tokens.append(token)
        position = token.end
    tokens.append(_Token("eof", "", "", len(text), len(text)))
    return tokens


def _next_token(text: str, position: int, expression: str) -> Any:
    position = _skip_space(text, position)
    if position >= len(text):
        return None
    match = _TOKEN.match(text, position)
    if match is None or match.end() == position:
        raise WherePredicateError(expression)
    kind = match.lastgroup or ""
    raw = match.group(kind)
    return _Token(kind, _token_value(kind, raw), raw, match.start(kind), match.end(kind))


def _skip_space(text: str, position: int) -> int:
    while position < len(text) and text[position].isspace():
        position += 1
    return position


def _token_value(kind: str, raw: str) -> Any:
    if kind == "literal":
        return unquote(raw)
    if kind == "number":
        return int(raw) if re.fullmatch(r"-?\d+", raw) else float(raw)
    return raw
