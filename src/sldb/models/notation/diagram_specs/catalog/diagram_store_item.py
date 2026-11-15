"""`diagram_store_item`."""

from __future__ import annotations

from pydantic import BaseModel, ConfigDict, Field

from sldb.models.notation.diagram_specs.catalog.aliases import _PATH_RULE


class DiagramStoreItem(BaseModel):
    """A catalog view: an item of a diagram store or an entry of a legacy `vistas.yml`."""

    model_config = ConfigDict(extra="forbid", json_schema_extra={"description": "A catalog view. " + _PATH_RULE})

    id: str
    title: str | None = None
    desc: str | None = None
    category: str | None = None
    nav: str | None = None
    lbl: str | None = None
    src: str | None = Field(default=None, description="Rendered source of the view (`.mmd`, `.svg`, `.html`, optionally `#fragment`). " + _PATH_RULE)
    mmd: str | None = Field(default=None, description="Legacy alias of `src`. " + _PATH_RULE)
    specs: list[str] = Field(default_factory=list, description="Spec YAML files of the view (a path with extension; an id without extension keeps the legacy lookup). " + _PATH_RULE)
    notation: str | None = Field(
        default=None,
        description="Notation the view is synced with: a path to a notation YAML, a builtin name or the name of a NotationDoc in the store; absent = the builtin of the spec's type. " + _PATH_RULE,
    )
    puml: str | None = None
    notes: list[str] = Field(default_factory=list)
    project: str | None = None
    type: str | None = None
    tags: list[str] = Field(default_factory=list)
