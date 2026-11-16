"""A module's name from its path, the imports its top level declares (from kimun's adapter), and the
nested ones: every import statement that is not a direct child of the module node."""

from __future__ import annotations

import os
from typing import Any

from sldb.code.readers import field_text, text

_IMPORTS = {"import_statement", "future_import_statement", "import_from_statement"}


def py_module_name(rel: str) -> str:
    parts = rel[:-len(os.path.splitext(rel)[1])].split("/")
    if parts[-1] == "__init__":
        parts.pop()
    return ".".join(parts)


def py_imports(root: Any, src: bytes) -> set[str]:
    """The imports of the top level: one entry per statement that is a direct child of `root`."""
    return {_entry(stmt, src) for stmt in root.named_children if stmt.type in _IMPORTS}


def py_nested_imports(root: Any, src: bytes) -> set[str]:
    """The imports below the top level (inside `def`, `class`, `if`, `try`, `with`...), same format as `py_imports`."""
    out: set[str] = set()
    stack = [c for stmt in root.named_children for c in stmt.named_children]
    while stack:
        node = stack.pop()
        if node.type in _IMPORTS:
            out.add(_entry(node, src))
        else:
            stack.extend(node.named_children)
    return out


def _entry(stmt: Any, src: bytes) -> str:
    if stmt.type == "import_statement":
        return _import_names(stmt, src)
    if stmt.type == "future_import_statement":
        return "__future__"
    return "".join(field_text(stmt, src, "module_name").split())


def _import_names(stmt: Any, src: bytes) -> str:
    names = [field_text(c, src, "name") if c.type == "aliased_import" else text(c, src) for c in stmt.children_by_field_name("name")]
    return ",".join("".join(n.split()) for n in names)
