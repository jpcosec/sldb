"""The name of a called TypeScript/JavaScript expression and whether it is canonical.

A chain that starts at an identifier, `this`, `super` or a function is canonical, built from the tree,
not the text: identifiers and property names joined by `.` (`?.` and `!` when written), with no
whitespace, no `await` and no type arguments (`client\\n  .documents` gives `client.documents`). A
link of the chain that is itself a call is written `()` without its arguments (`fetch(url).then(cb).then`
gives `fetch().then().then`; `(await listDocuments(m)).slice` gives `listDocuments().slice`). An
anonymous function or IIFE as object is `(fn)`; an index access is `[]` (`?.[]` when optional).
Parentheses, `await`, `as`/`satisfies` and `x<T>` are seen through.

A chain that starts at anything else (an array, a binary expression, a `new`, a literal...) is not
canonical: its name is the text of the called expression as `ts_loose` gives it (`new Set(xs).has`,
`(a ?? []).map`), and the caller flags it `canonical: false`.
"""

from __future__ import annotations

from typing import Any

from sldb.code.readers import text
from sldb.code.ts_loose import loose_text

_LEAVES = {"identifier", "property_identifier", "private_property_identifier", "this", "super"}
_FUNCTIONS = {"arrow_function", "function_expression", "function", "generator_function"}
_SEEN_THROUGH = {"await_expression", "parenthesized_expression", "as_expression", "satisfies_expression",
                 "instantiation_expression", "non_null_expression"}
_CHAIN = {"member_expression": "object", "subscript_expression": "object", "call_expression": "function"}


def call_name(node: Any, src: bytes) -> tuple[str, bool]:
    """`(name, canonical)` of `node`, the `function` field of a call."""
    root = _root(node)
    if root is not None and (root.type in _LEAVES or root.type in _FUNCTIONS):
        return _canonical(node, src), True
    return loose_text(node, src), False


def _root(node: Any) -> Any:
    """Where the chain starts: down objects, called functions and seen-through wrappers."""
    while node is not None:
        if node.type in _SEEN_THROUGH and node.named_child_count:
            node = node.named_children[0]
        elif node.type in _CHAIN:
            node = node.child_by_field_name(_CHAIN[node.type])
        else:
            return node
    return None


def _canonical(node: Any, src: bytes) -> str:
    kind = node.type
    if kind in _LEAVES:
        return text(node, src)
    if kind in _FUNCTIONS:
        return "(fn)"
    if kind == "non_null_expression":
        return _canonical(node.named_children[0], src) + "!"
    if kind in _SEEN_THROUGH:
        return _canonical(node.named_children[0], src)
    return _BUILDERS[kind](node, src)


def _optional(node: Any) -> bool:
    return any(c.type == "optional_chain" for c in node.children)


def _member(node: Any, src: bytes) -> str:
    dot = "?." if _optional(node) else "."
    return _canonical(node.child_by_field_name("object"), src) + dot + text(node.child_by_field_name("property"), src)


def _subscript(node: Any, src: bytes) -> str:
    return _canonical(node.child_by_field_name("object"), src) + ("?.[]" if _optional(node) else "[]")


def _call(node: Any, src: bytes) -> str:
    return _canonical(node.child_by_field_name("function"), src) + "()"


_BUILDERS = {"member_expression": _member, "subscript_expression": _subscript, "call_expression": _call}
