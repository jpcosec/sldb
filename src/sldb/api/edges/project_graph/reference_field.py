"""A mapping field (frontmatter or a YAML block) whose values name graph nodes."""

from __future__ import annotations

from pydantic import BaseModel, ConfigDict, Field


class ReferenceField(BaseModel):
    """Where references sit in a mapping and how a value becomes a target id."""

    model_config = ConfigDict(frozen=True)

    path: tuple[str, ...] = Field(description="Keys from the mapping's top to the field (`contract`, `sources`).")
    target_prefix: str = Field(default="", description="Prefix a value gets unless it already starts with it (`topic:`).")
    default_role: str = Field(description="Edge role of a value that names no role of its own.")
    allowed_roles: tuple[str, ...] = Field(default=(), description="Roles an `{id, role}` item may name; any other falls back to the default.")
    scalar_only: bool = Field(default=False, description="Only a non-blank string value counts; lists are not read.")
    index_owned: bool = Field(default=False, description="The sldb index owns this field when the document's model declares it.")

    def target(self, value: str) -> str:
        """The target id a declared value names."""
        value = value.strip()
        return value if not self.target_prefix or value.startswith(self.target_prefix) else f"{self.target_prefix}{value}"

    def role_of(self, item: dict) -> str:
        """The role an `{id, role}` item declares, or the default when it names none it may."""
        role = item.get("role")
        return role if isinstance(role, str) and role in self.allowed_roles else self.default_role
