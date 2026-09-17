"""Edit Python source text by AST node positions, keeping every other byte intact.

Moved here from `sldb.cli.commands.models_utils`, which re-exports these names.
"""

from __future__ import annotations

import ast
from pathlib import Path

from sldb.core.exceptions import SLDBModelEditError


def find_class_node(tree: ast.Module, class_name: str, path: Path) -> ast.ClassDef:
    """The top-level class statement named `class_name`.

    Raises:
        SLDBModelEditError: When the module defines no such class.
    """
    for node in tree.body:
        if isinstance(node, ast.ClassDef) and node.name == class_name:
            return node
    raise SLDBModelEditError(f"Class '{class_name}' not found in {path}.")


def remove_node_block(source: str, node: ast.stmt) -> str:
    """The source without the whole lines a statement spans."""
    lines = source.splitlines(keepends=True)
    start_line = node.lineno - 1
    end_line = node.end_lineno
    del lines[start_line:end_line]
    return "".join(lines)


def replace_rhs_expression(source: str, node: ast.expr, replacement: str) -> str:
    """The source with an expression's text replaced (AST column offsets are UTF-8 byte offsets)."""
    # ast col_offset/end_col_offset son offsets en BYTES utf-8; las líneas se
    # parten por bytes para que el corte no se corra con caracteres multibyte.
    lines = source.splitlines(keepends=True)
    s_line, e_line = node.lineno - 1, (node.end_lineno or node.lineno) - 1
    s_col, e_col = node.col_offset, node.end_col_offset
    if s_line == e_line:
        raw = lines[s_line].encode('utf-8')
        lines[s_line] = (raw[:s_col] + replacement.encode('utf-8') + raw[e_col:]).decode('utf-8')
    else:
        s_raw, e_raw = lines[s_line].encode('utf-8'), lines[e_line].encode('utf-8')
        lines[s_line : e_line + 1] = [(s_raw[:s_col] + replacement.encode('utf-8') + e_raw[e_col:]).decode('utf-8')]
    return "".join(lines)
