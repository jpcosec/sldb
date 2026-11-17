"""The text of a called TypeScript/JavaScript expression that is not canonical (`ts_callee`): its source
text without the `await` keywords and without the type arguments of a call, `new` or `x<T>`, with each
run of whitespace collapsed to one space (not removed): `new Set(xs).has`, `(a ?? []).map`,
`[...x].sort`, `'a b'.split`. Whitespace inside a literal is collapsed too.
"""

from __future__ import annotations

from typing import Any

_GENERIC = {"call_expression", "new_expression", "instantiation_expression"}


def loose_text(node: Any, src: bytes) -> str:
    """`node`'s text minus `await` and type arguments, whitespace runs collapsed to one space."""
    parts, pos = [], node.start_byte
    for start, end in sorted(_dropped(node)):
        if start >= pos:
            parts.append(src[pos:start])
            pos = end
    parts.append(src[pos:node.end_byte])
    return " ".join(b"".join(parts).decode("utf-8", "replace").split())


def _dropped(node: Any) -> list[tuple[int, int]]:
    """Byte ranges to drop: an `await` keyword with its trailing whitespace, a call's type arguments."""
    out, stack = [], [node]
    while stack:
        n = stack.pop()
        if n.type == "await_expression" and n.named_child_count:
            out.append((n.start_byte, n.named_children[0].start_byte))
        elif n.type == "type_arguments" and n.parent is not None and n.parent.type in _GENERIC:
            out.append((n.start_byte, n.end_byte))
        stack.extend(n.named_children)
    return out
