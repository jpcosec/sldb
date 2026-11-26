"""`StandardSpec`: el estandar que una notacion implementa."""

from __future__ import annotations

from pydantic import BaseModel, ConfigDict, field_validator


class StandardSpec(BaseModel):
    """El estandar que una notacion implementa: nombre y, si se sabe, version."""

    model_config = ConfigDict(extra="forbid")

    name: str
    version: str | None = None

    @field_validator("name")
    @classmethod
    def _name(cls, v: str) -> str:
        if not v.strip():
            raise ValueError("standard.name must be a non-empty name")
        return v.strip()

    @field_validator("version")
    @classmethod
    def _version(cls, v: str | None) -> str | None:
        if v is None:
            return None
        if not v.strip():
            raise ValueError("standard.version must be non-empty when present")
        return v.strip()

    def label(self) -> str:
        """`<name> <version>`, o solo el nombre sin version."""
        return f"{self.name} {self.version}" if self.version else self.name
