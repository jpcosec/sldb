"""A tracked document addressed by model and name, as returned by document operations."""

from __future__ import annotations

from pathlib import Path

from pydantic import BaseModel, Field


class DocumentReference(BaseModel):
    """Which document an operation tracked, untracked or saved, and where its Markdown lives."""

    model: str = Field(description="Registered model name the document belongs to.")
    name: str = Field(description="Document name, unique within its model.")
    path: Path = Field(description="Absolute path of the document's Markdown file.")
