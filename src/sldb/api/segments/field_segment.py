"""A stretch of document text that one marker wrote out of the payload."""

from __future__ import annotations

from typing import TYPE_CHECKING, Any, Literal

from pydantic import BaseModel, Field

from sldb.api.segments.composition_spec import CompositionSpec
from sldb.api.segments.source_ref import SourceRef

if TYPE_CHECKING:
    from sldb.api.segments.segment import Segment


class FieldSegment(BaseModel):
    """One field's surface in the render, with its address and typed value."""

    type: Literal["field"] = Field(default="field", description="Segment discriminator; always 'field'.")
    start: int = Field(description="Inclusive character offset where the value starts in the document text.")
    end: int = Field(description="Exclusive character offset where the value ends; equal to start for an absent optional.")
    text: str = Field(description="The value's rendered surface, as it appears in the document text.")
    path: str = Field(description="Field address in the 'sldb fields' space, such as 'title' or 'steps/2/title'.")
    marker: str = Field(description="Marker kind that wrote the value: rev, optrev, render or py.")
    traits: list[str] = Field(default_factory=list, description="Marker traits declared in the template, such as 'yaml' or 'table'.")
    editable: bool = Field(description="Whether the template lets the value be edited; true for rev and optrev markers.")
    display: Literal["inline", "block"] = Field(description="Whether the field owns its own block of the document or sits inside a line.")
    kind: str | None = Field(default=None, description="Input kind of the field per sldb.api.schema.field_kinds; None for composed pieces' inner fields.")
    value: Any = Field(default=None, description="The typed value behind the surface; the UI edits this, not the text.")
    source: SourceRef | None = Field(default=None, description="Origin document when the value comes from a composed piece; None when it is the document's own.")
    composition: CompositionSpec | None = Field(default=None, description="Composition declaration when this field assembles other documents; None otherwise.")
    children: list["Segment"] = Field(default_factory=list, description="Segments nested inside this one, literals interleaved.")
