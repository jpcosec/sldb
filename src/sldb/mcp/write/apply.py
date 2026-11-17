"""Apply a proposal with `sldb.api.apply_batch`: whole, or nothing and the cause."""

from __future__ import annotations

from pathlib import Path
from typing import TYPE_CHECKING, Any

import sldb.api as api
from sldb.mcp.addresses import document_address
from sldb.mcp.changes import EDGE_MODEL, BatchChange, Proposal
from sldb.mcp.write.findings import edge_findings, on_write_alerts
from sldb.mcp.write.pending import PENDING
from sldb.mcp.write.pendings import edge_pending, level_pending

if TYPE_CHECKING:
    from sldb.mcp.write.undo import UndoStack


def rejected(cause: str, explanation: str, **detail: Any) -> dict[str, Any]:
    """A refused proposal: nothing was written, and why."""
    return {"applied": False, "rejected": cause, "explanation": explanation, "written": False, **detail}


def refusal(error: Exception) -> dict[str, Any]:
    """SLDB's refusals come back with their cause; anything else is a tool error."""
    if not type(error).__module__.startswith("sldb."):
        raise error
    findings = [f.as_dict() for f in getattr(error, "findings", [])]
    if not findings:
        return rejected(type(error).__name__, str(error))
    rules = sorted({f["code"] for f in findings})
    return rejected("rules", f"refused by {', '.join(rules)}: {error}", findings=findings, rules=rules)


def written_row(store_path: Path, change: BatchChange) -> dict[str, Any]:
    """A document just written: its address, path, version and provenance."""
    document = api.serialize_document(api.runtime_document(store_path, None, f"{change.model}/{change.id}"))
    export_id = f"{change.model}:{change.id}"
    return {"export_id": export_id, "address": document_address(export_id), "path": document["path"], "version": document["version"], "provenance": document["provenance"]}


def applied(store_path: Path, proposal: Proposal, report: Any) -> dict[str, Any]:
    """The answer of an applied proposal."""
    written = [c for c in proposal.changes if c.action != "delete"]
    pending = [*edge_pending(proposal.changes), *level_pending(proposal.level), PENDING["guards_in_transaction"], PENDING["on_write_alerts"]]
    deleted = [document_address(f"{c.model}:{c.id}") for c in proposal.changes if c.action == "delete"]
    edges = [c for c in written if c.model == EDGE_MODEL]
    return {"applied": True, "saved": list(report.saved), "documents": [written_row(store_path, c) for c in written], "deleted": deleted, "alerts": on_write_alerts(store_path, written), "edge_findings": edge_findings(store_path, edges), "pending": pending}


def run_batch(store_path: Path, proposal: Proposal, undo: UndoStack) -> dict[str, Any]:
    """`apply_batch` on the proposal, answered as applied, stale or refused; an applied batch's
    inverse goes onto the session's undo stack."""
    try:
        report = api.apply_batch(store_path, [c.batch_form() for c in proposal.changes])
    except api.ConflictError as error:
        return rejected("stale", f"the store changed after the proposal was made: {error} Read it again and propose anew.", document=error.ref)
    except Exception as error:
        return refusal(error)
    undo.push(report.inverse)
    return applied(store_path, proposal, report)
