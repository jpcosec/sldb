"""A stretch of document text that came from the template, not from a value."""

from __future__ import annotations

from typing import Literal

from pydantic import BaseModel, Field


class LiteralSegment(BaseModel):
    """Template text between two field spans; never editable."""

    type: Literal["literal"] = Field(default="literal", description="Segment discriminator; always 'literal'.")
    start: int = Field(description="Inclusive character offset where the literal starts in the document text.")
    end: int = Field(description="Exclusive character offset where the literal ends in the document text.")
    text: str = Field(description="The literal text itself, exactly as it appears in the document.")
