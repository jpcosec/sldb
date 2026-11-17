"""The file's statements as Postgres reads them, through pglast (libpg_query, Postgres' own parser): extra `[postgres]`.

`pg_statements` splits the file with Postgres' scanner and parses each statement on its own, so one
statement that does not parse leaves the others readable. It gives `None` when pglast is not
installed (the `.sql` reading is then tree-sitter's alone) and `[]` when the scanner cannot split the
file (an unterminated quote): then no statement counts as parsed. Each statement carries its byte
range in the file, its text (as parsed) and `raw` text (as decoded), its tokens without comments
(positions are characters of that text, as pglast gives them) and its parsed node, or `None` when Postgres rejects it.

A file that is not UTF-8 (a Latin-1 comment) is decoded with `surrogateescape`, so each invalid byte
is one character of the `raw` text and `to_byte` maps back to the file's bytes exactly. Postgres only
reads UTF-8, so the text it parses has each of those characters as one U+FFFD: the same characters
at the same positions, the bytes the tree-sitter reading also shows as U+FFFD.
"""

from __future__ import annotations

import re
from typing import Any

try:
    from pglast import parser as _pg
    from pglast.enums import ObjectType
except ImportError:  # the extra [postgres] is not installed
    _pg = None

_COMMENTS = ("SQL_COMMENT", "C_COMMENT")
_ESCAPED = re.compile("[\udc80-\udcff]")


def pg_statements(src: bytes) -> list[dict[str, Any]] | None:
    if _pg is None:
        return None
    raw = src.decode("utf-8", "surrogateescape")
    text = _ESCAPED.sub("\ufffd", raw)
    try:
        return [_statement(raw, text, s.start, s.stop) for s in _pg.split(text, with_parser=False, only_slices=True)]
    except _pg.ParseError:
        return []


def is_table(node: Any) -> bool:
    """Whether an `AlterTableStmt` is about a table (not an index, a view or a sequence)."""
    return node.objtype == ObjectType.OBJECT_TABLE


def to_byte(stmt: dict[str, Any], pos: int) -> int:
    """The byte offset in the file of the character `pos` of the statement's text."""
    return stmt["start"] + _nbytes(stmt["raw"][:pos])


def _nbytes(raw: str) -> int:
    return len(raw.encode("utf-8", "surrogateescape"))


def _statement(raw: str, text: str, start: int, stop: int) -> dict[str, Any]:
    body, base = text[start:stop], _nbytes(raw[:start])
    return {"start": base, "end": base + _nbytes(raw[start:stop]), "text": body, "raw": raw[start:stop], "tokens": [t for t in _pg.scan(body) if t.name not in _COMMENTS], "node": _parse(body)}


def _parse(body: str) -> Any:
    try:
        return _pg.parse_sql(body)[0].stmt
    except _pg.ParseError:
        return None
