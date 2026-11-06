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
    class_node = find_class_node(ast.parse(source), class_name, path)
    lines = source.splitlines(keepends=True)
    indent, insert_line = _insertion_point(class_node, lines)
    lines.insert(insert_line, f"{indent}{attr_name} = {repr(value)}\n")
    return "".join(lines)


def _is_dunder_assign(node: ast.stmt) -> bool:
    """Whether the statement assigns a `__dunder__` name."""
    return isinstance(node, ast.Assign) and any(isinstance(t, ast.Name) and t.id.startswith("__") and t.id.endswith("__") for t in node.targets)


def _insertion_point(class_node: ast.ClassDef, lines: list[str]) -> tuple[str, int]:
    """The indent and the line after which a new metadata assignment goes."""
    if not class_node.body:
        return "    ", class_node.lineno
    first = class_node.body[0]
    indent = _indent_of(lines[first.lineno - 1])
    metas = [n for n in class_node.body if _is_dunder_assign(n)]
    if metas:
        return indent, metas[-1].end_lineno or metas[-1].lineno
    return indent, (first.end_lineno or first.lineno) if _is_docstring(first) else first.lineno - 1


def _indent_of(line: str) -> str:
    """The line's leading whitespace, four spaces when it has none."""
    return line[: len(line) - len(line.lstrip())] or "    "


def _is_docstring(node: ast.stmt) -> bool:
    return isinstance(node, ast.Expr) and isinstance(node.value, ast.Constant) and isinstance(node.value.value, str)
