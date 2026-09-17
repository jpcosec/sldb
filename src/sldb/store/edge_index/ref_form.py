"""Reader of the one s-expression an anchor's `ref` may be written as (pron spec 13):
lists, bare symbols and quoted strings."""

from __future__ import annotations

import re
from typing import Any

from sldb.store.edge_index.ref_symbol import RefSymbol

_FORM_TOKEN = re.compile(r'\s*(?:(\()|(\))|"((?:[^"\\]|\\.)*)"|([^\s()"]+))')


def read_form(text: str) -> Any:
    """The first form of `text` as nested lists of RefSymbol and str; [] when there is none."""
    stack: list[list] = [[]]
    pos, text = 0, text.strip()
    while pos < len(text):
        m = _FORM_TOKEN.match(text, pos)
        if m is None or m.end() == pos:
            break
        pos = m.end()
        _push_token(stack, m)
    return stack[0][0] if stack[0] else []


def _push_token(stack: list[list], m: re.Match) -> None:
    if m.group(1):
        stack.append([])
    elif m.group(2):
        done = stack.pop()
        stack[-1].append(done)
    elif m.group(3) is not None:
        stack[-1].append(re.sub(r"\\(.)", r"\1", m.group(3)))
    elif m.group(4) is not None:
        stack[-1].append(RefSymbol(m.group(4)))
