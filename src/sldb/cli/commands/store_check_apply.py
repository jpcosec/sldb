"""`sldb stores check --apply`: run the policy's answers after the report; the exit code is the errors'."""

from __future__ import annotations

import json
from typing import Any

from sldb.core.finding import split


def exit_after_apply(findings: list, sp: Any, args: Any) -> int:
    """`--apply` after the report; the exit code depends on the errors alone."""
    if getattr(args, "apply", False):
        _apply(findings, sp, args.pythonpath, args.format)
    return 1 if split(findings)[0] else 0


def _apply(findings: list, sp: Any, pythonpath: str | None, fmt: str) -> None:
    """`--apply`: what the policy answers (reindex, hooks), run and listed."""
    from sldb.api.stores.apply_findings import apply_findings

    ran = apply_findings(findings, sp, pythonpath)
    if fmt in ("json", "yaml"):
        print(json.dumps({"applied": ran}))
    else:
        print("\n".join(f"applied: {r['response']} for {r['subject']}: {'ok' if r['ok'] else 'FAILED'}" for r in ran) or "applied: nothing to run")
