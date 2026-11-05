"""Everything one project document declares, in the order the reader resolves it."""

from __future__ import annotations

from sldb.api.edges.project_graph.declaration import Declaration
from sldb.api.edges.project_graph.frontmatter_mapping import frontmatter_mapping
from sldb.api.edges.project_graph.mapping_declarations import MappingDeclarations
from sldb.api.edges.project_graph.node_lookup import NodeLookup
from sldb.api.edges.project_graph.path_text import has_path_prefix
from sldb.api.edges.project_graph.project_graph_config import ProjectGraphConfig
from sldb.api.edges.project_graph.text_declarations import line_declarations, section_declarations, yaml_block_declarations


class DocumentDeclarations:
    """Frontmatter fields, model fields of the kind, YAML blocks, sections, then line mentions."""

    def __init__(self, config: ProjectGraphConfig, lookup: NodeLookup) -> None:
        """Keep the configuration and the node lookup that resolves model-field values."""
        self.config = config
        self.lookup = lookup
        self.mapping = MappingDeclarations(config.reference_fields)

    def __call__(self, kind: str, path: str, text: str, skip_fields: frozenset[str]) -> list[Declaration]:
        """The declarations of one document.

        Args:
            kind: The document's node kind.
            path: Its repo-relative path.
            text: Its text.
            skip_fields: Fields the store index owns for it (its tracked model declares them).

        Returns:
            Declarations, not yet resolved.
        """
        declarations = self._frontmatter(kind, text, skip_fields)
        if self.config.read_yaml_blocks:
            declarations.extend(yaml_block_declarations(text, self.mapping))
        return declarations + self._mentions(kind, path, text.splitlines())

    def _mentions(self, kind: str, path: str, lines: list[str]) -> list[Declaration]:
        """Section mentions, then line mentions, of the rules that read this document."""
        declarations: list[Declaration] = []
        for rule in self.config.section_mentions:
            if not rule.kinds or kind in rule.kinds:
                declarations.extend(section_declarations(lines, rule))
        for rule in self.config.line_mentions:
            if kind in rule.kinds and not any(has_path_prefix(path, prefix) for prefix in rule.excluded_path_prefixes):
                declarations.extend(line_declarations(lines, rule))
        return declarations

    def _frontmatter(self, kind: str, text: str, skip_fields: frozenset[str]) -> list[Declaration]:
        mapping = frontmatter_mapping(text)
        if mapping is None:
            return []
        declarations = self.mapping(mapping, "frontmatter", skip_fields)
        for field in self.config.fields_by_kind.get(kind, ()):
            if field not in skip_fields and field in mapping:
                declarations.extend(self._model_field(field, mapping[field]))
        return declarations

    def _model_field(self, field: str, value: object) -> list[Declaration]:
        declarations: list[Declaration] = []
        for item in value if isinstance(value, list) else [value]:
            target = self._model_field_target(field, item) if isinstance(item, str) and item.strip() else None
            if target is not None:
                declarations.append(Declaration(target, field, "frontmatter"))
        return declarations

    def _model_field_target(self, field: str, item: str) -> str | None:
        """A provenance value links only while its source is a node; any other value resolves or stays raw."""
        if field in self.config.provenance_fields:
            node = self.lookup.by_path.get(item.strip().removeprefix("./"))
            return node.id if node is not None else None
        reference = self.lookup.reference_id(item)
        if reference is not None:
            return reference
        return item.strip() if self.lookup.looks_like_reference(item) else None
