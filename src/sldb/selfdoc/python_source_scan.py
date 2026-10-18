"""Scan source files into static fact dictionaries for graph projection."""
from __future__ import annotations

import ast
from pathlib import Path

from .python_source_facts import PythonSourceFacts
from .python_source_values import frontmatter, module_name, source_hash


def scan_source_facts(root: Path, package: str | None) -> list[dict]:
    """Collect source facts for each Python file below a selected root."""
    return [_scan_file(path, root, package) for path in sorted(root.rglob("*.py"))]


def metadata_diagnostics(root: Path, files: list[dict]) -> list[str]:
    """`path:line: problem` for every malformed docstring metadata and every declared id given
    to two declarations: reported before anything is written (spec section 2)."""
    from .docstring_metadata import parse_docstring

    found, seen = [], {}
    for path in sorted(root.rglob("*.py")):
        tree = ast.parse(path.read_text(encoding="utf-8"), filename=str(path))
        for node in [tree, *(n for n in ast.walk(tree) if isinstance(n, (ast.ClassDef, ast.FunctionDef, ast.AsyncFunctionDef)))]:
            found += _node_diagnostics(path.relative_to(root), node, parse_docstring(ast.get_docstring(node, clean=True)), seen)
    return found


def _node_diagnostics(rel: Path, node: ast.AST, meta, seen: dict) -> list[str]:
    where = f"{rel}:{getattr(node, 'lineno', 1)}"
    problems = [f"{where}: {error}" for error in meta.errors]
    declared = meta.values.get("id") if meta.declared and not meta.errors else None
    if declared and declared in seen:
        problems.append(f"{where}: declared id '{declared}' is also declared at {seen[declared]}")
    elif declared:
        seen[declared] = where
    return problems


def _scan_file(path: Path, root: Path, package: str | None) -> dict:
    text = path.read_text(encoding="utf-8")
    tree = ast.parse(text, filename=str(path))
    visitor = PythonSourceFacts(module_name(path, root, package), str(path.relative_to(root)), source_hash(text), tree)
    visitor.visit(tree)
    return _file_fact(visitor, tree)


def _file_fact(visitor: PythonSourceFacts, tree: ast.Module) -> dict:
    return {"module": visitor.module, "id": visitor.module_id, "path": visitor.path, "hash": visitor.digest,
            "metadata": frontmatter(tree), "symbols": visitor.symbols, "imports": visitor.imports,
            "references": visitor.references}
