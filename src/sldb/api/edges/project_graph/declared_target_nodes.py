"""Files that documents declare in a frontmatter field, made nodes so references resolve."""

from __future__ import annotations

from pathlib import Path, PurePosixPath

from sldb.api.edges.project_graph.declared_file_targets import DeclaredFileTargets
from sldb.api.edges.project_graph.file_exclusions import FileExclusions
from sldb.api.edges.project_graph.file_node import FileNode
from sldb.api.edges.project_graph.frontmatter_mapping import frontmatter_mapping
from sldb.api.edges.project_graph.node_provenance import NodeProvenance


class DeclaredTargetNodes:
    """File nodes for declared targets no path rule made a node and no surface holds."""

    def __init__(self, root: Path, exclusions: FileExclusions, extractor: str) -> None:
        """Keep the (resolved) project root, the exclusions and the extractor name."""
        self.root = root
        self.exclusions = exclusions
        self.extractor = extractor

    def __call__(self, declarations: tuple[DeclaredFileTargets, ...], taken: set[str]) -> list[FileNode]:
        """One node per new declared file, in declaring-document order.

        Args:
            declarations: The declaring fields to read.
            taken: Paths that are already nodes or documents; grows with every node made.

        Returns:
            The new nodes.
        """
        nodes: list[FileNode] = []
        for declaration in declarations:
            for path in self._declaring_documents(declaration):
                target = self._declared_path(path, declaration.field)
                if target is not None and target not in taken:
                    taken.add(target)
                    nodes.append(self._node(target, declaration))
        return nodes

    def _declaring_documents(self, declaration: DeclaredFileTargets) -> list[Path]:
        directory = self.root / declaration.directory
        return sorted(path for path in directory.rglob(declaration.pattern) if path.is_file()) if directory.exists() else []

    def _declared_path(self, document: Path, field: str) -> str | None:
        """The declared repo-relative file, when it is a plain path to an existing project file."""
        value = _field_value(document, field)
        normalized = value.removeprefix("./") if value else ""
        if not normalized or normalized.startswith("/") or ".." in PurePosixPath(normalized).parts or ":" in normalized:
            return None
        if not (self.root / normalized).resolve().is_relative_to(self.root) or not (self.root / normalized).is_file():
            return None
        return None if self.exclusions.excludes(PurePosixPath(normalized).as_posix()) else normalized

    def _node(self, path: str, declaration: DeclaredFileTargets) -> FileNode:
        provenance = NodeProvenance(path=path, source_kind=declaration.source_kind, extractor=self.extractor)
        return FileNode(id=f"{declaration.kind}:{path}", kind=declaration.kind, identity=path, path=path, file_kind=declaration.file_kind, provenance=provenance)


def _field_value(document: Path, field: str) -> str | None:
    try:
        text = document.read_text(encoding="utf-8")
    except (OSError, UnicodeDecodeError):
        return None
    value = (frontmatter_mapping(text) or {}).get(field)
    return value.strip() if isinstance(value, str) and value.strip() else None
