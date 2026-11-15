"""`class_method`."""

from __future__ import annotations

from pydantic import BaseModel, ConfigDict, Field

from sldb.models.notation.diagram_specs.class_diagram.class_parameter import ClassParameter
from sldb.models.notation.diagram_specs.class_diagram.aliases import MemberName
from sldb.models.notation.diagram_specs.class_diagram.aliases import TypeName
from sldb.models.notation.diagram_specs.class_diagram.aliases import Visibility


class ClassMethod(BaseModel):
    model_config = ConfigDict(extra="forbid")
    name: MemberName
    parameters: list[ClassParameter] = Field(default_factory=list)
    returns: TypeName = "void"
    visibility: Visibility = "public"
    abstract: bool = False
    static: bool = False
