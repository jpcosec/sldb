"""What `apply_batch` applied."""

from __future__ import annotations

from pydantic import BaseModel, Field


class BatchReport(BaseModel):
    """The changes a batch wrote, all of them: a batch that fails halfway writes none."""

    saved: list[str] = Field(description="Change ids in the order they were applied: creates and tracks, then updates, moves, and finally untracks and deletes.")
