"""Find project graph nodes by path, id or name, and name the targets that have none."""

from __future__ import annotations

from pathlib import PurePosixPath

from sldb.api.edges.project_graph.document_node import DocumentNode
from sldb.api.edges.project_graph.file_node import FileNode
from sldb.api.edges.project_graph.missing_target_kind import MissingTargetKind

ProjectNode = DocumentNode | FileNode


class NodeLookup:
    """Every node of the project by path, by id and by bare name (id without kind, file stem)."""

    def __init__(self, nodes: list[ProjectNode], missing_kinds: tuple[MissingTargetKind, ...]) -> None:
        """Index the nodes; a later node on the same path or bare name wins, as the index order says.

        A portable reference names a document as sldb tracks it, by its file stem; a document
        with a shorter declared id resolves by its stem too (set only where no id claims it).
        """
        self.by_path = {node.path: node for node in nodes}
        self.existing_ids = {node.id for node in nodes}
        self.ids_by_name = {node.id.split(":", 1)[-1]: node.id for node in nodes}
        for node in nodes:
            self.ids_by_name.setdefault(PurePosixPath(node.path).stem, node.id)
        self.by_id = {node.id: node for node in self.by_path.values()}
        self.missing_kinds = missing_kinds

    def reference_id(self, value: str) -> str | None:
        """The node id a declared value names (id, bare name, path, stem or `kind:id`), or None."""
        candidate = value.strip()
        if any(ch.isspace() for ch in candidate):
            return None  # prose, not a reference
        if candidate in self.ids_by_name:
            return self.ids_by_name[candidate]
        node = self.by_path.get(candidate.removeprefix("./"))
        if node is not None:
            return node.id
        stem = PurePosixPath(candidate).stem
        return self.ids_by_name.get(stem) or (candidate if ":" in candidate else None)

    def looks_like_reference(self, value: str) -> bool:
        """Whether a declared value means to name a node; prose (any whitespace) never does."""
        candidate = value.strip()
        if any(ch.isspace() for ch in candidate):
            return False
        if "/" in candidate or ":" in candidate:
            return True
        return PurePosixPath(candidate).stem in self.ids_by_name or candidate in self.by_path

    def target_id(self, target: str) -> str:
        """The id a declared target stands for: `kind:id` as is, a node's path as its id, else a missing id."""
        if ":" in target:
            return target
        node = self.by_path.get(target.removeprefix("./"))
        return node.id if node is not None else self.missing_target_id(target)

    def missing_target_id(self, target: str) -> str:
        """The id a path that is no node would have, by the configured kinds; else the path."""
        if ":" in target:
            return target
        path = target.removeprefix("./")
        parts = PurePosixPath(path).parts
        kind = next((rule.kind for rule in self.missing_kinds if rule.matches(parts, path)), None)
        return f"{kind}:{path}" if kind else path
