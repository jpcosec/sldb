"""The declared edges of a project grouped by the node they reach."""

from __future__ import annotations

from sldb.api.edges.project_graph.project_edge import ProjectEdge
from sldb.api.edges.project_graph.project_graph_extraction import ProjectGraphExtraction


class InverseEdges:
    """One inverse map for every edge type, built once from the whole extraction.

    The extraction's edges are sorted by key (source, target, role, locator), so the edges
    of one target keep that order among themselves.
    """

    def __init__(self, extraction: ProjectGraphExtraction) -> None:
        """Group the extraction's edges by target id."""
        self.by_target: dict[str, list[ProjectEdge]] = {}
        for edge in extraction.edges:
            self.by_target.setdefault(edge.target_id, []).append(edge)

    def edges_to(self, node_id: str) -> list[ProjectEdge]:
        """The edges reaching `node_id`, sorted by key; empty for a node nothing names."""
        return list(self.by_target.get(node_id, []))
