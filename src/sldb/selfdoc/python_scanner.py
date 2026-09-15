"""Static Python AST inventory with no imports or handler execution."""
from __future__ import annotations

import ast
import hashlib
from pathlib import Path

from .python_symbol import PythonSymbol


class PythonScanner:
    """Scan Python files into deterministic, qualified symbol facts."""

    def scan(self, source_root: Path, package: str | None = None) -> list[PythonSymbol]:
        return [symbol for path in sorted(source_root.rglob("*.py")) for symbol in self._file_symbols(path, source_root, package)]

    def _file_symbols(self, path: Path, root: Path, package: str | None) -> list[PythonSymbol]:
        text = path.read_text(encoding="utf-8")
        module = self._module_name(path, root, package)
        tree = ast.parse(text, filename=str(path))
        return self._symbols(tree, path, root, module, hashlib.sha256(text.encode()).hexdigest())

    def _module_name(self, path: Path, root: Path, package: str | None) -> str:
        parts = list(path.relative_to(root).with_suffix("").parts)
        if parts[-1] == "__init__": parts.pop()
        return ".".join(([package] if package else []) + parts)

    def _symbols(self, tree, path, root, module, digest) -> list[PythonSymbol]:
        imports = self._imports(tree)
        return self._walk(tree.body, path, root, module, digest, imports, [])

    def _walk(self, nodes, path, root, module, digest, imports, parents) -> list[PythonSymbol]:
        records = []
        for node in nodes:
            if isinstance(node, (ast.ClassDef, ast.FunctionDef, ast.AsyncFunctionDef)):
                records.append(self._symbol(node, path, root, module, digest, imports, parents))
                records.extend(self._walk(node.body, path, root, module, digest, imports, [*parents, node.name]))
        return records

    def _symbol(self, node, path, root, module, digest, imports, parents) -> PythonSymbol:
        qualname = ".".join([*parents, node.name])
        return PythonSymbol(id=f"python:{module}:{qualname}", kind=type(node).__name__, module=module,
            qualname=qualname, path=str(path.relative_to(root)), line_start=node.lineno, line_end=node.end_lineno,
            signature=self._signature(node), docstring=ast.get_docstring(node), source_sha256=digest, imports=imports)

    def _signature(self, node) -> str | None:
        if not isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)): return None
        return f"{node.name}({ast.unparse(node.args)})"

    def _imports(self, tree) -> list[str]:
        return sorted({self._import_name(node) for node in tree.body if isinstance(node, (ast.Import, ast.ImportFrom))})

    def _import_name(self, node) -> str:
        if isinstance(node, ast.Import): return ",".join(alias.name for alias in node.names)
        return f"{'.' * node.level}{node.module or ''}"
