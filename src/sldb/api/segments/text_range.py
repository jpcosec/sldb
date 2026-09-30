"""A stretch of text addressed by character offsets."""

from __future__ import annotations

from pydantic import BaseModel, Field


class TextRange(BaseModel):
    """Raw-text content that no field and no template literal explains."""

    start: int = Field(description="Inclusive character offset where the range starts in the raw text.")
    end: int = Field(description="Exclusive character offset where the range ends in the raw text.")
    text: str = Field(description="The range's text, trimmed of surrounding whitespace.")
