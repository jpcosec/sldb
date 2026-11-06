"""One section of a composed `ViewDoc` (GD25): which documents, which fields, and what each row carries."""

from __future__ import annotations

from typing import Any

from pydantic import BaseModel, ConfigDict, Field, field_validator

from sldb.models.notation.view_section_parts import ViewEdge, normalize_names, normalize_transitions


class ViewSection(BaseModel):
    """`select` chooses the rows (a selector of `select_documents`, `{param}` allowed in its
    values); `fields` says which projected fields each row shows (`*` = all); `edges`, `rules`
    and `transitions` add neighbours, findings and the holding and blocked edges; `group_by`
    groups the rows, in the order of `group_order`."""

    model_config = ConfigDict(extra="forbid")

    key: str = Field(description="The section's key in the result; unique within the view.")
    select: dict[str, Any] = Field(description="Selector keys (`ref`, `prefix`, `path_glob`, `model`, `where`, `include_linked`); `{param}` in a value is filled when the view runs.")
    fields: list[str] = Field(default_factory=lambda: ["*"], description="Projected fields each row returns; `*` = every projected field.")
    edges: list[ViewEdge] = Field(default_factory=list, description="Neighbour ids to add to each row, one key per entry.")
    group_by: str = Field(default="", description="Field the rows are grouped by; empty = no groups.")
    group_order: list[str] = Field(default_factory=list, description="Order of the groups' values; other values follow, sorted.")
    rules: list[str] = Field(default_factory=list, description="Names of RuleDocs evaluated on each row (`findings`).")
    transitions: dict[str, str] | None = Field(default=None, description="`{from_field, relation}`: the holding and blocked edges leaving the node `from_field` names.")

    @field_validator("key", "group_by")
    @classmethod
    def _stripped(cls, value: str, info) -> str:
        if info.field_name == "key" and not value.strip():
            raise ValueError("a section needs a key")
        return value.strip()

    @field_validator("select", mode="before")
    @classmethod
    def _select(cls, value: Any) -> dict[str, Any]:
        if not isinstance(value, dict) or not value:
            raise ValueError(f"select must be a non-empty selector mapping, got {value!r}")
        return value

    @field_validator("fields", "rules", "group_order", mode="before")
    @classmethod
    def _names(cls, value: Any, info) -> list[str]:
        if value is None and info.field_name == "fields":
            return ["*"]
        return normalize_names(value, info.field_name)

    @field_validator("edges", mode="before")
    @classmethod
    def _edges(cls, value: Any) -> list:
        return [] if value is None else value

    @field_validator("transitions", mode="before")
    @classmethod
    def _transitions(cls, value: Any) -> dict[str, str] | None:
        return normalize_transitions(value)
