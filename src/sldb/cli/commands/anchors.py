"""`sldb anchors record|check` handlers: alerts by every route, exit by the errors alone. `check`
reports code anchors and, since GO07, document anchors (`check_doc_anchors`, alerts only)."""

from __future__ import annotations

from pathlib import Path
from typing import Any

from sldb.api.anchors import check_anchors, check_doc_anchors, record_anchor
from sldb.api.anchors.anchor_docs import write_anchor
from sldb.cli import alert_sink
from sldb.cli.output_format import emit
from sldb.cli.store_context import get_store_context
from sldb.models.anchor_state import AnchorState


class AnchorsCLI:
    def run(self, args: Any) -> int:
        return {"record": self._record, "check": self._check}[args.anchors_command](args)

    def _record(self, args: Any) -> int:
        _sp, root = get_store_context(args.store, mode="readonly")
        block = record_anchor(root, args.ref)
        if not args.write:
            emit(block, args.format, "\n".join(f"{k}: {v}" for k, v in block.items()))
            return 0
        written = write_anchor(args.store, args.pythonpath, _target(root, args.write), block, args.claim, args.name)
        emit({**block, "written": str(written.path)}, args.format, f"recorded {block['ref']} -> {written.path}")
        return 0

    def _check(self, args: Any) -> int:
        reports, doc_findings = check_anchors(args.store, args.pythonpath, record=args.record), check_doc_anchors(args.store, args.pythonpath)
        findings = [f for r in reports if (f := r.finding())] + doc_findings
        body = {"anchors": [r.as_dict() for r in reports], "doc_anchors": [f.as_dict() for f in doc_findings]}
        emit({**body, "errors": [f.as_dict() for f in findings if f.level == "error"], "alerts": [f.as_dict() for f in findings if f.level == "alert"]}, args.format, _summary(reports, findings, doc_findings))
        alert_sink.report(findings, text=args.format == "text")
        return 1 if any(f.level == "error" for f in findings) else 0


def _target(root: Path, write: str) -> Path:
    return Path(write) if Path(write).is_absolute() else root / write


def _summary(reports: list, findings: list, doc_findings: list) -> str:
    counts = {state.value: sum(r.state is state for r in reports) for state in AnchorState}
    shown = ", ".join(f"{n} {name}" for name, n in counts.items() if n or name == "intact")
    moved = f" — {len(doc_findings)} document anchor(s) moved" if doc_findings else ""
    return f"anchors: {len(reports)} checked — {shown}{moved} — {alert_sink.tally(findings) or 'no findings'}"
