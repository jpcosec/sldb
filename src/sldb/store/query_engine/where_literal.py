"""String literals of the `--where` grammar: their pattern, their value, and how to write one.

`split_outside_literals` cuts an expression where a separator appears outside every literal,
so a quoted `" and "` or `"{x}"` is never mistaken for grammar.
"""

from __future__ import annotations

import re
from decimal import Decimal
from typing import Any

# '"', then non-quote/non-backslash chars or a backslash escaping any char, then '"'.
# The value unquotes \" -> " and \\ -> \.
LITERAL = r'"(?:[^"\\]|\\.)*"'
LITERAL_NONEMPTY = r'("(?:[^"\\]|\\.)+")'


def unquote(raw: str) -> str:
    """The literal's value: the quotes off, the two escapes resolved; any other backslash survives verbatim."""
    body, out, i = raw[1:-1], [], 0
    while i < len(body):
        if body[i] == "\\" and i + 1 < len(body) and body[i + 1] in ('"', "\\"):
            out.append(body[i + 1])
            i += 2
        else:
            out.append(body[i])
            i += 1
    return "".join(out)


def quote(value: str) -> str:
    """The literal whose value is `value` (the inverse of `unquote`)."""
    return '"' + value.replace("\\", "\\\\").replace('"', '\\"') + '"'


def split_outside_literals(text: str, separator: str) -> list[str]:
    """`text` cut at every match of the `separator` regex that is not inside a literal."""
    parts, last = [], 0
    for m in re.finditer(f"({LITERAL})|{separator}", text):
        if m.group(1) is None:
            parts.append(text[last:m.start()])
            last = m.end()
    return parts + [text[last:]]


def scalar_literal(value: Any) -> str | None:
    """`value` written in the grammar: a quoted string or a number; None for anything else."""
    if isinstance(value, bool) or not isinstance(value, (str, int, float)):
        return None
    return quote(value) if isinstance(value, str) else format(Decimal(repr(value)), "f")
