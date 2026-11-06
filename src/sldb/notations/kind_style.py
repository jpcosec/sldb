"""`KindStyle`: forma, icono, relleno y trazo de un kind."""

from __future__ import annotations

from pydantic import BaseModel, ConfigDict


class KindStyle(BaseModel):
    model_config = ConfigDict(extra="forbid")

    shape: str
    icon: str
    fill: str
    stroke: str
