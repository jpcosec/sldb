"""The edges and missing targets of one source, deduplicated as they are found."""

from __future__ import annotations

from sldb.api.edges.project_graph.missing_project_target import MissingProjectTarget
from sldb.api.edges.project_graph.project_edge import ProjectEdge


class SourceEdges:
    """Collect one source's edges and findings; the first of two equal keys is kept."""

    def __init__(self) -> None:
        """Start empty."""
        self.edges: list[ProjectEdge] = []
        self.missing: list[MissingProjectTarget] = []
        self._edge_keys: set[tuple[str, str, str, str]] = set()
        self._missing_keys: set[tuple[str, str, str]] = set()

    def add_edge(self, edge: ProjectEdge) -> None:
        """Keep an edge unless one with its key is kept."""
        if edge.key() not in self._edge_keys:
            self._edge_keys.add(edge.key())
            self.edges.append(edge)

    def add_missing(self, missing: MissingProjectTarget) -> None:
        """Keep a finding unless one with its key is kept."""
        if missing.key() not in self._missing_keys:
            self._missing_keys.add(missing.key())
            self.missing.append(missing)

    def names_target(self, source_id: str, target_id: str) -> bool:
        """Whether a finding from `source_id` to `target_id` is kept, at any locator."""
        return any(item.source_id == source_id and item.target_id == target_id for item in self.missing)

    def sorted(self) -> tuple[list[ProjectEdge], list[MissingProjectTarget]]:
        """Edges and findings, each sorted by its key."""
        return sorted(self.edges, key=ProjectEdge.key), sorted(self.missing, key=MissingProjectTarget.key)
