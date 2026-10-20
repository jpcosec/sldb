"""`/health`: whether this store is serving something trustworthy, and what to do if not.

The route used to answer `{"status": "ok"}` unconditionally — "the process is up", which the
HTTP status code already said. A reader asking a store for its health wants to know whether the
payloads it is about to read were extracted under the contract that is loaded now, and if not,
which subject to look at and whether a command or a human resolves it.

`status` is `degraded` only on an error; every alert is listed as a finding all the same, so a
healthy store still says what moved (docs/architecture/anchoring.md §4).
"""

from __future__ import annotations

from pathlib import Path
from typing import Any

_DECIDE = ("store/data-mutation", "store/missing")


def health_payload(store_path: Path, project_root: Path, pythonpath: str) -> dict[str, Any]:
    """The store's verdict, its findings, and the single action they imply."""
    from sldb.api.stores.store_check import check_store

    report = check_store(store_path, project_root, pythonpath)
    return {"status": "ok" if report["valid"] else "degraded", **_findings(report)}


def _findings(report: dict[str, Any]) -> dict[str, Any]:
    """The findings and the action — empty when nothing broke or moved.

    A finding that needs a decision outranks any safe command: the index holds the only record
    of the value a reindex would overwrite, so it must not be offered as the next step.
    """
    findings = [_entry(f) for f in report["errors"] + report["alerts"]]
    if not findings:
        return {"findings": [], "action": None}
    blocked = [f for f in findings if f["needs_decision"]]
    update = all(f["fix"].endswith("sldb stores update") for f in findings)
    action = f"inspect: {len(blocked)} finding(s) need a decision" if blocked else ("run: sldb stores update" if update else "see each finding's fix")
    return {"findings": findings, "action": action}


def _entry(finding: dict[str, Any]) -> dict[str, Any]:
    """One thing to look at: what it is, whose, how bad, and whether a command fixes it."""
    decide = finding["code"] in _DECIDE and finding["fix"].startswith("decide first")
    return {"kind": finding["code"], "level": finding["level"], "subject": finding["subject"], "explain": finding["what"], "fix": finding["fix"], "needs_decision": decide}
