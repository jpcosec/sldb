"""Small pure helpers for static Python source facts."""
from __future__ import annotations

import ast
import hashlib

import yaml


def source_hash(text: str) -> str:
    """Return the containing file's content hash."""
    return hashlib.sha256(text.encode()).hexdigest()


def frontmatter(node: ast.AST) -> dict:
    """Read only valid leading YAML metadata from one docstring."""
    docstring = ast.get_docstring(node, clean=True) or ""
    if not docstring.startswith("---\n"):
        return {}
    _, separator, remainder = docstring.partition("\n---")
    if not separator:
        return {}
    payload = yaml.safe_load(docstring[4:len(docstring) - len(remainder) - 4])
    return payload if isinstance(payload, dict) else {}


def declared_id(node: ast.AST, fallback: str) -> str:
    """Prefer a declared source identity over the legacy fallback."""
    value = frontmatter(node).get("id")
    return value if isinstance(value, str) and value else fallback


def annotation_names(node: ast.AST) -> list[str]:
    """Return lexical names used by one annotation expression."""
    return sorted({item.id for item in ast.walk(node) if isinstance(item, ast.Name)})


def module_name(path, root, package: str | None) -> str:
    """Match the current scanner's qualified module naming behavior."""
    parts = list(path.relative_to(root).with_suffix("").parts)
    if parts[-1] == "__init__":
        parts.pop()
    return ".".join(([package] if package else []) + parts)


def relative_module(module: str, requested: str | None, level: int) -> str:
    """Resolve an ImportFrom module spelling against its importer's package."""
    if not level:
        return requested or ""
    package = module.split(".")[:-1]
    base = package[:len(package) - level + 1]
    return ".".join([*base, *(requested or "").split(".")]).strip(".")
