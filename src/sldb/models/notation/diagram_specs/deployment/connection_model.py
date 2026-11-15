"""`connection_model`."""

from __future__ import annotations

from typing import Literal
from pydantic import BaseModel, ConfigDict, Field


class ConnectionModel(BaseModel):
    model_config = ConfigDict(populate_by_name=True, extra="forbid")
    from_: str = Field(
        alias="from", description="Source node identifier for the connection."
    )
    to: str = Field(description="Destination node or artifact identifier for the connection.")
    kind: Literal["communication", "deploy", "manifest"] = Field(
        default="communication",
        description=(
            "communication (default): a communication path between two nodes, or between two artifacts as before; "
            "deploy: «deploy» from an artifact to the node it is deployed on; "
            "manifest: «manifest» from an artifact to the node or artifact it manifests."
        ),
    )
    protocol: str | None = Field(
        default=None,
        description="Optional protocol or transport label for the connection.",
    )
    label: str | None = Field(
        default=None,
        description="Optional label for the connection; shown with the protocol when both are set.",
    )
