"""What a project's graph is made of: the configuration a `ProjectGraph` reads.

sldb owns the reading (documents, files, the store's edge index, declarations); the project
owns this configuration: where its documents live, which files are nodes, which fields and
sections declare references, and which documents are archived records.
"""

from __future__ import annotations

from typing import Callable

from pydantic import BaseModel, ConfigDict, Field

from sldb.api.edges.project_graph.declared_file_targets import DeclaredFileTargets
from sldb.api.edges.project_graph.document_surface import DocumentSurface
from sldb.api.edges.project_graph.file_exclusions import FileExclusions
from sldb.api.edges.project_graph.file_rule import FileRule
from sldb.api.edges.project_graph.line_mentions import LineMentions
from sldb.api.edges.project_graph.missing_target_kind import MissingTargetKind
from sldb.api.edges.project_graph.reference_field import ReferenceField
from sldb.api.edges.project_graph.section_mentions import SectionMentions


class ProjectGraphConfig(BaseModel):
    """The project-specific half of a project graph."""

    model_config = ConfigDict(frozen=True)

    document_extractor: str = Field(description="Provenance `extractor` of document nodes.")
    file_extractor: str = Field(description="Provenance `extractor` of file nodes.")
    edge_extractor: str = Field(description="`extractor` of declared edges and missing targets.")
    surfaces: tuple[DocumentSurface, ...] = Field(description="Document surfaces, in the order their nodes are read.")
    file_rules: tuple[FileRule, ...] = Field(default=(), description="Ordered rules classifying project files.")
    exclusions: FileExclusions = Field(default_factory=FileExclusions, description="What the file walk never reads.")
    declared_file_targets: tuple[DeclaredFileTargets, ...] = Field(default=(), description="Frontmatter fields naming files that must be nodes.")
    reference_fields: tuple[ReferenceField, ...] = Field(default=(), description="Mapping fields (frontmatter, YAML blocks) holding references.")
    read_yaml_blocks: bool = Field(default=True, description="Also read `reference_fields` in fenced YAML blocks of the body.")
    fields_by_kind: dict[str, tuple[str, ...]] = Field(default_factory=dict, description="Model-declared reference fields of each node kind, read from frontmatter.")
    fields_by_model: dict[str, tuple[str, ...]] = Field(default_factory=dict, description="Fields whose edges the store index owns, per tracked model.")
    kind_by_model: dict[str, str] = Field(default_factory=dict, description="Node kind of each model, naming the targets the index leaves unresolved.")
    provenance_fields: tuple[str, ...] = Field(default=(), description="Fields recording where a document came from: they link while the source exists and are never missing.")
    section_mentions: tuple[SectionMentions, ...] = Field(default=(), description="Mentions read under headings.")
    line_mentions: tuple[LineMentions, ...] = Field(default=(), description="Mentions read on every line.")
    missing_target_kinds: tuple[MissingTargetKind, ...] = Field(default=(), description="Kinds of dangling path targets.")
    closed_document: Callable[[str, str], bool] | None = Field(
        default=None,
        description="(kind, text) -> whether a document is history besides `record: true` (a closed issue).",
    )

