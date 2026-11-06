"""A project's declared-edge graph, read one source at a time from the store index and the files."""

from __future__ import annotations

from pathlib import Path

from sldb.api.edges.project_graph.document_edge_reader import DocumentEdgeReader
from sldb.api.edges.project_graph.inverse_edges import InverseEdges
from sldb.api.edges.project_graph.missing_project_target import MissingProjectTarget
from sldb.api.edges.project_graph.project_edge import ProjectEdge
from sldb.api.edges.project_graph.project_graph_config import ProjectGraphConfig
from sldb.api.edges.project_graph.project_graph_extraction import ProjectGraphExtraction
from sldb.api.edges.project_graph.project_nodes import ProjectNodes
from sldb.api.edges.project_graph.project_store import load_project_store
from sldb.api.edges.project_graph.project_texts import ProjectTexts, indexed_payloads
from sldb.api.edges.project_graph.source_edges import SourceEdges
from sldb.api.edges.project_graph.store_sources import StoreSources


class ProjectGraph:
    """Nodes are read once; the edges a source declares are read when that source is asked for.

    The store's own edge index (cached by sldb while its shards do not move) gives the schema
    edges of tracked documents and the values it could not resolve; each document's text gives
    what its model does not declare (configured fields, YAML blocks, sections, mentions). A
    reader that needs a few sources reads those documents, not all of them. The edges reaching
    a node come from one inverse map, built from every source the first time it is asked.
    """

    def __init__(self, root: Path, config: ProjectGraphConfig) -> None:
        """Read the nodes and open the store.

        Args:
            root: The project root.
            config: The project's graph configuration.
        """
        self.root = root.resolve()
        self.config = config
        self.nodes = ProjectNodes(self.root, config)
        self.store = load_project_store(self.root, [node.path for node in self.nodes.documents])
        self.texts = ProjectTexts(self.root, config, indexed_payloads(self.store.index) if self.store else None)
        self.store_sources = StoreSources(self.store, self.nodes.lookup, self.texts, config)
        self._document_reader = DocumentEdgeReader(config, self.nodes, self.store, self.texts)
        self._read: dict[str, tuple[list[ProjectEdge], list[MissingProjectTarget]]] = {}
        self._extraction: ProjectGraphExtraction | None = None
        self._inverse: InverseEdges | None = None

    def node_ids(self) -> set[str]:
        """Every id that may be the source of an edge or of a missing target."""
        return {*self.nodes.documents_by_id, *self.store_sources.edges_by_source(), *self.store_sources.unresolved_by_source()}

    def edges_from(self, node_id: str) -> list[ProjectEdge]:
        """The declared edges leaving `node_id`, sorted by key."""
        return self._read_source(node_id)[0]

    def missing_from(self, node_id: str) -> list[MissingProjectTarget]:
        """The declared targets of `node_id` that resolve to no node, sorted by key."""
        return self._read_source(node_id)[1]

    def edges_to(self, node_id: str) -> list[ProjectEdge]:
        """The declared edges reaching `node_id`, the same records `edges_from` gives, sorted by key."""
        if self._inverse is None:
            self._inverse = InverseEdges(self.extraction())
        return self._inverse.edges_to(node_id)

    def extraction(self) -> ProjectGraphExtraction:
        """Every source read (once): all edges and findings, each sorted by key."""
        if self._extraction is None:
            edges: list[ProjectEdge] = []
            missing: list[MissingProjectTarget] = []
            for node_id in sorted(self.node_ids()):
                edges.extend(self.edges_from(node_id))
                missing.extend(self.missing_from(node_id))
            self._extraction = ProjectGraphExtraction(edges=sorted(edges, key=ProjectEdge.key), missing_targets=sorted(missing, key=MissingProjectTarget.key))
        return self._extraction

    def _read_source(self, node_id: str) -> tuple[list[ProjectEdge], list[MissingProjectTarget]]:
        """Index edges first, then each document with that id, then the index's unresolved values.

        Every deduplication key starts with the source id, so one source read alone gives
        what reading the whole graph gives for it.
        """
        if node_id not in self._read:
            found = SourceEdges()
            for edge in self.store_sources.edges_by_source().get(node_id, []):
                found.add_edge(edge)
            for node in self.nodes.documents_by_id.get(node_id, []):
                self._document_reader(node, found)
            self.store_sources.add_unresolved(node_id, found)
            self._read[node_id] = found.sorted()
        return self._read[node_id]
