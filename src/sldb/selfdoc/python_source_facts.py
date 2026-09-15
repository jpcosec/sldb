"""Collect lexical declarations, imports, and annotations without execution."""
from __future__ import annotations

import ast

from .python_source_values import annotation_names, declared_id, frontmatter


class PythonSourceFacts(ast.NodeVisitor):
    """Visit one module and retain source-located static facts."""

    def __init__(self, module: str, path: str, digest: str, tree: ast.Module) -> None:
        self.module, self.path, self.digest = module, path, digest
        self.module_id = declared_id(tree, f"python:{module}")
        self.owners, self.symbols, self.imports, self.references = [self.module_id], [], [], []

    def visit_ClassDef(self, node: ast.ClassDef) -> None:
        self._declaration(node, "ClassDef")

    def visit_FunctionDef(self, node: ast.FunctionDef) -> None:
        self._declaration(node, "FunctionDef")

    def visit_AsyncFunctionDef(self, node: ast.AsyncFunctionDef) -> None:
        self._declaration(node, "AsyncFunctionDef")

    def _declaration(self, node, kind: str) -> None:
        parent, qualname = self.owners[-1], ".".join([item["name"] for item in self.symbols if item["id"] in self.owners[1:]] + [node.name])
        fact = self._symbol(node, kind, parent, qualname)
        self.symbols.append(fact); self.owners.append(fact["id"]); self.generic_visit(node); self.owners.pop()

    def _symbol(self, node, kind, parent, qualname) -> dict:
        fallback = f"python:{self.module}:{qualname}"
        return {"id": declared_id(node, fallback), "parent": parent, "name": node.name, "kind": kind,
                "metadata": frontmatter(node), "line": node.lineno, "end": node.end_lineno}

    def visit_Import(self, node: ast.Import) -> None:
        for alias in node.names:
            self._binding(node, alias.name, None, alias.asname, 0)

    def visit_ImportFrom(self, node: ast.ImportFrom) -> None:
        for alias in node.names:
            self._binding(node, node.module or "", alias.name, alias.asname, node.level)

    def _binding(self, node, module, name, alias, level) -> None:
        local = alias or (name or module.split(".")[0])
        self.imports.append({"owner": self.owners[-1], "module": module, "name": name, "alias": alias,
                             "local": local, "level": level, "line": node.lineno, "end": node.end_lineno})

    def visit_AnnAssign(self, node: ast.AnnAssign) -> None:
        if isinstance(node.target, ast.Name):
            self._references(node.target.id, node.annotation, node)
        self.generic_visit(node)

    def _references(self, site: str, annotation: ast.AST, node: ast.AST) -> None:
        for name in annotation_names(annotation):
            self.references.append({"owner": self.owners[-1], "site": site, "name": name,
                                    "expression": ast.unparse(annotation), "line": node.lineno, "end": node.end_lineno})
