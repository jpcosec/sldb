"""`activity_data`."""

from __future__ import annotations

from pydantic import BaseModel, ConfigDict, Field, model_validator

from sldb.models.notation.diagram_specs.activity.group_model import GroupModel
from sldb.models.notation.diagram_specs.activity.step_model import StepModel


class ActivityData(BaseModel):
    model_config = ConfigDict(extra="forbid")
    start: str = Field(description="Identifier of the first step in the activity flow.")
    steps: dict[str, StepModel] = Field(
        description="All activity steps keyed by identifier."
    )
    end: str = Field(
        description="Identifier of the terminal step in the activity flow."
    )
    groups: dict[str, GroupModel] = Field(
        default_factory=dict,
        description=(
            "Optional groups keyed by id. Each group becomes a collapsed subProcess in the BPMN renderer; "
            "a step joins one with its `group` field."
        ),
    )

    @model_validator(mode="after")
    def _groups_exist(self) -> "ActivityData":
        known = set(self.groups)
        for sid, step in self.steps.items():
            if step.group is not None and step.group not in known:
                available = ", ".join(sorted(known)) or "none defined"
                raise ValueError(
                    f"Step '{sid}' references unknown group '{step.group}' (groups: {available})"
                )
        return self
