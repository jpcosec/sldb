"""What a server knows and an extension may use: the store, the level, the actor, the signal log
and the batch validators the write tools run."""

from __future__ import annotations

from pathlib import Path

import sldb.api as api
from sldb.mcp.extension import BatchValidator
from sldb.mcp.mutability import server_level
from sldb.mcp.signals import SignalLog


class ServerContext:
    """The store a server serves, the write level the operator fixed, who signs what it writes
    and the signal log. Handed to every extension next to the server."""

    def __init__(self, store: str | Path, level: int, actor: str | None) -> None:
        location = api.open_store(Path(store), mode="readonly")
        self.store_path, self.project_root = location.store_path, location.project_root
        self.level = server_level(level)
        self.actor = actor
        self.log = SignalLog(self.store_path, actor)
        self.batch_validators: list[BatchValidator] = []

    def add_batch_validator(self, validator: BatchValidator) -> None:
        """Run `validator(changes, context)` before `propose_changes` and `apply_changes` write
        or seal anything; its "error" findings reject the batch, its "alert" findings ride along."""
        self.batch_validators.append(validator)
