"""`enforcement_artifact`."""

from __future__ import annotations

from typing import List
from pydantic import BaseModel, ConfigDict, Field

from sldb.models.notation.diagram_specs.reflection.enforcement_fact import EnforcementFact


class EnforcementArtifact(BaseModel):
    """Condensed version of the IR for consumption by linters, auditors, and gates."""

    model_config = ConfigDict(extra="forbid")

    fingerprint: str = Field(
        description="Hash or version identifier to ensure artifact integrity."
    )
    facts: List[EnforcementFact] = Field(
        description="List of atomic facts that form the enforcement surface."
    )
