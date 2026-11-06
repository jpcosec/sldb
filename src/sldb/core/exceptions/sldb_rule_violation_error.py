"""Domain error raised when a write breaks a rule of severity `error` (GO08, rules.md §8)."""

from __future__ import annotations

from typing import Any

from .sldb_error import SLDBError


class SLDBRuleViolationError(SLDBError):
    """A write refused by its `on_write` rules: nothing was written.

    `findings` are the error `Finding`s, ordered by the export id of their RuleDoc; the message
    has one line per finding, `<code>: <what>`. In the envelope it is `rules/violation`, exit 1.
    """

    def __init__(self, findings: list[Any]) -> None:
        self.findings = list(findings)
        super().__init__("\n".join(f"{f.code}: {f.what}" for f in self.findings))
