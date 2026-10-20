"""What a command reports besides its output: an error or an alert (docs/architecture/anchoring.md, §4).

An **error** is something broken or a violated contract, and fails the command. An **alert**
is a source that moved against what was recorded: the state is valid, the command exits 0,
and the alert is never silent (`sldb.cli.alert_sink` prints it by every route).
"""

from __future__ import annotations

from dataclasses import asdict, dataclass
from typing import Literal

Level = Literal["error", "alert"]


@dataclass(frozen=True)
class Finding:
    """One finding: its level, a stable `ns/name` code, whose it is, what moved, what to do."""

    level: Level
    code: str
    subject: str
    what: str
    fix: str = ""
    document: str | None = None

    def as_dict(self) -> dict:
        return asdict(self)

    def line(self) -> str:
        return f"{self.level}: [{self.code}] {self.subject}: {self.what}"


def alert(code: str, subject: str, what: str, fix: str = "", document: str | None = None) -> Finding:
    return Finding("alert", code, subject, what, fix, document)


def error(code: str, subject: str, what: str, fix: str = "", document: str | None = None) -> Finding:
    return Finding("error", code, subject, what, fix, document)


def split(findings: list[Finding]) -> tuple[list[Finding], list[Finding]]:
    """`(errors, alerts)`, each in the order given."""
    return [f for f in findings if f.level == "error"], [f for f in findings if f.level == "alert"]
