"""`class_relation`."""

from __future__ import annotations

from typing import Literal
from pydantic import BaseModel, ConfigDict, Field

from sldb.models.notation.diagram_specs.class_diagram.aliases import Identifier
from sldb.models.notation.diagram_specs.class_diagram.aliases import Label
from sldb.models.notation.diagram_specs.class_diagram.aliases import Multiplicity


class ClassRelation(BaseModel):
    model_config = ConfigDict(populate_by_name=True, extra="forbid")
    from_: Identifier = Field(alias="from")
    to: Identifier
    relation: Literal["inheritance", "realization", "composition", "aggregation", "association", "dependency"]
    label: Label | None = None
    from_multiplicity: Multiplicity | None = None
    to_multiplicity: Multiplicity | None = None
