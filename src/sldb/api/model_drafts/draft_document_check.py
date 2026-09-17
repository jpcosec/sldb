"""The result of checking one tracked document against a model draft."""

from __future__ import annotations

from pathlib import Path

from pydantic import BaseModel, Field


class DraftDocumentCheck(BaseModel):
    """Whether one tracked document still round-trips under the checked contract."""

    name: str = Field(description="Tracked document name.")
    path: Path = Field(description="The document's Markdown file.")
    valid: bool = Field(description="True when the document extracts and re-renders identically under the contract.")
