"""The result of verifying a store journal's hash chain."""

from __future__ import annotations

from pydantic import BaseModel, Field


class JournalVerifyReport(BaseModel):
    """Whether a store's journal chain verifies, and where it breaks if it does not."""

    store: str = Field(description="Store path the journal was read from.")
    entries: int = Field(description="Number of entries checked.")
    valid: bool = Field(description="True when every entry hashes and links to the previous one.")
    broken_seq: int | None = Field(default=None, description="Sequence number where the chain broke.")
    reason: str | None = Field(default=None, description="Why the chain broke, when it did.")
