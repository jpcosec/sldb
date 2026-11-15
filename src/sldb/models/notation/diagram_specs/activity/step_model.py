"""`step_model`."""

from __future__ import annotations

from typing import Any
from pydantic import BaseModel, ConfigDict, Field, model_validator

from sldb.models.notation.diagram_specs.base.doc_ref import DocRef
from sldb.models.notation.diagram_specs.activity.aliases import StepTone
from sldb.models.notation.diagram_specs.base.extensions import move_extensions


class StepModel(BaseModel):
    model_config = ConfigDict(extra="forbid")
    label: str = Field(description="Display label rendered for the activity step.")
    kind: str = Field(
        default="action",
        description="Semantic step type: action (default), decision (branches) or merge (joins branches back into one flow; drawn as a diamond like decision).",
    )
    tone: StepTone | None = Field(
        default=None,
        description=(
            "Optional color tone for the BPMN renderer: success, warning, danger, info, neutral, or rule1..rule5 "
            "to tint each decision group. A gateway's outgoing flows take its border color."
        ),
    )
    detail: str | None = Field(
        default=None,
        description=(
            "Optional long text shown in the viewer's side panel; the BPMN box keeps showing only `label`. "
            "Other renderers may ignore it."
        ),
    )
    group: str | None = Field(
        default=None,
        description=(
            "Optional group id the step belongs to. The BPMN renderer draws each group as a collapsed "
            "subProcess with its own drill-down plane; renderers that do not support groups ignore it."
        ),
    )
    partition: str | None = Field(
        default=None,
        description="Optional swimlane (UML activity partition) the step belongs to, such as Dev, Approver or AWS; renderers draw one lane per partition.",
    )
    notes: str | None = Field(
        default=None,
        description="Optional UML note attached to the step, drawn as a note with a folded corner joined to it.",
    )
    next: str | None = Field(
        default=None, description="Identifier of the next step in the default path."
    )
    branches: dict[str, str] = Field(
        default_factory=dict,
        description="Conditional branch labels mapped to destination step identifiers.",
    )
    atoms: list[str] = Field(
        default_factory=list,
        description="Optional atom ids (desk/atoms) that explain this element; the catalog shows exactly these instead of fuzzy matching.",
    )
    refs: list[DocRef] = Field(
        default_factory=list,
        description="Optional sldb document refs `Model:name` (or `store:Model:name` for a linked store) this element points at; the catalog resolves and lists them.",
    )
    extensions: dict[str, Any] = Field(
        default_factory=dict,
        description=(
            "Project annotations: every step key that starts with `x-` (`x-veredicto`, `x-marcas`), kept as "
            "written (renderers ignore them). Any other unknown key in a step is an error."
        ),
    )

    @model_validator(mode="before")
    @classmethod
    def _extensions(cls, value: Any) -> Any:
        return move_extensions(value)
