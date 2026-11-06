"""`LinkEndSpec`: un extremo de un link reificado."""

from __future__ import annotations

from pydantic import BaseModel, ConfigDict


class LinkEndSpec(BaseModel):
    model_config = ConfigDict(extra="forbid")

    relation: str = ""
    label: str = ""
    terminal: str | dict = "none"
