"""Read or replace the `__template__` literal of a model class in its source text."""

from __future__ import annotations

import ast
from pathlib import Path

from sldb.api.model_drafts.source_editing import find_class_node, replace_rhs_expression
from sldb.core.exceptions import SLDBModelEditError


def template_assign_node(class_node: ast.ClassDef, class_name: str) -> ast.Assign:
    """The class's `__template__ = ...` statement.

    Raises:
        SLDBModelEditError: When the class assigns no `__template__`.
    """
    for node in class_node.body:
        if isinstance(node, ast.Assign) and any(isinstance(t, ast.Name) and t.id == "__template__" for t in node.targets):
            return node
    raise SLDBModelEditError(f"Class '{class_name}' has no __template__ assignment.")


def template_literal(template: str) -> str:
    """Source text of a stripped triple-quoted literal holding the template."""
    escaped = template.replace('"""', '\"\"\"')
    return f'"""{escaped}""".strip()'


def replace_template_literal(path: Path, class_name: str, template: str) -> str:
    """The source of `path` with class `class_name`'s template replaced by `template`."""
    source = path.read_text(encoding="utf-8")
    class_node = find_class_node(ast.parse(source), class_name, path)
    assign_node = template_assign_node(class_node, class_name)
    return replace_rhs_expression(source, assign_node.value, template_literal(template))


def read_template_literal(path: Path, class_name: str) -> str:
    """The template text class `class_name` declares in the source at `path`."""
    source = path.read_text(encoding="utf-8")
    class_node = find_class_node(ast.parse(source), class_name, path)
    value_node = template_assign_node(class_node, class_name).value
    literal = value_node.func.value if isinstance(value_node, ast.Call) else value_node  # type: ignore[attr-defined]
    template: str = ast.literal_eval(literal)
    return template
