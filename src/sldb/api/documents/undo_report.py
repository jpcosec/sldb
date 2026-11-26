"""What `undo_batches` reverted."""

from __future__ import annotations

from typing import Any

from pydantic import BaseModel, Field


class UndoReport(BaseModel):
    undone: list[str] = Field(description="Batch ids reverted, newest first.")
    saved: list[list[str]] = Field(default_factory=list, description="Per reverted batch, the change ids written.")
    changes: list[list[dict[str, Any]]] = Field(default_factory=list, description="Per reverted batch, the inverse changes applied.")
    remaining: int = Field(description="Batches still not reverted.")
