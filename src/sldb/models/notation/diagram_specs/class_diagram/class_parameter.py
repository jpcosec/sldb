"""`class_parameter`."""

from __future__ import annotations

from pydantic import BaseModel, ConfigDict

from sldb.models.notation.diagram_specs.class_diagram.aliases import MemberName
from sldb.models.notation.diagram_specs.class_diagram.aliases import TypeName


class ClassParameter(BaseModel):
    model_config = ConfigDict(extra="forbid")
    name: MemberName
    type: TypeName
