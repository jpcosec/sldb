"""`group_model`."""

from __future__ import annotations

from pydantic import BaseModel, ConfigDict, Field

from sldb.models.notation.diagram_specs.activity.aliases import StepTone


class GroupModel(BaseModel):
    model_config = ConfigDict(extra="ignore")
    label: str = Field(description="Display label of the collapsed subProcess that represents the group.")
    tone: StepTone | None = Field(
        default=None,
        description="Optional BPMN in Color tone for the collapsed subProcess, using the same palette as steps.",
    )
    detail: str | None = Field(
        default=None,
        description="Optional long text about the group, shown in the viewer's side panel when the subProcess is selected.",
    )
