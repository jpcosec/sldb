"""`message_model`."""

from __future__ import annotations

from pydantic import BaseModel, ConfigDict, Field


class MessageModel(BaseModel):
    model_config = ConfigDict(populate_by_name=True, extra="forbid")
    from_: str = Field(
        alias="from", description="Participant id that sends the message."
    )
    to: str = Field(description="Participant id that receives the message.")
    message: str = Field(description="Label displayed on the message arrow.")
    kind: str = Field(
        default="sync", description="Message interaction type, such as sync or async."
    )
    condition: str | None = Field(
        default=None,
        description="Optional condition that qualifies when the message is sent.",
    )
    group: str | None = Field(
        default=None, description="Optional group label for visually related messages."
    )
