"""One rendered piece of a composed field, traced back to its source document."""

from __future__ import annotations

from typing import TYPE_CHECKING, Literal

from pydantic import BaseModel, Field

from sldb.api.segments.source_ref import SourceRef

if TYPE_CHECKING:
    from sldb.api.segments.segment import Segment


class CompositionPiece(BaseModel):
    """The text a single reference contributed to a composed field."""

    type: Literal["composition"] = Field(default="composition", description="Segment discriminator; always 'composition'.")
    start: int = Field(description="Inclusive character offset where the piece starts in the document text.")
    end: int = Field(description="Exclusive character offset where the piece ends in the document text.")
    text: str = Field(description="The piece's rendered surface, as it appears in the document text.")
    path: str = Field(default="", description="Always empty: a piece has no address of its own in the parent payload.")
    marker: str = Field(default="compose", description="Marker kind; always 'compose' for a composed piece.")
    traits: list[str] = Field(default_factory=list, description="Marker traits; empty for composed pieces.")
    editable: bool = Field(default=False, description="Always false: a piece is edited through its source document, not here.")
    display: Literal["inline", "block"] = Field(description="Whether the piece owns its own block of the document or sits inside a line.")
    source: SourceRef = Field(description="The document this piece was composed from.")
    ref_index: int = Field(description="Position of this reference in the composed field's source list.")
    ref: str = Field(description="The reference as written in the parent document.")
    children: list["Segment"] = Field(default_factory=list, description="Segments nested inside the piece, literals interleaved.")
