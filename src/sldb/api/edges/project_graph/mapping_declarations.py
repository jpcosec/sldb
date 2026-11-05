"""References declared in a mapping (frontmatter or a YAML block) by the configured fields."""

from __future__ import annotations

from sldb.api.edges.project_graph.declaration import Declaration
from sldb.api.edges.project_graph.reference_field import ReferenceField


class MappingDeclarations:
    """Read every `ReferenceField` of a mapping into declarations."""

    def __init__(self, fields: tuple[ReferenceField, ...]) -> None:
        """Keep the fields, read in order."""
        self.fields = fields

    def __call__(self, mapping: dict, locator: str, skip_fields: frozenset[str] = frozenset()) -> list[Declaration]:
        """The declarations of `mapping`, located at `locator`.

        Args:
            mapping: The parsed mapping.
            locator: Where it sits (`frontmatter`, `line:N:yaml`).
            skip_fields: Top-level fields the store index owns for this document.

        Returns:
            Declarations in field order.
        """
        declarations: list[Declaration] = []
        for field in self.fields:
            if field.index_owned and field.path[0] in skip_fields:
                continue
            declarations.extend(_field_declarations(field, _dig(mapping, field.path), locator))
        return declarations


def _dig(mapping: dict, path: tuple[str, ...]) -> object:
    value: object = mapping
    for key in path:
        if not isinstance(value, dict):
            return None
        value = value.get(key)
    return value


def _field_declarations(field: ReferenceField, value: object, locator: str) -> list[Declaration]:
    if field.scalar_only:
        is_value = isinstance(value, str) and bool(value.strip())
        return [Declaration(field.target(value), field.default_role, locator)] if is_value else []
    if isinstance(value, str):
        return [Declaration(field.target(value), field.default_role, locator)]
    items = value if isinstance(value, list) else []
    return [declaration for item in items for declaration in _item_declarations(field, item, locator)]


def _item_declarations(field: ReferenceField, item: object, locator: str) -> list[Declaration]:
    if isinstance(item, str):
        return [Declaration(field.target(item), field.default_role, locator)]
    if isinstance(item, dict) and isinstance(item.get("id"), str):
        return [Declaration(field.target(item["id"]), field.role_of(item), locator)]
    return []
