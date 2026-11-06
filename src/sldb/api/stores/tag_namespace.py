"""One entry of `tag_namespaces` in `.sldb/store.yaml` (GD27, docs/architecture/tags.md).

A tag `name:value` belongs to the namespace `name` (the text before its first colon). The
namespace says whether the value's dots form a hierarchy (`hierarchical`), whether the value
places the document in a folder (`folder_axis`, read by `tag_folder`) and which documents
anchor its values (`anchored_by: {model, field}`: a local document of `model` whose `field`
is the tag). The checks run as the rule family `builtin:tag_namespace:<name>`.
"""

from __future__ import annotations

from typing import Any

from pydantic import BaseModel, ConfigDict, Field, SerializerFunctionWrapHandler, field_validator, model_serializer

from sldb.store.semantic_tags import split_namespace, tag_prefixes

ANCHOR_KEYS = ("model", "field")


class TagNamespace(BaseModel):
    """What a store declares of one tag namespace."""

    model_config = ConfigDict(extra="forbid")

    name: str = Field(description="The namespace: what precedes the first colon of its tags; no colon, no blank.")
    hierarchical: bool = Field(default=True, description="Whether `a.b.c` is a path whose prefixes `a` and `a.b` are tags too; false means the value is one piece, without prefixes.")
    folder_axis: bool = Field(default=False, description="Declarative: the value of a tag of this namespace is the document's folder (`tag_folder`).")
    anchored_by: dict[str, str] | None = Field(default=None, description="`{model, field}`: every tag the namespace requires must be the `field` of a local document of `model`.")

    @field_validator("name")
    @classmethod
    def _is_a_namespace(cls, value: str) -> str:
        if not value.strip() or ":" in value or value != value.strip():
            raise ValueError(f"tag namespace name {value!r} must be non-blank, without colons or surrounding spaces")
        return value

    @field_validator("anchored_by")
    @classmethod
    def _names_model_and_field(cls, value: dict[str, str] | None) -> dict[str, str] | None:
        if value is not None and (set(value) != set(ANCHOR_KEYS) or not all(str(value[k]).strip() for k in ANCHOR_KEYS)):
            raise ValueError(f"anchored_by must be {{model, field}} with non-blank values, not {value!r}")
        return value

    @model_serializer(mode="wrap")
    def _without_absent_anchor(self, handler: SerializerFunctionWrapHandler) -> dict[str, Any]:
        """A namespace without `anchored_by` dumps without the key (as `store.yaml` is written)."""
        return {key: value for key, value in handler(self).items() if value is not None}

    def required(self, tag: str) -> list[str]:
        """The tags an anchor must exist for so `tag` is placed: its value's prefixes (the
        value included) when hierarchical, else the value alone; each with the namespace."""
        value = split_namespace(tag)[1]
        values = tag_prefixes(value) if self.hierarchical else [value]
        return [f"{self.name}:{v}" for v in values]


def unique_namespaces(value: list[TagNamespace]) -> list[TagNamespace]:
    """`tag_namespaces` as declared, once no name repeats (a `ValueError` naming the repeated ones)."""
    names = [namespace.name for namespace in value]
    if len(names) != len(set(names)):
        raise ValueError(f"tag_namespaces declares a name twice: {sorted(n for n in set(names) if names.count(n) > 1)}")
    return value
