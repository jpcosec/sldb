"""Names and extents over Postgres' tokens (pglast's scanner) of one statement.

A token gives its first and last character (inclusive) in the statement's text, and a quoted
identifier is a single token, so `"a,b"`, `"a)b"` or `"a""b"` never split a list. Names are read as
written and unquoted with `sql_names.unquote` (`"a""b"` is `a"b`; an unquoted `Users` stays `Users`,
the spelling tree-sitter gives the facts), never case-folded.
"""

from __future__ import annotations

from typing import Any

from sldb.code.sql_names import unquote

_OPEN, _CLOSE, _COMMA, _DOT, _SEMI = "ASCII_40", "ASCII_41", "ASCII_44", "ASCII_46", "ASCII_59"
_DEPTH = {_OPEN: 1, _CLOSE: -1}


def index_at(tokens: list[Any], pos: int) -> int:
    """The index of the first token at or after the character `pos`."""
    return next(i for i, t in enumerate(tokens) if t.start >= pos)


def tok_text(tok: Any, text: str) -> str:
    return text[tok.start:tok.end + 1]


def written(tokens: list[Any], i: int, text: str) -> tuple[str, int]:
    """The name (dotted parts included) that starts at token `i`, unquoted, and the index of the token after it."""
    j = i
    while j + 2 < len(tokens) and tokens[j + 1].name == _DOT:
        j += 2
    return unquote(text[tokens[i].start:tokens[j].end + 1]), j + 1


def paren_list(tokens: list[Any], i: int, text: str) -> list[str]:
    """The names of the first parenthesized list at or after token `i` (each item's first token)."""
    k = next(n for n in range(i, len(tokens)) if tokens[n].name == _OPEN) + 1
    names = []
    while k < len(tokens) and tokens[k - 1].name != _CLOSE and tokens[k].name != _CLOSE:
        names.append(unquote(tok_text(tokens[k], text)))
        k = element_end(tokens, k) + 1
    return names


def element_end(tokens: list[Any], i: int) -> int:
    """The index of the token that ends the element starting at `i`: a `,` or `;` at its level, or the `)` closing it."""
    depth = 0
    for k in range(i, len(tokens)):
        depth += _DEPTH.get(tokens[k].name, 0)
        if depth < 0 or (depth == 0 and tokens[k].name in (_COMMA, _SEMI)):
            return k
    return len(tokens)
