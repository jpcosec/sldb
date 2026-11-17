"""SQL identifiers as the tree delimits them: quotes off, `""` as `"`, the parts joined by dots.

A name is read from the bytes of tree-sitter nodes (`exact_name`, which the reading with the extra
`[postgres]` uses; without it `sql_readers.sql_name` keeps the reading of before). tree-sitter-sql
0.3.13 splits a quoted identifier with an escaped quote (`"a""b"`) into `"a"` and a second token,
often an `ERROR`; a name node (a table, a column) runs on over the quoted parts glued to its
closing quote (`name_end`): `"a""b"."c""d"` is `a"b.c"d`.
"""

from __future__ import annotations

import re
from typing import Any

_PART = re.compile(r'"((?:[^"]|"")*)"|([^".\s]+)')
_GLUED = re.compile(rb'"(?:[^"]|"")*"|\s*\.\s*(?:"(?:[^"]|"")*"|[\w$]+)')


def unquote(raw: str) -> str:
    """`"public"."users"` is `public.users`, `"a""b"` is `a"b`."""
    return ".".join(bare or quoted.replace('""', '"') for quoted, bare in _PART.findall(raw))


def name_end(node: Any, src: bytes) -> int:
    """Where the identifier that starts at `node` ends: past the quoted parts the grammar split from it."""
    end = node.end_byte
    while src[end - 1:end] == b'"' and (m := _GLUED.match(src, end)) is not None:
        end = m.end()
    return end


def exact_name(node: Any, src: bytes) -> str:
    """A tree-sitter name node's name: `"public"."users"` is `public.users`, `"a""b"` is `a"b`."""
    return unquote(src[node.start_byte:name_end(node, src)].decode("utf-8", "replace"))
