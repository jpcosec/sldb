"""`sequence_data`."""

from __future__ import annotations

from pydantic import BaseModel, ConfigDict, Field

from sldb.models.notation.diagram_specs.sequence.message_model import MessageModel
from sldb.models.notation.diagram_specs.sequence.participant_model import ParticipantModel


class SequenceData(BaseModel):
    model_config = ConfigDict(extra="forbid")
    participants: list[ParticipantModel] = Field(
        description="Ordered participants that appear across the sequence diagram."
    )
    messages: list[MessageModel] = Field(
        description="Ordered interactions exchanged between participants."
    )
