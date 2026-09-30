"""One field located in raw markdown, with how confidently it was placed."""

from __future__ import annotations

from typing import Any, Literal

from pydantic import BaseModel, Field


class ExtractedField(BaseModel):
    """A field's span in the raw text, carried over from the canonical render."""

    type: Literal["field"] = Field(default="field", description="Segment discriminator; always 'field'.")
    start: int = Field(description="Inclusive character offset where the value starts in the raw text.")
    end: int = Field(description="Exclusive character offset where the value ends in the raw text.")
    text: str = Field(description="The value's surface as it appears in the raw text.")
    path: str = Field(description="Field address in the 'sldb fields' space, such as 'title' or 'tags/0'.")
    marker: str = Field(description="Marker kind that wrote the value: rev, optrev, render or py.")
    traits: list[str] = Field(default_factory=list, description="Marker traits declared in the template.")
    editable: bool = Field(description="Whether the template lets the value be edited; true for rev and optrev.")
    display: Literal["inline", "block"] = Field(description="Whether the field owns its own block or sits inside a line.")
    kind: str | None = Field(default=None, description="Input kind of the field per sldb.api.schema.field_kinds.")
    value: Any = Field(default=None, description="The typed value behind the surface.")
    alignment: Literal["exact", "approximate"] = Field(description="'exact' when both borders fell on text identical to the canonical render, else 'approximate'.")
