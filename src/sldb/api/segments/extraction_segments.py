"""What a model finds in a piece of raw markdown, and what it leaves unexplained."""

from __future__ import annotations

from typing import Any

from pydantic import BaseModel, Field

from sldb.api.segments.extracted_field import ExtractedField
from sldb.api.segments.text_range import TextRange


class ExtractionSegments(BaseModel):
    """Fields located in raw markdown, plus the coverage of that placement."""

    model: str = Field(description="Class name of the model the markdown was extracted with.")
    text: str = Field(description="The raw markdown exactly as submitted; every field offset addresses this.")
    payload: dict[str, Any] = Field(default_factory=dict, description="The payload extracted from the raw markdown.")
    canonical_text: str = Field(description="The canonical render of that payload, which the offsets were mapped from.")
    fields: list[ExtractedField] = Field(default_factory=list, description="Every field found, in reading order over the raw text.")
    unmatched: list[TextRange] = Field(default_factory=list, description="Runs of raw text that neither a field nor the template accounts for.")
    coverage: float = Field(description="Fraction of the raw text's non-blank length that field spans cover, from 0 to 1.")
