"""A whole document seen as an editable sequence of literals and field spans."""

from __future__ import annotations

from typing import Any

from pydantic import BaseModel, Field

from sldb.api.segments.segment import Segment


class DocumentSegments(BaseModel):
    """The canonical render of one tracked document, segmented by origin."""

    id: str = Field(description="The document reference the caller asked for.")
    doc: str | None = Field(default=None, description="Tracked document name; None when the document is not named in the store.")
    model: str = Field(description="Class name of the model the document is tracked with.")
    path: str | None = Field(default=None, description="Path of the document file relative to the store root; None when untracked.")
    text: str = Field(description="The canonical render of the payload; every offset in segments addresses this text.")
    canonical: bool | None = Field(default=None, description="Whether the file on disk matches the canonical text; None when the file could not be read.")
    payload: dict[str, Any] = Field(default_factory=dict, description="The extracted payload the text was rendered from.")
    segments: list[Segment] = Field(default_factory=list, description="The document's full segment sequence, in reading order.")
