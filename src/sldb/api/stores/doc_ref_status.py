"""Whether a document reference resolves, as `doc_status` reports it."""

from __future__ import annotations

from pydantic import BaseModel, Field


class DocRefStatus(BaseModel):
    """The state of one reference, computed when asked and never stored."""

    ref: str = Field(description="The reference as given.")
    store: str = Field(description="`local`, or the alias of the linked store the reference names.")
    status: str = Field(description="ok | missing | ambiguous | link-missing (no such alias) | link-broken (alias whose target is missing or not a store).")
    model: str | None = Field(default=None, description="Model of the document, when found.")
    name: str | None = Field(default=None, description="Name of the document, when found.")
    path: str | None = Field(default=None, description="Tracked path, relative to its store's project root, when found.")
    detail: str | None = Field(default=None, description="Why the reference did not resolve, when it did not.")

    @property
    def exists(self) -> bool:
        """True only when the reference names exactly one document."""
        return self.status == "ok"
