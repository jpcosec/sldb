"""Scan source files into static fact dictionaries for graph projection."""
from __future__ import annotations

import ast
from pathlib import Path

from .python_source_facts import PythonSourceFacts
from .python_source_values import frontmatter, module_name, source_hash


def scan_source_facts(root: Path, package: str | None) -> list[dict]:
    """Collect source facts for each Python file below a selected root."""
    return [_scan_file(path, root, package) for path in sorted(root.rglob("*.py"))]


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
