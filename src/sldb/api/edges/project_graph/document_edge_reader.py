"""Resolve one document's declarations into edges and missing targets."""

from __future__ import annotations

from sldb.api.edges.project_graph.declaration import Declaration
from sldb.api.edges.project_graph.document_declarations import DocumentDeclarations
from sldb.api.edges.project_graph.document_node import DocumentNode
from sldb.api.edges.project_graph.missing_project_target import MissingProjectTarget
from sldb.api.edges.project_graph.project_edge import ProjectEdge
from sldb.api.edges.project_graph.project_graph_config import ProjectGraphConfig
from sldb.api.edges.project_graph.project_nodes import ProjectNodes
from sldb.api.edges.project_graph.project_store import ProjectStore
from sldb.api.edges.project_graph.project_texts import ProjectTexts
from sldb.api.edges.project_graph.source_edges import SourceEdges

MISSING_REASON = "declared target was not found among extracted graph nodes"


class DocumentEdgeReader:
    """Read a Markdown document's own declarations; the store index owns its model's fields."""

    def __init__(self, config: ProjectGraphConfig, nodes: ProjectNodes, store: ProjectStore | None, texts: ProjectTexts) -> None:
        """Keep what resolving needs: configuration, nodes, store and texts."""
        self.config = config
        self.nodes = nodes
        self.store = store
        self.texts = texts
        self.declarations = DocumentDeclarations(config, nodes.lookup)

    def __call__(self, node: DocumentNode, found: SourceEdges) -> None:
        """Add the document's edges and missing targets to `found`; a non-Markdown file declares nothing."""
        path = self.texts.root / node.path
        if path.suffix != ".md" or not path.exists():
            return
        text = self.texts.text(node.path)
        record = self.texts.is_history(node.kind, text)
        for declaration in self.declarations(node.kind, node.path, text, self._index_owned(node.path)):
            self._resolve(node, declaration, record, found)

    def _resolve(self, node: DocumentNode, declaration: Declaration, record: bool | None, found: SourceEdges) -> None:
        """An edge when the target is a node, a missing target otherwise."""
        target_id = self.nodes.lookup.target_id(declaration.target)
        if target_id not in self.nodes.lookup.existing_ids:
            found.add_missing(MissingProjectTarget(source_id=node.id, target_id=target_id, provenance_path=node.path, provenance_locator=declaration.locator, reason=MISSING_REASON, extractor=self.config.edge_extractor, record=record))
        else:
            found.add_edge(ProjectEdge(source_id=node.id, target_id=target_id, role=declaration.role, provenance_path=node.path, provenance_locator=declaration.locator, extractor=self.config.edge_extractor, record=record))

    def _index_owned(self, path: str) -> frozenset[str]:
        """The fields the tracked model of the document declares (the index reads those)."""
        tracked = self.store.tracked.get(path) if self.store is not None else None
        return frozenset(self.config.fields_by_model.get(tracked.model, ())) if tracked and tracked.model else frozenset()
