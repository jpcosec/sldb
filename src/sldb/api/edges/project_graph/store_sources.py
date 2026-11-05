"""The store index's edges and unresolved values, grouped by the project node declaring them."""

from __future__ import annotations

from sldb.api.edges.project_graph.missing_project_target import MissingProjectTarget
from sldb.api.edges.project_graph.node_lookup import NodeLookup, ProjectNode
from sldb.api.edges.project_graph.project_edge import ProjectEdge
from sldb.api.edges.project_graph.project_graph_config import ProjectGraphConfig
from sldb.api.edges.project_graph.project_store import ProjectStore
from sldb.api.edges.project_graph.project_texts import ProjectTexts
from sldb.api.edges.project_graph.source_edges import SourceEdges
from sldb.api.edges.project_graph.store_edges import store_edges
from sldb.api.edges.project_graph.store_unresolved import store_unresolved
from sldb.store.edge_index.unresolved_reference import UnresolvedReference

Unresolved = tuple[UnresolvedReference, str, ProjectNode]


class StoreSources:
    """Project the store index once, on first use, and hand each source its part."""

    def __init__(self, store: ProjectStore | None, lookup: NodeLookup, texts: ProjectTexts, config: ProjectGraphConfig) -> None:
        """Keep the store (None for a project without one) and what projecting needs."""
        self.store = store
        self.lookup = lookup
        self.texts = texts
        self.config = config
        self._edges: dict[str, list[ProjectEdge]] | None = None
        self._unresolved: dict[str, list[Unresolved]] | None = None

    def edges_by_source(self) -> dict[str, list[ProjectEdge]]:
        """Index edges grouped by source id, in index order."""
        if self._edges is None:
            edges = store_edges(self.store, self.lookup, self.texts.is_record_path, self.config.edge_extractor) if self.store else []
            self._edges = {}
            for edge in edges:
                self._edges.setdefault(edge.source_id, []).append(edge)
        return self._edges

    def unresolved_by_source(self) -> dict[str, list[Unresolved]]:
        """Dangling index values grouped by declaring node id, in index order."""
        if self._unresolved is None:
            found = store_unresolved(self.store, self.lookup, self.config.provenance_fields) if self.store else []
            self._unresolved = {}
            for item in found:
                self._unresolved.setdefault(item[2].id, []).append(item)
        return self._unresolved

    def add_unresolved(self, node_id: str, found: SourceEdges) -> None:
        """Add the source's dangling index values unless its documents already reported that target."""
        for reference, value, node in self.unresolved_by_source().get(node_id, []):
            missing = self._missing(reference, value, node)
            if not found.names_target(missing.source_id, missing.target_id):
                found.add_missing(missing)

    def _missing(self, reference: UnresolvedReference, value: str, node: ProjectNode) -> MissingProjectTarget:
        reason = f"declared target was not resolved by the sldb edge index ({reference.reason})"
        return MissingProjectTarget(
            source_id=node.id, target_id=self._target_id(reference, value), provenance_path=node.path, provenance_locator="frontmatter",
            reason=reason, extractor=self.config.edge_extractor, record=self.texts.history_at(node.kind, node.path),
        )

    def _target_id(self, reference: UnresolvedReference, value: str) -> str:
        """The configured kind of the missing document's model (`kind:name`), else the export id or the value's id."""
        if not reference.target_export_id:
            return self.lookup.target_id(value)
        model, _, name = reference.target_export_id.partition(":")
        kind = self.config.kind_by_model.get(model)
        return f"{kind}:{name}" if kind and name else reference.target_export_id
