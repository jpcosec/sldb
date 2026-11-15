"""`enforcement_fact`."""

from __future__ import annotations

from typing import Dict, Any
from pydantic import BaseModel, Field


class EnforcementFact(BaseModel):
    """A single atomic fact extracted for enforcement purposes."""

    source: str = Field(description="Subject identifier of the fact.")
    target: str = Field(description="Object identifier of the fact.")
    relation: str = Field(description="The semantic relation between source and target.")
    context: Dict[str, Any] = Field(
        default_factory=dict, description="Condensed 6D context or additional attributes."
    )
