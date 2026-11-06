"""Read, replace or insert class-level metadata assignments in a model's source text."""

from __future__ import annotations

import ast
from pathlib import Path
from typing import Any

from sldb.api.model_drafts.source_editing import find_class_node, replace_rhs_expression


def find_metadata_assign(class_node: ast.ClassDef, attr_name: str) -> ast.Assign | None:
    """The class's `attr_name = ...` assignment, or None when absent."""
    for node in class_node.body:
        if isinstance(node, ast.Assign) and any(isinstance(t, ast.Name) and t.id == attr_name for t in node.targets):
            return node
    return None


def read_metadata_literal(path: Path, class_name: str, attr_name: str) -> Any:
    """The literal value class `class_name` assigns to `attr_name` at `path`."""
    source = path.read_text(encoding="utf-8")
    class_node = find_class_node(ast.parse(source), class_name, path)
    assign = find_metadata_assign(class_node, attr_name)
    if assign is None:
        return None
    try:
        return ast.literal_eval(assign.value)
    except Exception:
        return None


def replace_or_insert_metadata(source: str, class_name: str, path: Path, attr_name: str, value: Any) -> str:
    """The source of `path` with `attr_name` updated to `repr(value)`, inserting if missing."""
    tree = ast.parse(source)
    class_node = find_class_node(tree, class_name, path)
    assign = find_metadata_assign(class_node, attr_name)
    if assign is not None:
        return replace_rhs_expression(source, assign.value, repr(value))
    return insert_metadata_assignment(source, class_name, path, attr_name, value)


def insert_metadata_assignment(source: str, class_name: str, path: Path, attr_name: str, value: Any) -> str:
    """Insert `attr_name = value` into class `class_name`."""
    tree = ast.parse(source)
    class_node = find_class_node(tree, class_name, path)
    lines = source.splitlines(keepends=True)
    if not class_node.body:
        indent = "    "
        insert_line = class_node.lineno
    else:
        first = class_node.body[0]
        first_line = lines[first.lineno - 1]
        indent = first_line[: len(first_line) - len(first_line.lstrip())] or "    "
        meta_assigns = [
            node for node in class_node.body
            if isinstance(node, ast.Assign) and any(
                isinstance(t, ast.Name) and t.id.startswith("__") and t.id.endswith("__")
                for t in node.targets
            )
        ]
        if meta_assigns:
            insert_line = meta_assigns[-1].end_lineno or meta_assigns[-1].lineno
        elif _is_docstring(first):
            insert_line = first.end_lineno or first.lineno
        else:
            insert_line = first.lineno - 1

    lines.insert(insert_line, f"{indent}{attr_name} = {repr(value)}\n")
    return "".join(lines)


def _is_docstring(node: ast.stmt) -> bool:
    return isinstance(node, ast.Expr) and isinstance(node.value, ast.Constant) and isinstance(node.value.value, str)
