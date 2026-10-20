"""Readers over tree-sitter Python nodes: text, docstring, signature, kind (from kimun's adapter)."""

from __future__ import annotations

import ast
import inspect
import re
from typing import Any


def text(node: Any, src: bytes) -> str:
    return src[node.start_byte:node.end_byte].decode("utf-8", "replace")


def field_text(node: Any, src: bytes, field: str) -> str | None:
    child = node.child_by_field_name(field)
    return text(child, src) if child is not None else None


def first_statement(block: Any) -> Any:
    """First non-comment named child of a body-like node."""
    for child in block.named_children if block is not None else []:
        if child.type != "comment":
            return child
    return None


def py_string_value(node: Any, src: bytes) -> str | None:
    """Evaluate a (possibly implicitly concatenated) string literal; None if not a plain str."""
    try:
        value = ast.literal_eval("(" + text(node, src) + "\n)")
    except (ValueError, SyntaxError):
        return None
    return value if isinstance(value, str) else None


def docstring_node(node: Any) -> Any:
    """The expression statement holding the docstring of a module, class or function, or None."""
    body = node if node.type == "module" else node.child_by_field_name("body")
    stmt = first_statement(body)
    if stmt is None or stmt.type != "expression_statement" or stmt.named_child_count != 1:
        return None
    return stmt if stmt.named_children[0].type in ("string", "concatenated_string") else None


def py_doc(node: Any, src: bytes) -> str | None:
    stmt = docstring_node(node)
    value = py_string_value(stmt.named_children[0], src) if stmt is not None else None
    return None if value is None else inspect.cleandoc(value)


def py_end_line(node: Any) -> int:
    """Line of the last real token: tree-sitter lets a block swallow trailing comment lines, ast does not."""
    while True:
        kids = [c for c in node.children if c.type != "comment"]
        if not kids:
            return node.end_point[0] + 1
        node = kids[-1]


def py_norm(t: str) -> str:
    """Whitespace-collapse and requote simple "x" strings as 'x' (what ast.unparse prints)."""
    return re.sub(r'(?<![\w"])"([^"\'\\\n]*)"(?!")', r"'\1'", " ".join(t.split()))


def py_param(p: Any, src: bytes) -> str:
    if p.type == "typed_default_parameter":
        return f"{field_text(p, src, 'name')}: {py_norm(field_text(p, src, 'type'))}={py_norm(field_text(p, src, 'value'))}"
    if p.type == "default_parameter":
        return f"{field_text(p, src, 'name')}={py_norm(field_text(p, src, 'value'))}"
    return py_norm(text(p, src))


def py_signature(node: Any, src: bytes) -> str | None:
    if node.type != "function_definition":
        return None
    params = node.child_by_field_name("parameters")
    inner = [py_param(c, src) for c in params.named_children if c.type != "comment"]
    return f"{field_text(node, src, 'name')}({', '.join(inner)})"


def py_native_kind(node: Any, src: bytes) -> str:
    if node.type == "class_definition":
        return "ClassDef"
    is_async = any(c.type == "async" for c in node.children if c.start_byte < node.child_by_field_name("name").start_byte)
    return "AsyncFunctionDef" if is_async else "FunctionDef"
