"""The proposal `propose_changes` returns and `apply_changes` takes back."""

from __future__ import annotations

from pydantic import BaseModel, ConfigDict, Field

from sldb.mcp.changes.batch_change import BatchChange


class Proposal(BaseModel):
    """What `propose_changes` returns and `apply_changes` takes back, unchanged."""

    model_config = ConfigDict(extra="forbid")

    changes: list[BatchChange]
    level: int = Field(description="The write level the batch needs.")
    store_hash: str = Field(description="The store's fingerprint when proposed (informational: no SLDB write accepts it as a precondition yet).")
    seal: str = Field(description="The server's seal over the batch; any edit makes `apply_changes` refuse it.")
