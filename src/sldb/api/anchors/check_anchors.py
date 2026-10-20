"""Every code anchor of a store against the code now (code-anchoring.md §4): read-only unless
`record`, which writes the reconnections (new `ref`, a `history` entry) and nothing else.
"""

from __future__ import annotations

from pathlib import Path
from typing import Any

from sldb.api.anchors.anchor_report import AnchorReport
from sldb.api.anchors.reconnect import candidates
from sldb.api.anchors.record_anchor import symbol_of, symbols_of
from sldb.models.anchor_state import AnchorState
from sldb.models.code_ref import parse_code_ref
from sldb.code.fingerprints import NORMALIZATION
from sldb.code.runtime import TreeSitterUnavailable

_NODES = ("signature", "docstring", "body")


def check_anchors(store: str | Path | None, pythonpath: str | None = None, record: bool = False) -> list[AnchorReport]:
    """One report per tracked `CodeAnchorDoc`, in store order."""
    from sldb.api.anchors.anchor_docs import anchor_documents, record_reconnection

    reports = []
    for doc in anchor_documents(store, pythonpath):
        report = check_one(doc.root, doc.name, doc.payload)
        if record and report.state is AnchorState.RECONNECTED:
            record_reconnection(store, pythonpath, doc, report.to)
        reports.append(report)
    return reports


def check_one(root: Path, name: str, payload: dict[str, Any]) -> AnchorReport:
    """The state of one anchor payload against the code under `root`."""
    ref, seen = str(payload.get("ref", "")), payload.get("seen")
    parsed = parse_code_ref(ref)
    if parsed is None or not isinstance(seen, dict) or "body" not in seen:
        return AnchorReport(name, ref, AnchorState.INVALID, detail="ref form or `seen` block")
    if int(payload.get("normalization", 0) or 0) != NORMALIZATION:
        return AnchorReport(name, ref, AnchorState.RENORMALIZE, detail=f"recorded under normalization {payload.get('normalization')}, current is {NORMALIZATION}")
    try:
        return _compare(root, name, ref, parsed, str(payload.get("kind", "")), seen)
    except TreeSitterUnavailable as exc:
        return AnchorReport(name, ref, AnchorState.UNAVAILABLE, detail=str(exc))


def _compare(root: Path, name: str, ref: str, parsed: tuple[str, str], kind: str, seen: dict) -> AnchorReport:
    path, qualified = parsed
    facts = symbols_of(root, path)
    if facts and facts[0]["attrs"].get("has_error"):
        return AnchorReport(name, ref, AnchorState.UNPARSEABLE, detail=path)
    found = symbol_of(root, path, qualified) if facts else None
    if found is not None:
        differs = [node for node in _NODES if found["fingerprints"].get(node) != seen.get(node)]
        return AnchorReport(name, ref, AnchorState.CHANGED, changed=differs) if differs else AnchorReport(name, ref, AnchorState.INTACT)
    return _reconnected_or_lost(name, ref, candidates(root, path, kind, seen, facts))


def _reconnected_or_lost(name: str, ref: str, options: list[str]) -> AnchorReport:
    if len(options) == 1:
        return AnchorReport(name, ref, AnchorState.RECONNECTED, to=options[0])
    return AnchorReport(name, ref, AnchorState.LOST, candidates=options, detail="no symbol by that name" if not options else "")
