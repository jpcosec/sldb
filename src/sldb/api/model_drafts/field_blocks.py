"""Insert or remove one field declaration in a model class's source text."""

from __future__ import annotations

import ast
from pathlib import Path
from typing import Any

from sldb.api.model_drafts.source_editing import find_class_node, remove_node_block
from sldb.core.exceptions import SLDBModelEditError


def field_block(field_name: str, field_type: str, description: str, default_supplied: bool, default_value: Any) -> str:
    """The source line declaring a pydantic field, with a default when one is supplied."""
    if default_supplied:
        return f"    {field_name}: {field_type} = Field(default={default_value!r}, description={description!r})\n"
    return f"    {field_name}: {field_type} = Field(description={description!r})\n"


def insert_field_block(path: Path, cls_name: str, f_name: str, f_block: str) -> str:
    """The source of `path` with `f_block` appended to the body of class `cls_name`.

    Raises:
        SLDBModelEditError: When the class is missing or already declares the field.
    """
    source = path.read_text(encoding="utf-8")
    class_node = find_class_node(ast.parse(source), cls_name, path)
    check_field_absent(class_node, cls_name, f_name)
    lines = source.splitlines(keepends=True)
    lines.insert(class_node.body[-1].end_lineno or len(lines), f_block)
    return "".join(lines)


def check_field_absent(class_node: ast.ClassDef, cls_name: str, f_name: str) -> None:
    """Refuse to add a field the class already declares."""
    for node in class_node.body:
        if isinstance(node, ast.AnnAssign) and isinstance(node.target, ast.Name) and node.target.id == f_name:
            raise SLDBModelEditError(f"Field '{f_name}' already exists in '{cls_name}'.")


def field_node(class_node: ast.ClassDef, class_name: str, field_name: str) -> ast.AnnAssign:
    """The annotated assignment declaring a field.

    Raises:
        SLDBModelEditError: When the class does not declare the field.
    """
    for node in class_node.body:
        if isinstance(node, ast.AnnAssign) and isinstance(node.target, ast.Name) and node.target.id == field_name:
            return node
    raise SLDBModelEditError(f"Field '{field_name}' does not exist in '{class_name}'.")


def remove_field_block(path: Path, class_name: str, field_name: str) -> str:
    """The source of `path` without the declaration of `field_name` in class `class_name`."""
    source = path.read_text(encoding="utf-8")
    class_node = find_class_node(ast.parse(source), class_name, path)
    return remove_node_block(source, field_node(class_node, class_name, field_name))
