"""What a policy knows of the document a finding is about (docs/architecture/provenance.md §5)."""

from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class Subject:
    """What the policy knows of the document a finding is about."""

    authority: str = "generated"
    declared: bool = False  # True when the block or the model's `__authority__` said so
    by: str = "agent"
    narrative: bool = False  # a model whose template declares no literal heading
