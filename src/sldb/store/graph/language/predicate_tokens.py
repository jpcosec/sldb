"""Tokens of the predicate language: literals, numbers, names, keywords and operators.

A name may carry dots (`sldb.authority`, `tasks.0.title`): a field path for a leaf, or steps
joined by `.` inside a quantifier's path (rules-language.md §8, H5 and H9).
"""

from __future__ import annotations

import re
from collections import namedtuple
from typing import Any

from sldb.store.query_engine.where_literal import unquote
from sldb.store.exceptions import WherePredicateError

_TOKEN = re.compile(
    r"""(?:
        (?P<literal>"(?:[^"\\]|\\.)*")
      | (?P<number>-?\d+(?:\.\d+)?)
      | (?P<ident>[A-Za-z_][\w.]*)
      | (?P<op>!=|<=|>=|[=<>~()\[\],{}:^+.])
    )""",
    re.VERBOSE,
)
Token = namedtuple("Token", "kind value raw start end")


def tokenize(text: str) -> list:
    """Every token of `text` with its source offsets, ended by an `eof` token."""
    tokens: list = []
    position = _skip_space(text, 0)
    while position < len(text):
        tokens.append(_token_at(text, position))
        position = _skip_space(text, tokens[-1].end)
    tokens.append(Token("eof", "", "", len(text), len(text)))
    return tokens


def _token_at(text: str, position: int) -> Any:
    match = _TOKEN.match(text, position)
    if match is None or match.end() == position:
        raise WherePredicateError(text)
    kind = match.lastgroup or ""
    raw = match.group(kind)
    return Token(kind, _value(kind, raw), raw, match.start(kind), match.end(kind))


def _skip_space(text: str, position: int) -> int:
    while position < len(text) and text[position].isspace():
        position += 1
    return position


def _value(kind: str, raw: str) -> Any:
    if kind == "literal":
        return unquote(raw)
    if kind == "number":
        return int(raw) if re.fullmatch(r"-?\d+", raw) else float(raw)
    return raw
