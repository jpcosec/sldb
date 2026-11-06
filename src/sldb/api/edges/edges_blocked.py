"""Edges a subject's `on_transition` rules block (GO08, rules.md §9): the other half of
`edges_holding`."""

from __future__ import annotations

from pathlib import Path
from typing import Any, Iterable

from sldb.api.edges.edges_holding import transition
from sldb.store.models import EdgeRecord


def edges_blocked(store: str | Path | None, export_id: str, subject: dict[str, Any], relation: str | None = None, include_linked: bool = True, exclude_tags: Iterable[str] = (), document: str | None = None) -> list[EdgeRecord]:
    """The edges leaving `export_id` whose condition holds on `subject` but that an `error`
    finding of an `on_transition` rule on `document` blocks, each with `effects` and `findings`
    (every finding of the subject: errors and alerts). Empty when no error is found, and
    without `document` (no rule runs). Arguments as in `edges_holding`."""
    held, findings = transition(store, export_id, subject, relation, include_linked, exclude_tags, document)
    if not any(f.level == "error" for f in findings or []):
        return []
    return [e.model_copy(update={"findings": findings}) for e in held]
