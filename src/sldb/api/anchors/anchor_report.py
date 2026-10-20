"""What `anchors check` says of one anchor, and the finding it becomes."""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any

from sldb.core.finding import Finding
from sldb.models.anchor_state import AnchorState

_FIX = {
    AnchorState.CHANGED: "look at it; `sldb anchors record <ref> --write <doc>` re-records what it sees",
    AnchorState.RECONNECTED: "`sldb anchors check --record` writes the new ref into the anchor",
    AnchorState.LOST: "re-anchor by hand: `sldb anchors record <new ref> --write <doc>`",
    AnchorState.RENORMALIZE: "re-record the anchor under the current normalization",
    AnchorState.UNPARSEABLE: "fix the file: it does not parse",
    AnchorState.INVALID: "fix the anchor document (ref form, or missing `seen`)",
    AnchorState.UNAVAILABLE: "pip install 'structuredLanguageDB[code]'",
}


@dataclass
class AnchorReport:
    document: str
    ref: str
    state: AnchorState
    changed: list[str] = field(default_factory=list)  # nodes that differ, for `changed`
    to: str | None = None  # the new ref, for `reconnected`
    candidates: list[str] = field(default_factory=list)  # for `lost` with several
    detail: str = ""

    @property
    def level(self) -> str:
        return self.state.level

    def what(self) -> str:
        if self.state is AnchorState.CHANGED:
            return f"changed({'|'.join(self.changed)})"
        if self.state is AnchorState.RECONNECTED:
            return f"reconnected: {self.ref} -> {self.to}"
        if self.state is AnchorState.LOST and self.candidates:
            return f"lost: {len(self.candidates)} candidates ({', '.join(self.candidates)})"
        return f"{self.state.value}{': ' + self.detail if self.detail else ''}"

    def finding(self) -> Finding | None:
        if self.state is AnchorState.INTACT:
            return None
        return Finding(self.level, f"anchors/{self.state.value}", f"CodeAnchorDoc:{self.document}", self.what(), _FIX[self.state], self.document)

    def as_dict(self) -> dict[str, Any]:
        return {"document": self.document, "ref": self.ref, "state": self.state.value, "level": self.level, "changed": self.changed, "to": self.to, "candidates": self.candidates, "detail": self.detail}
