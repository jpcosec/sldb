"""The base of every typed change: unknown keys are refused."""

from __future__ import annotations

from pydantic import BaseModel, ConfigDict


class _Change(BaseModel):
    model_config = ConfigDict(extra="forbid")
