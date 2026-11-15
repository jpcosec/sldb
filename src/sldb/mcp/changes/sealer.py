"""The seal that proves a proposal came from this server process, unchanged."""

from __future__ import annotations

import hashlib
import hmac
import json
import secrets

from sldb.mcp.changes.batch_change import BatchChange
from sldb.mcp.changes.proposal import Proposal


class Sealer:
    """Seals and checks proposals with a secret of this server process (an HMAC: it is not a
    store precondition; the guards are, and `apply_batch` checks them)."""

    def __init__(self) -> None:
        self._key = secrets.token_bytes(32)

    def seal(self, changes: list[BatchChange], level: int, store_hash: str) -> str:
        body = json.dumps({"changes": [c.model_dump(mode="json") for c in changes], "level": level, "store_hash": store_hash}, sort_keys=True, separators=(",", ":"))
        return hmac.new(self._key, body.encode("utf-8"), hashlib.sha256).hexdigest()

    def check(self, proposal: Proposal) -> None:
        if not hmac.compare_digest(proposal.seal, self.seal(proposal.changes, proposal.level, proposal.store_hash)):
            raise ValueError("the proposal is not the one propose_changes returned (edited, or proposed by another server process); propose it again")
