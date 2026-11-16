"""Readers over tree-sitter TypeScript/JavaScript nodes: top-level declarations, their kind, JSDoc, signature, imports.

A declaration is a `function`, a `const`/`let`/`var` whose value is a function (directly or as the
first argument of a wrapping call, `memo(...)`, `forwardRef(...)`), or, in `.ts`/`.tsx`, a `type`
or an `interface`; exported or not. Reexports (`export { X } from ...`) declare nothing; an unnamed
`export default` takes the module's last segment as its name. Kinds: `hook` (`use` + capital),
`component` (capital and a JSX node anywhere in it), `type`, else `function`.
"""

from __future__ import annotations

import inspect
import re
from typing import Any

from sldb.code.readers import field_text, py_norm, text

_FUNCTIONS = {"arrow_function", "function_expression", "function", "function_declaration", "generator_function_declaration", "generator_function"}
_TYPES = {"type_alias_declaration", "interface_declaration"}
_VARIABLES = {"lexical_declaration", "variable_declaration"}
_JSX = {"jsx_element", "jsx_self_closing_element", "jsx_fragment"}
_HOOK = re.compile(r"use[A-Z]")


def function_of(value: Any) -> Any:
    """The function a value holds: itself, or the first argument of a wrapping call, recursively; None otherwise."""
    if value is None or value.type in _FUNCTIONS:
        return value
    args = value.child_by_field_name("arguments") if value.type == "call_expression" else None
    return function_of(args.named_children[0]) if args is not None and args.named_children else None


def declarations(stmt: Any, default_name: str, typed: bool, src: bytes) -> list[tuple[str, Any, Any]]:
    """`(name, node, function or None)` of each declaration a top-level statement makes."""
    inner = stmt.child_by_field_name("declaration") or stmt.child_by_field_name("value") if stmt.type == "export_statement" else stmt
    if inner is None:
        return []
    if inner.type in _VARIABLES:
        pairs = [(d, function_of(d.child_by_field_name("value"))) for d in inner.named_children if d.type == "variable_declarator"]
        return [(field_text(d, src, "name"), d, fn) for d, fn in pairs if fn is not None]
    if inner.type in _TYPES:
        return [(field_text(inner, src, "name"), inner, None)] if typed else []
    fn = function_of(inner)
    return [(field_text(inner, src, "name") or default_name, inner, fn)] if fn is not None else []


def kind_of(name: str, node: Any, fn: Any) -> str:
    if fn is None:
        return "type"
    if _HOOK.match(name):
        return "hook"
    return "component" if name[:1].isupper() and has_jsx(node) else "function"


def has_jsx(node: Any) -> bool:
    stack = [node]
    while stack:
        n = stack.pop()
        if n.type in _JSX:
            return True
        stack.extend(n.named_children)
    return False


def jsdoc(stmt: Any, src: bytes) -> str | None:
    """The `/** ... */` that ends on the line just before `stmt` (the last one, when several), without delimiters or `*`."""
    prev = stmt.prev_sibling
    if prev is None or prev.type != "comment" or not text(prev, src).startswith("/**") or prev.end_point[0] + 1 != stmt.start_point[0]:
        return None
    lines = [re.sub(r"^\s*\*? ?", "", line) for line in text(prev, src)[3:-2].splitlines()]
    return inspect.cleandoc("\n".join(lines)).strip() or None


def ts_signature(name: str, fn: Any, src: bytes) -> str | None:
    """`name(params)` like the Python reader's; None for a type."""
    if fn is None:
        return None
    params = fn.child_by_field_name("parameters")
    inner = [c for c in params.named_children if c.type != "comment"] if params is not None else [fn.child_by_field_name("parameter")]
    return f"{name}({', '.join(py_norm(text(p, src)) for p in inner if p is not None)})"


def ts_imports(root: Any, src: bytes) -> list[str]:
    """The source of each top-level `import`, sorted: `import R from "react"` is `react`."""
    sources = [s.child_by_field_name("source") for s in root.named_children if s.type == "import_statement"]
    return sorted({text(s, src)[1:-1] for s in sources if s is not None})
