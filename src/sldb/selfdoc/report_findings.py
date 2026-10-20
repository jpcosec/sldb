"""A selfdoc report as findings: what broke (error) apart from what the source moved (alert).

docs/architecture/anchoring.md §4: generated fields gone stale, documents not yet generated or
tracked, stale hashes, symbols or commands removed, a rename hint and a stale source graph are
alerts. Malformed metadata, repeated ids and a graph missing or unreadable are errors.
"""
from __future__ import annotations

from sldb.core.finding import Finding, alert, error

_SYNC = "sldb selfdoc sync (python-sync for the Python variants)"
_ALERTS = (
    ("missing", "selfdoc/missing", "not generated yet"),
    ("changed", "selfdoc/changed", "its generated fields are stale"),
    ("untracked", "selfdoc/untracked", "not tracked in the store"),
    ("stale_indexes", "selfdoc/stale-index", "its index hash is stale"),
    ("removed", "selfdoc/removed", "its symbol or command is gone from the source; the document is kept"),
    ("graph_stale", "selfdoc/graph-stale", "the source graph is stale against the scanned AST"),
)


def report_findings(report) -> list[Finding]:
    """Every finding of `report`, errors first."""
    errors = [error("selfdoc/metadata", "docstring", m) for m in report.metadata_errors]
    errors += [error("selfdoc/graph", g, "the source graph is missing or unreadable", _SYNC) for g in report.graph_errors]
    alerts = [alert(code, subject, what, _SYNC) for field, code, what in _ALERTS for subject in getattr(report, field)]
    return errors + alerts + [alert("selfdoc/renamed", r.get("from", "?"), f"maybe renamed to {r.get('to', '?')} (an unverified hint)") for r in report.renamed]


def report_payload(report) -> dict:
    """The JSON `selfdoc check` prints: `ok`, the report's fields, and its findings by level."""
    found = report_findings(report)
    listed = {"errors": [f.as_dict() for f in found if f.level == "error"], "alerts": [f.as_dict() for f in found if f.level == "alert"]}
    return {"ok": report.ok, **report.model_dump(), **listed}
