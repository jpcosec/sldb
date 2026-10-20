"""The one way a finding leaves the CLI, so an alert is never silent.

`report` prints each finding as a line in text mode (a JSON payload carries them instead),
writes a `::warning`/`::error` annotation to stderr under GitHub Actions, and keeps every alert
for the envelope's `warnings` (`sldb.cli.envelope`). `tally` is the closing count.
"""

from __future__ import annotations

import os
import sys

from sldb.core.finding import Finding, split

_KEPT: list[dict] = []


def report(findings: list[Finding], text: bool = True) -> None:
    """Every finding by every route; `text=False` when the command printed them in its JSON."""
    _KEPT.extend(f.as_dict() for f in findings if f.level == "alert")
    for finding in findings:
        if text:
            print(finding.line() + (f"\n    fix     : {finding.fix}" if finding.fix else ""))
        if os.environ.get("GITHUB_ACTIONS") == "true":
            print(_annotation(finding), file=sys.stderr)


def tally(findings: list[Finding]) -> str:
    """`2 error(es), 3 alerta(s)`, or empty when there are none."""
    errors, alerts = split(findings)
    return ", ".join(f"{n} {label}" for n, label in ((len(errors), "error(es)"), (len(alerts), "alerta(s)")) if n)


def kept() -> list[dict]:
    return list(_KEPT)


def forget() -> None:
    _KEPT.clear()


def _annotation(finding: Finding) -> str:
    kind = "warning" if finding.level == "alert" else "error"
    message = f"{finding.subject}: {finding.what}".replace("%", "%25").replace("\r", "%0D").replace("\n", "%0A")
    return f"::{kind} title={finding.code}::{message}"
