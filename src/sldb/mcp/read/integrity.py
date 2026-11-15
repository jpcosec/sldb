"""The integrity check of the store and its edge index."""

from __future__ import annotations

from pathlib import Path
from typing import Any

import sldb.api as api
from sldb.mcp.paging import page


def counts(report: Any) -> dict[str, int]:
    """The size of each list of an `EdgeCheckReport`."""
    return {k: len(v) for k, v in report.model_dump().items() if isinstance(v, list)}


def check_integrity(store_path: Path, project_root: Path, offset: int, limit: int) -> dict[str, Any]:
    """The store's integrity check (`check_store`) and the edge index's (`check_edges`):
    verdicts and counts, with the errors and alerts as one page of findings.

    The verdict covers this store's own edges (`include_linked=False`); the federated
    index is reported apart, as `linked_edges`: its findings are the linked stores' to fix.
    """
    report = api.check_store(store_path, project_root)
    edges, federated = api.check_edges(store_path, include_linked=False), api.check_edges(store_path, include_linked=True)
    findings = list(report["errors"]) + list(report["alerts"]) + [{"level": "error", "code": "edges/invalid", "what": e} for e in edges.errors]
    summary = {k: (len(v) if isinstance(v, list) else v) for k, v in report.items()}
    shown = page(findings, offset, limit, None if findings else "the store and its edge index report no error and no alert")
    return {"ok": bool(report["ok"]) and edges.ok, "store": summary, "edges": {"ok": edges.ok, **counts(edges)}, "linked_edges": counts(federated), "findings": shown}
