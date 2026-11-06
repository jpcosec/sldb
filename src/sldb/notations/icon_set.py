"""`IconSet`: el conjunto de iconos que declara una paleta."""

from __future__ import annotations

from pydantic import BaseModel, ConfigDict, Field


class IconSet(BaseModel):
    model_config = ConfigDict(extra="forbid")

    name: str
    version: str = ""
    icons: list[str] = Field(min_length=1)
