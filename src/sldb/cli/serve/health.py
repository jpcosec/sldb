"""`/health`: whether this store is serving something trustworthy, and what to do if not.

The route used to answer `{"status": "ok"}` unconditionally — "the process is up", which the
HTTP status code already said. A reader asking a store for its health wants to know whether the
payloads it is about to read were extracted under the contract that is loaded now, and if not,
which subject to look at and whether a command or a human resolves it.
"""

from __future__ import annotations

from pathlib import Path
from typing import Any


def health_payload(store_path: Path, project_root: Path, pythonpath: str) -> dict[str, Any]:
    """The store's verdict, its findings, and the single action they imply."""
    from sldb.api.stores.store_check import check_store

    report = check_store(store_path, project_root, pythonpath)
    return {"status": "ok" if report["valid"] else "degraded", **_findings(report)}


def _findings(report: dict[str, Any]) -> dict[str, Any]:
    """The findings and the action — empty when the store is clean.

    A finding that needs a decision outranks any safe command: the index holds the only record
    of the value a reindex would overwrite, so it must not be offered as the next step.
    """
    if report["valid"]:
        return {"findings": [], "action": None}
    findings = _finding_list(report)
    blocked = [f for f in findings if f["needs_decision"]]
    action = f"inspect: {len(blocked)} finding(s) need a decision" if blocked else "run: sldb stores update"
    return {"findings": findings, "action": action}


def _finding_list(report: dict[str, Any]) -> list[dict[str, Any]]:
    """One entry per thing to look at: what moved, whose it is, whether a command fixes it."""
    models = [{"kind": "contract_moved", "subject": name, "needs_decision": False} for name in report.get("moved_contracts", [])]
    docs = [{"kind": d["note"], "subject": f"{d['model']}:{d['doc']}", "needs_decision": True, "explain": d["explain"]} for d in report.get("damaged", [])]
    return models + docs
