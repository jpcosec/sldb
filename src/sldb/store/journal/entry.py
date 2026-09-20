"""One journal entry: a write through `sldb.api`, hash-chained to the previous entry."""

from __future__ import annotations

from datetime import datetime, timezone
from typing import Any

from pydantic import BaseModel, Field


class JournalEntry(BaseModel):
    """A single write, with what changed and the hashes that link it into the chain."""

    operation: str = Field(
        description="The api operation that wrote, e.g. create_document, save_document_payload, "
        "add_model, create_model, promote_model_draft, add_model_field, backfill_document, ..."
    )
    address: str = Field(
        description="What was written: `Model:doc` for documents, the model name for model operations."
    )
    field: str | None = Field(default=None, description="Field within the document, when the write is field-scoped.")
    previous_value: Any | None = Field(default=None, description="Value before the write, when the operation knows it.")
    new_value: Any | None = Field(default=None, description="Value after the write, when the operation knows it.")
    hash_c_before: str | None = Field(default=None, description="Document content hash before the write.")
    hash_c_after: str | None = Field(default=None, description="Document content hash after the write.")
    hash_d_before: str | None = Field(default=None, description="Document field hash before the write.")
    hash_d_after: str | None = Field(default=None, description="Document field hash after the write.")
    hash_a_before: str | None = Field(default=None, description="Store root hash before the write.")
    hash_a_after: str | None = Field(default=None, description="Store root hash after the write.")
    actor: str | None = Field(default=None, description="Optional caller label for correlation, e.g. a pron MoveDoc id.")
    timestamp: datetime = Field(
        default_factory=lambda: datetime.now(timezone.utc),
        description="UTC moment the entry was generated.",
    )
    previous_hash: str | None = Field(default=None, description="entry_hash of the previous entry; None for the first.")
    entry_hash: str = Field(default="", description="SHA-256 of every field above except entry_hash itself.")
