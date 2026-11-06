"""What a project's graph is made of: the configuration a `ProjectGraph` reads.

sldb owns the reading (documents, files, the store's edge index, declarations); the project
owns this configuration: where its documents live, which files are nodes, which fields and
sections declare references, and which documents are archived records. It is plain data:
`from_mapping` loads it from (and `to_mapping` dumps it to) the mapping a `store.yaml`
declares under `project_graph`.
"""

from __future__ import annotations

import warnings
from typing import Any, Callable

from pydantic import BaseModel, ConfigDict, Field, model_validator

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
        default=None, exclude=True,
        description="Deprecated: `(kind, text) -> closed`, a Python-only argument that never loads or dumps; declare `closed:` on the surface instead.",
    )

    @model_validator(mode="after")
    def _closed_document_is_deprecated(self) -> ProjectGraphConfig:
        if self.closed_document is not None:
            warnings.warn("ProjectGraphConfig(closed_document=...) is deprecated: declare `closed:` on the document surface", DeprecationWarning, stacklevel=2)
        return self

    @classmethod
    def from_mapping(cls, mapping: Any, path: str = "project_graph") -> ProjectGraphConfig:
        """The configuration a plain mapping (what `store.yaml` holds under `project_graph`) declares.

        Args:
            mapping: Scalars, lists and mappings only, keyed by the field names.
            path: Where the mapping sits, prefixed to the key an error names.

        Raises:
            ValueError: An unknown key or a value that is not data, naming the key's path
                (`project_graph.surfaces[0].closed_document`); a value of the wrong type.
        """
        from sldb.api.edges.project_graph.project_graph_config_mapping import config_from_mapping

        return config_from_mapping(mapping, path)

    def to_mapping(self) -> dict[str, Any]:
        """The configuration as plain data: `from_mapping` of it is an equal configuration.

        Raises:
            ValueError: `closed_document` is set; a callable is not data.
        """
        from sldb.api.edges.project_graph.project_graph_config_mapping import config_to_mapping

        return config_to_mapping(self)

