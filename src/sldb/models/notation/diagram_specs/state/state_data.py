"""`state_data`."""

from __future__ import annotations

from pydantic import BaseModel, ConfigDict, Field

from sldb.models.notation.diagram_specs.state.state_model import StateModel
from sldb.models.notation.diagram_specs.state.transition_model import TransitionModel


class StateData(BaseModel):
    model_config = ConfigDict(extra="forbid")
    entity: str = Field(
        description="Name of the entity whose lifecycle is being modeled."
    )
    initial: str = Field(description="Identifier of the initial state.")
    states: list[StateModel] = Field(
        description="All states that can appear in the lifecycle."
    )
    transitions: list[TransitionModel] = Field(
        description="Transitions connecting the defined states."
    )
