"""The project files (source, test, config, spec) that are graph nodes."""

from __future__ import annotations

from pathlib import Path

from sldb.api.edges.project_graph.declared_target_nodes import DeclaredTargetNodes
from sldb.api.edges.project_graph.document_nodes import surface_files
from sldb.api.edges.project_graph.file_node import FileNode
from sldb.api.edges.project_graph.node_provenance import NodeProvenance
from sldb.api.edges.project_graph.project_file_walk import ProjectFileWalk
from sldb.api.edges.project_graph.project_graph_config import ProjectGraphConfig


def extract_file_nodes(root: Path, config: ProjectGraphConfig, *, document_paths: set[str] | None = None) -> list[FileNode]:
    """Path-rule nodes plus declared-target nodes, sorted by node id.

    Args:
        root: The project root.
        config: The project's graph configuration.
        document_paths: Repo-relative paths of the document nodes, when the caller has them;
            otherwise the surfaces are globbed again.

    Returns:
        The file nodes.
    """
    project_root = root.resolve()
    walked = ProjectFileWalk(config.exclusions, config.file_rules)(project_root)
    nodes = [_rule_node(path, rule.kind, rule.file_kind, config.file_extractor) for path, rule in walked]
    if document_paths is None:
        document_paths = _document_paths(project_root, config)
    taken = {node.path for node in nodes} | document_paths
    nodes.extend(DeclaredTargetNodes(project_root, config.exclusions, config.file_extractor)(config.declared_file_targets, taken))
    return sorted(nodes, key=lambda node: node.id)


def _rule_node(path: str, kind: str, file_kind: str, extractor: str) -> FileNode:
    provenance = NodeProvenance(path=path, source_kind="path_rule", extractor=extractor)
    return FileNode(id=f"{kind}:{path}", kind=kind, identity=path, path=path, file_kind=file_kind, provenance=provenance)


def _document_paths(root: Path, config: ProjectGraphConfig) -> set[str]:
    return {path.relative_to(root).as_posix() for surface in config.surfaces for path in surface_files(root, surface)}
