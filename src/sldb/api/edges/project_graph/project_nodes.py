"""Every node of a project graph: its documents and its files."""

from __future__ import annotations

from pathlib import Path

from sldb.api.edges.project_graph.document_node import DocumentNode
from sldb.api.edges.project_graph.document_nodes import extract_document_nodes
from sldb.api.edges.project_graph.file_nodes import extract_file_nodes
from sldb.api.edges.project_graph.node_lookup import NodeLookup
from sldb.api.edges.project_graph.project_graph_config import ProjectGraphConfig


class ProjectNodes:
    """Documents and files read once, and the lookup that resolves references to them."""

    def __init__(self, root: Path, config: ProjectGraphConfig) -> None:
        """Read the document surfaces, then the files (documents are never file nodes).

        Args:
            root: The (resolved) project root.
            config: The project's graph configuration.
        """
        self.documents = extract_document_nodes(root, config)
        self.files = extract_file_nodes(root, config, document_paths={node.path for node in self.documents})
        self.lookup = NodeLookup([*self.documents, *self.files], config.missing_target_kinds)
        self.documents_by_id: dict[str, list[DocumentNode]] = {}
        for node in self.documents:
            self.documents_by_id.setdefault(node.id, []).append(node)
