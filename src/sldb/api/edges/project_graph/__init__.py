"""The declared-edge graph of a project, read from its sldb store and its files.

A project (a desk, a repository) configures where its documents live, which files are nodes
and which fields and sections declare references (`ProjectGraphConfig`); `ProjectGraph`
reads the nodes once, the store's cached edge index for tracked documents, and the text of
only the documents a reader asks about. `project_graph(store)` is the graph of the project
whose `store.yaml` declares the configuration under `project_graph`, kept per process.
"""

from sldb.api.edges.project_graph.declared_file_targets import DeclaredFileTargets
from sldb.api.edges.project_graph.document_node import DocumentNode
from sldb.api.edges.project_graph.document_nodes import extract_document_nodes
from sldb.api.edges.project_graph.document_surface import DocumentSurface
from sldb.api.edges.project_graph.file_exclusions import FileExclusions
from sldb.api.edges.project_graph.file_node import FileNode
from sldb.api.edges.project_graph.file_nodes import extract_file_nodes
from sldb.api.edges.project_graph.file_rule import FileRule
from sldb.api.edges.project_graph.line_mentions import LineMentions
from sldb.api.edges.project_graph.mention_pattern import MentionPattern
from sldb.api.edges.project_graph.missing_project_target import MissingProjectTarget
from sldb.api.edges.project_graph.missing_target_kind import MissingTargetKind
from sldb.api.edges.project_graph.node_provenance import NodeProvenance
from sldb.api.edges.project_graph.project_edge import ProjectEdge
from sldb.api.edges.project_graph.project_graph import ProjectGraph
from sldb.api.edges.project_graph.project_graph_config import ProjectGraphConfig
from sldb.api.edges.project_graph.project_graph_extraction import ProjectGraphExtraction
from sldb.api.edges.project_graph.reference_field import ReferenceField
from sldb.api.edges.project_graph.section_mentions import SectionMentions
from sldb.api.edges.project_graph.store_project_graph import project_graph

__all__ = [
    "DeclaredFileTargets", "DocumentNode", "DocumentSurface", "FileExclusions", "FileNode", "FileRule",
    "LineMentions", "MentionPattern", "MissingProjectTarget", "MissingTargetKind", "NodeProvenance",
    "ProjectEdge", "ProjectGraph", "ProjectGraphConfig", "ProjectGraphExtraction", "ReferenceField",
    "SectionMentions", "extract_document_nodes", "extract_file_nodes", "project_graph",
]
