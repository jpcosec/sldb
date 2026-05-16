"""
Scans Python source code using AST to extract semantics, code structure, and I/O.
It identifies modules, classes, and functions, generating corresponding KnowledgeNode objects.
"""

from __future__ import annotations

import ast
import fnmatch
import re
from dataclasses import dataclass
from pathlib import Path

from .contracts import (
    ASTFacet,
    ComplianceFacet,
    Edge,
    IOFacet,
    KnowledgeNode,
    SemanticFacet,
    SystemIdentity,
)
from wiki_compiler.adapters.ontology_facets import (
    infer_io_from_ast,
    scan_python_file,
    scan_python_sources,
)


IO_LINE_RE = re.compile(
    r"^(?:input|inputs|output|outputs|i/o):\s*(?P<medium>memory|disk|network)\s*\|\s*(?P<path>[^|]+?)\s*(?:\|\s*(?P<schema>.+))?$",
    re.IGNORECASE,
)


@dataclass(frozen=True)
class IgnoreRule:
    """Represents a rule for ignoring files during scanning, based on a glob pattern."""

    pattern: str
    reason: str | None

    def matches(self, path: str) -> bool:
        """Determines if the given path matches the ignore pattern."""
        if fnmatch.fnmatch(path, self.pattern):
            return True
        if fnmatch.fnmatch(path, f"{self.pattern}/**"):
            return True
        if self.pattern.startswith("**/"):
            # Extract the directory name without the **/ prefix and trailing /
            # e.g., "**/node_modules/" -> "node_modules"
            prefix = self.pattern[3:].rstrip("/")
            # Normalize path with surrounding slashes for easy contains check
            normalized = "/" + path + "/"
            # Check if path contains /{prefix}/ anywhere (e.g., /node_modules/ anywhere)
            if f"/{prefix}/" in normalized:
                return True
            # Also check if path ends with /{prefix} (at root level)
            if f"/{path}".endswith(f"/{prefix}"):
                return True
        if self.pattern.endswith("/"):
            prefix = self.pattern  # e.g., "src/looting/" from "src/looting/"
            return path.startswith(prefix) or path == prefix.rstrip("/")
        return False


from .protocols import ScannerPlugin


def scan_codebase(
    project_root: Path,
    source_roots: list[Path] | None = None,
    wikiignore_path: Path | None = None,
    plugins: list[ScannerPlugin] | None = None,
) -> list[KnowledgeNode]:
    """Recursively scans source directories for knowledge nodes using available scanner plugins."""
    roots = source_roots or [project_root / "src"]
    ignore_rules = load_wikiignore_rules(
        wikiignore_path or project_root / ".wikiignore"
    )

    # Use default plugins if none provided
    if plugins is None:
        plugins = [PythonScanner(), TypeScriptScanner()]

    nodes: list[KnowledgeNode] = []

    # Map extensions to plugins
    extension_map: dict[str, ScannerPlugin] = {}
    for plugin in plugins:
        for ext in plugin.supported_extensions:
            extension_map[ext] = plugin

    for root in roots:
        if not root.exists():
            continue
        for file_path in sorted(p for p in root.rglob("*") if p.is_file()):
            # Rule: Hidden files/directories are implicitly excluded (Not-Self)
            if any(part.startswith(".") for part in file_path.parts):
                continue

            rel_path = file_path.relative_to(project_root).as_posix()
            reason = match_ignore_reason(rel_path, ignore_rules)
            if reason is not None:
                nodes.append(build_ignored_file_node(rel_path, reason))
                continue

            plugin = extension_map.get(file_path.suffix)
            if plugin:
                nodes.extend(plugin.scan(file_path, project_root))

    return nodes


class PythonScanner:
    """Scanner plugin for Python source code."""

    @property
    def supported_extensions(self) -> set[str]:
        return {".py"}

    def scan(self, path: Path, project_root: Path) -> list[KnowledgeNode]:
        return scan_python_file(project_root, path)


class TypeScriptScanner:
    """Scanner plugin for TypeScript source code."""

    @property
    def supported_extensions(self) -> set[str]:
        return {".ts", ".tsx"}

    def scan(self, path: Path, project_root: Path) -> list[KnowledgeNode]:
        # For now, return a basic file node. Full extraction to be added.
        rel_path = path.relative_to(project_root).as_posix()
        return [
            KnowledgeNode(
                identity=SystemIdentity(node_id=f"file:{rel_path}", node_type="file"),
                semantics=SemanticFacet(
                    intent=f"TypeScript source file `{rel_path}`.", raw_docstring=None
                ),
                compliance=ComplianceFacet(status="implemented", failing_standards=[]),
            )
        ]


def scan_python_sources(
    project_root: Path,
    source_roots: list[Path] | None = None,
    wikiignore_path: Path | None = None,
) -> list[KnowledgeNode]:
    """Legacy wrapper for backward compatibility."""
    return scan_codebase(project_root, source_roots, wikiignore_path, [PythonScanner()])


def load_wikiignore_rules(wikiignore_path: Path) -> list[IgnoreRule]:
    """Reads and parses the .wikiignore file into a list of IgnoreRule objects."""
    if not wikiignore_path.exists():
        return []
    rules: list[IgnoreRule] = []
    for raw_line in wikiignore_path.read_text(encoding="utf-8").splitlines():
        line = raw_line.strip()
        if not line or line.startswith("#"):
            continue
        pattern, _, comment = line.partition(" #")
        rules.append(
            IgnoreRule(pattern=pattern.strip(), reason=comment.strip() or None)
        )
    return rules


def match_ignore_reason(path: str, rules: list[IgnoreRule]) -> str | None:
    """Returns the reason a path is ignored if it matches any of the provided rules."""
    reason: str | None = None
    for rule in rules:
        if rule.matches(path):
            reason = rule.reason or "Ignored by .wikiignore"
    return reason


def build_ignored_file_node(rel_path: str, reason: str) -> KnowledgeNode:
    """Creates a KnowledgeNode representing a file that has been explicitly ignored."""
    return KnowledgeNode(
        identity=SystemIdentity(node_id=f"file:{rel_path}", node_type="file"),
        semantics=SemanticFacet(
            intent=f"Ignored source file `{rel_path}`.", raw_docstring=None
        ),
        ast=ASTFacet(
            construct_type="script", signatures=[f"module {rel_path}"], dependencies=[]
        ),
        compliance=ComplianceFacet(
            status="exempt", exemption_reason=reason, failing_standards=[]
        ),
    )
