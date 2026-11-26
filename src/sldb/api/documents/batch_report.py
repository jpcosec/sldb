"""What `apply_batch` applied, and the batch that undoes it."""

from __future__ import annotations

from typing import Any

from pydantic import BaseModel, Field


class BatchReport(BaseModel):
    """The changes a batch wrote, all of them: a batch that fails halfway writes none."""

    saved: list[str] = Field(description="Change ids in the order they were applied: creates and tracks, then updates, moves, and finally untracks and deletes.")
    inverse: list[dict[str, Any]] = Field(default_factory=list, description="The batch that undoes this one, in the shape apply_batch accepts: a create becomes a delete, an update the previous payload, a delete a create with the previous model, path and payload, a move a move back, track and untrack each other. Changes over documents the batch left tracked carry its expected_content_hash (the document without its provenance block), so undoing after another write is a ConflictError with nothing written.")
    applied: bool = Field(default=True, description="False for a `dry_run`: the batch passed prevalidation and nothing was written (`saved` and `inverse` are empty).")
    rejections: list[dict[str, Any]] = Field(default_factory=list, description="Only for a `dry_run`: one entry per edge violation the batch would introduce (`code` types, cardinality, condition or endpoint; `relation` {source, type, target}; `relation_doc`; `message`), found on the index as it would be after the batch. A real apply does not check them: `dry_run` first.")
    planned: list[str] = Field(default_factory=list, description="Only for a `dry_run`: the change ids in the order a real apply would write them.")
    documents: list[dict[str, Any]] = Field(default_factory=list, description="Per document the batch touched: id, action, `before` (model, path, payload it replaced; null when it created it) and `after_hash` (the content hash it left; null when it removed it). What the write journal keeps to revert the batch.")
    batch_id: str | None = Field(default=None, description="The id the write journal gave this batch (None for a dry run).")
