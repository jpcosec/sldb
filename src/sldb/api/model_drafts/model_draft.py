"""A pending edit of a model's contract, as returned by the draft-editing operations."""

from __future__ import annotations

from pathlib import Path

from pydantic import BaseModel, Field


class ModelDraft(BaseModel):
    """The draft file an edit was written to; the active model is untouched until promotion."""

    model: str = Field(description="Registered model name the draft edits.")
    draft_path: Path = Field(description="The `.py.temp` sibling of the model source holding the accumulated draft.")
