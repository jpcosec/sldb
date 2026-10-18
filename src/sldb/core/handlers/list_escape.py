"""A list item's text that markdown would read as block syntax, escaped so it reads back as written.

A scalar item is rendered as `- <value>` and extracted as the item's source text. A value that
opens a code fence (```` ``` ````, `~~~`), a heading, a quote, a nested list, a thematic break or an
HTML block stops being the item's text once rendered: ``["```bash", "pytest", "```"]`` came back
as ``["pytest"]``, and any rewrite of the document, even of another field, deleted the rest.

The value is rendered with one leading backslash (a CommonMark escape: the line stays a
paragraph) and extracted without it. A value that itself starts with a backslash followed by
such a value is escaped too, so the mapping is one-to-one and an item someone wrote as `\\# x`
by hand keeps its backslash only when it had two.
"""

from __future__ import annotations

import re

_BLOCK = re.compile(r"(#{1,6}(\s|$)|>|[-+*](\s|$)|\d{1,9}[.)](\s|$)|`{3,}|~{3,}|\s|$|<|(?P<rule>[-*_])\s*(?P=rule)\s*(?P=rule))")


def needs_escape(value: str) -> bool:
    """Whether `- value` would not read back as `value`: block syntax, or an escape of one."""
    return bool(_BLOCK.match(value)) or (value.startswith("\\") and needs_escape(value[1:]))


def escape_item(value: str) -> str:
    return "\\" + value if needs_escape(value) else value


def unescape_item(text: str) -> str:
    return text[1:] if text.startswith("\\") and needs_escape(text[1:]) else text
