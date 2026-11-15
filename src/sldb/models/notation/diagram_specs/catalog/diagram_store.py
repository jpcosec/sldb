"""`diagram_store`."""

from __future__ import annotations

from typing import Literal
from pydantic import BaseModel, ConfigDict, Field

from sldb.models.notation.diagram_specs.catalog.diagram_store_item import DiagramStoreItem
from sldb.models.notation.diagram_specs.catalog.diagram_store_ref import DiagramStoreRef


class DiagramStore(BaseModel):
    model_config = ConfigDict(extra="forbid")

    kind: Literal["diagram-store"] = "diagram-store"
    template: str = "template.html"
    title: str | None = None
    catalog_title: str | None = None
    brand_name: str | None = None
    brand_subtitle: str | None = None
    project_name: str | None = None
    project: str | None = None
    category: str | None = None
    type: str | None = None
    html_artifact: str | None = None
    tags: list[str] = Field(default_factory=list)
    stores: list[str | DiagramStoreRef] = Field(default_factory=list)
    items: list[DiagramStoreItem] = Field(default_factory=list)
