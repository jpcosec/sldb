"""A point-in-time capture of the portable graph."""

from __future__ import annotations

from datetime import datetime, timezone
from typing import Any

from pydantic import BaseModel, Field

from sldb.store.graph.node import KnowledgeNode


class GraphSnapshot(BaseModel):
    """The portable capture used for persistence, backups and inter-module transfers."""

    version: str = Field(..., description="Schema version of the snapshot format.")
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc), description="The UTC timestamp when this snapshot was generated.")
    nodes: list[KnowledgeNode] = Field(description="The complete list of nodes included in this snapshot.")
    metadata: dict[str, Any] = Field(default_factory=dict, description="Optional metadata about the snapshot.")
