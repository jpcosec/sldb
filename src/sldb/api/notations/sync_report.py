"""What a sync created, updated, deleted and could not resolve."""

from __future__ import annotations

from dataclasses import asdict, dataclass, field
from typing import Any


@dataclass
class SyncReport:
    """The outcome of synchronizing a notation or palette."""

    spec_id: str
    created: list[str] = field(default_factory=list)
    updated: list[str] = field(default_factory=list)
    deleted: list[str] = field(default_factory=list)
    relation_types_added: list[str] = field(default_factory=list)
    notation: str = ""
    unresolved: list[str] = field(default_factory=list)
    edge_errors: list[str] = field(default_factory=list)
    problems: list[str] = field(default_factory=list)

    def to_dict(self) -> dict[str, Any]:
        """A plain dict copy of the report."""
        return asdict(self)
