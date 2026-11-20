"""A tracked document addressed by model and name, as returned by document operations."""

from __future__ import annotations

from pathlib import Path
from typing import Any

from pydantic import BaseModel, Field


class DocumentReference(BaseModel):
    """Which document an operation tracked, untracked or saved, and where its Markdown lives."""

    model: str = Field(description="Registered model name the document belongs to.")
    name: str = Field(description="Document name, unique within its model.")
    path: Path = Field(description="Absolute path of the document's Markdown file.")
    alerts: list[dict[str, Any]] = Field(default_factory=list, description="The on_write alerts of the write that saved it (Finding.as_dict()); empty otherwise.")
