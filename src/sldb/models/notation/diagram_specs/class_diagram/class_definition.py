"""`class_definition`."""

from __future__ import annotations

from typing import Literal
from pydantic import BaseModel, ConfigDict, Field

from sldb.models.notation.diagram_specs.class_diagram.class_attribute import ClassAttribute
from sldb.models.notation.diagram_specs.class_diagram.class_method import ClassMethod
from sldb.models.notation.diagram_specs.base.doc_ref import DocRef
from sldb.models.notation.diagram_specs.class_diagram.aliases import Label


class ClassDefinition(BaseModel):
    model_config = ConfigDict(extra="forbid")
    label: Label | None = None
    kind: Literal["class", "interface", "abstract", "record", "protocol", "enum"] = "class"
    attributes: list[ClassAttribute] = Field(default_factory=list)
    methods: list[ClassMethod] = Field(default_factory=list)
    atoms: list[str] = Field(
        default_factory=list,
        description="Optional atom ids (desk/atoms) that explain this element; the catalog shows exactly these instead of fuzzy matching.",
    )
    refs: list[DocRef] = Field(
        default_factory=list,
        description="Optional sldb document refs `Model:name` (or `store:Model:name` for a linked store) this element points at; the catalog resolves and lists them.",
    )
