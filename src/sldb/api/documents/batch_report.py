"""What `apply_batch` applied, and the batch that undoes it."""

from __future__ import annotations

from typing import Any

from pydantic import BaseModel, Field


class BatchReport(BaseModel):
    """The changes a batch wrote, all of them: a batch that fails halfway writes none."""

    saved: list[str] = Field(description="Change ids in the order they were applied: creates and tracks, then updates, moves, and finally untracks and deletes.")
    inverse: list[dict[str, Any]] = Field(default_factory=list, description="The batch that undoes this one, in the shape apply_batch accepts: a create becomes a delete, an update the previous payload, a delete a create with the previous model, path and payload, a move a move back, track and untrack each other. Changes over documents the batch left tracked carry its expected_content_hash (the document without its provenance block), so undoing after another write is a ConflictError with nothing written.")
