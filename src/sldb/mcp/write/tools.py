"""The write surface over one SLDB store, at the level the server was started with."""

from __future__ import annotations

from pathlib import Path
from typing import TYPE_CHECKING, Any

import sldb.api as api
from sldb.api.actor import set_actor
from sldb.mcp.changes import Change, Proposal, Sealer, model_of
from sldb.mcp.mutability import CONTENT, model_level, require, server_level
from sldb.mcp.write import apply, pendings, propose
from sldb.mcp.write.pending import PENDING

if TYPE_CHECKING:
    from sldb.mcp.context import ServerContext

#: Who signs the provenance of what this server writes (an agent writes `authored` as
#: `agent:<id>`); `--actor` names the agent.
DEFAULT_ACTOR = "agent:sldb-mcp"


class WriteTools:
    """`propose_changes` (the dry run) and `apply_changes` (whole or nothing), through `sldb.api`."""

    def __init__(self, store: str | Path, level: int, actor: str | None = None, context: ServerContext | None = None) -> None:
        self.level = server_level(level)
        location = api.open_store(Path(store))
        self.store_path, self.project_root = location.store_path, location.project_root
        self.actor = actor or DEFAULT_ACTOR
        set_actor(self.actor)
        self.sealer = Sealer()
        self.context = context

    def propose_changes(self, changes: list[Change]) -> dict[str, Any]:
        """Dry run: turn typed changes (create/update/delete a document, assert_edge/retract_edge)
        into a sealed proposal with the server's guards, and answer what it would write. Writes nothing."""
        self._require(changes, "propose_changes")
        for change in changes:
            self._check_path(change)
        findings = self._domain_findings(changes)
        if self._has_errors(findings):
            return self._domain_rejected(findings)
        fingerprint = api.store_fingerprint(self.store_path)
        batch = [propose.batch_change(self.store_path, change, fingerprint) for change in changes]
        level = max(model_level(c.model) for c in batch)
        sealed = Proposal(changes=batch, level=level, store_hash=fingerprint.store_hash, seal=self.sealer.seal(batch, level, fingerprint.store_hash))
        return self._with_alerts(self._dry_run(sealed), findings)

    def apply_changes(self, proposal: Proposal) -> dict[str, Any]:
        """Apply a proposal exactly as propose_changes returned it: whole, or nothing and why
        (`stale` when the store changed since, `rules` naming the RuleDocs that refused it)."""
        require(self.level, max([CONTENT, *(model_level(c.model) for c in proposal.changes)]), "apply_changes")
        self.sealer.check(proposal)
        findings = self._domain_findings(proposal.changes)
        if self._has_errors(findings):
            return self._domain_rejected(findings)
        return self._with_alerts(apply.run_batch(self.store_path, proposal), findings)

    def _domain_findings(self, changes: list[Any]) -> list[dict[str, Any]]:
        """What every batch validator an extension registered finds in `changes` (all of them run)."""
        if self.context is None:
            return []
        return [finding for validator in self.context.batch_validators for finding in validator(list(changes), self.context)]

    @staticmethod
    def _has_errors(findings: list[dict[str, Any]]) -> bool:
        return any(f.get("level") == "error" for f in findings)

    @staticmethod
    def _domain_rejected(findings: list[dict[str, Any]]) -> dict[str, Any]:
        """A batch a validator refused: nothing sealed or written, with every finding."""
        errors = sum(1 for f in findings if f.get("level") == "error")
        return apply.rejected("domain", f"{errors} domain check(s) failed", findings=findings)

    @staticmethod
    def _with_alerts(answer: dict[str, Any], findings: list[dict[str, Any]]) -> dict[str, Any]:
        """The answer, with the validators' alerts as `domain_alerts` when there are any."""
        return {**answer, "domain_alerts": findings} if findings else answer

    def _dry_run(self, proposal: Proposal) -> dict[str, Any]:
        """The answer of a dry run: the proposal and what it would write."""
        checked = "apply_batch prevalidates the whole batch (shape, registered model, payload round-trip, guards, free destination) and runs the on_write RuleDocs; nothing is written if any check fails"
        pending = [PENDING["dry_run"], *pendings.edge_pending(proposal.changes), *pendings.level_pending(proposal.level)]
        would = [propose.would_write(self.store_path, c) for c in proposal.changes]
        return {"dry_run": True, "written": False, "proposal": proposal.model_dump(mode="json"), "would_write": would, "checked_on_apply": checked, "pending": pending}

    @staticmethod
    def _check_path(change: Any) -> None:
        """No tool writes code or any other file than Markdown."""
        path = getattr(change, "path", None)
        if path is not None and not path.endswith(".md"):
            raise ValueError(f"{change.name}: {path!r} is not a Markdown document; no tool writes code or any other file")

    def _require(self, changes: list[Any], tool: str) -> None:
        """Refuse before reading the store: the tool's level, then each change's model's."""
        require(self.level, CONTENT, tool)
        if not changes:
            raise ValueError("propose at least one change")
        for change in changes:
            require(self.level, model_level(model_of(change)), f"{tool} on {model_of(change)}:{change.name}")
