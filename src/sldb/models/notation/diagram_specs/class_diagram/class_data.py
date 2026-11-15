"""`class_data`."""

from __future__ import annotations

from typing import Literal
from pydantic import BaseModel, ConfigDict, Field

from sldb.models.notation.diagram_specs.class_diagram.class_definition import ClassDefinition
from sldb.models.notation.diagram_specs.class_diagram.class_package import ClassPackage
from sldb.models.notation.diagram_specs.class_diagram.class_relation import ClassRelation
from sldb.models.notation.diagram_specs.class_diagram.aliases import Identifier


class ClassData(BaseModel):
    model_config = ConfigDict(extra="forbid")
    direction: Literal["TB", "LR"] = "TB"
    classes: dict[Identifier, ClassDefinition] = Field(min_length=1)
    relations: list[ClassRelation] = Field(default_factory=list)
    packages: dict[Identifier, ClassPackage] = Field(
        default_factory=dict,
        description=(
            "Optional UML packages. When a spec declares packages, every class belongs to exactly one package "
            "(an orphan class is an error); packages nest through `contains`."
        ),
    )
