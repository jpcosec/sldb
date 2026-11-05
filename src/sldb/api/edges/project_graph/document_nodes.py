"""The documents of a project as graph nodes, read from its document surfaces."""

from __future__ import annotations

import re
from pathlib import Path

from sldb.api.edges.project_graph.document_metadata import document_metadata
from sldb.api.edges.project_graph.document_node import DocumentNode
from sldb.api.edges.project_graph.document_surface import DocumentSurface
from sldb.api.edges.project_graph.node_provenance import NodeProvenance
from sldb.api.edges.project_graph.project_graph_config import ProjectGraphConfig


def extract_document_nodes(root: Path, config: ProjectGraphConfig) -> list[DocumentNode]:
    """Every file of every surface as a node, sorted by node id.

    Args:
        root: The project root.
        config: The project's graph configuration.

    Returns:
        One node per surface file; a file on two surfaces is two nodes.
    """
    project_root = root.resolve()
    nodes = [
        _document_node(project_root, path, surface, config.document_extractor)
        for surface in config.surfaces
        for path in surface_files(project_root, surface)
    ]
    return sorted(nodes, key=lambda node: node.id)


def surface_files(root: Path, surface: DocumentSurface) -> list[Path]:
    """The files of one surface, sorted by path."""
    directory = root / surface.directory if surface.directory else root
    if not directory.exists():
        return []
    found = sorted(path for path in directory.glob(surface.pattern) if path.is_file())
    return [path for path in found if surface.keeps(path.relative_to(directory).parts, path.name, path.suffix)]


def _document_node(root: Path, path: Path, surface: DocumentSurface, extractor: str) -> DocumentNode:
    relative_path = path.relative_to(root).as_posix()
    metadata = document_metadata(path)
    document_id = metadata.get("id")
    label = metadata.get("title") or re.sub(r"[-_]+", " ", path.stem).strip().title()
    identity = _identity(surface, relative_path, document_id, label, path)
    provenance = NodeProvenance(path=relative_path, source_kind="file_metadata", extractor=extractor)
    return DocumentNode(
        id=f"{surface.kind}:{identity}", kind=surface.kind, identity=identity, path=relative_path,
        label=label, provenance=provenance, document_id=document_id,
    )


def _identity(surface: DocumentSurface, relative_path: str, document_id: str | None, label: str, path: Path) -> str:
    if surface.identity == "document_id":
        return document_id or relative_path
    if surface.identity == "document_id_or_slug":
        return document_id or _slugify(label) or path.stem
    return relative_path


def _slugify(value: str) -> str:
    slug = re.sub(r"[^a-z0-9]+", "-", value.lower()).strip("-")
    return re.sub(r"-+", "-", slug)
