"""`ThemeColor`: un color por tema."""

from __future__ import annotations

from pydantic import BaseModel, ConfigDict


class ThemeColor(BaseModel):
    model_config = ConfigDict(extra="forbid")

    light: str
    dark: str
