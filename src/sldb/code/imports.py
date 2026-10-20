"""A module's name from its path, and the imports its top level declares (from kimun's adapter)."""

from __future__ import annotations

import os
from typing import Any

from sldb.code.readers import field_text, text


def py_module_name(rel: str) -> str:
    parts = rel[:-len(os.path.splitext(rel)[1])].split("/")
    if parts[-1] == "__init__":
        parts.pop()
    return ".".join(parts)


def py_imports(root: Any, src: bytes) -> set[str]:
    out: set[str] = set()
    for stmt in root.named_children:
        if stmt.type == "import_statement":
            out.add(_import_names(stmt, src))
        elif stmt.type == "future_import_statement":
            out.add("__future__")
        elif stmt.type == "import_from_statement":
            out.add("".join(field_text(stmt, src, "module_name").split()))
    return out


def _import_names(stmt: Any, src: bytes) -> str:
    names = [field_text(c, src, "name") if c.type == "aliased_import" else text(c, src) for c in stmt.children_by_field_name("name")]
    return ",".join("".join(n.split()) for n in names)
