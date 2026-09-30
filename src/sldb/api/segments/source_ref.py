"""Where a segment's text came from when it is not the document's own payload."""

from __future__ import annotations

from pydantic import BaseModel, Field


class SourceRef(BaseModel):
    """The origin document of a composed piece, as the store knows it."""

    doc: str | None = Field(default=None, description="Tracked document name of the source; None when the referenced file is not tracked.")
    path: str = Field(description="The reference as written in the parent document, usually a file path.")
    model: str = Field(description="Class name of the model the source was extracted with.")
