"""Serializable facts about one argparse argument."""
from __future__ import annotations

from pydantic import BaseModel, Field


class ArgumentRecord(BaseModel):
    """Describe a positional argument or option without executing it."""

    names: list[str] = Field(description="Option spellings or positional destination.")
    required: bool = Field(description="Whether argparse requires this argument.")
    default: str = Field(description="JSON default, or the literal SUPPRESS sentinel.")
    choices: list[str] | None = Field(description="JSON choices when constrained.")
    nargs: str | int | None = Field(description="Argparse cardinality.")
    value_type: str | None = Field(description="Qualified name of the value converter.")
    action: str = Field(description="Qualified argparse action class.")
    const: str = Field(description="JSON constant used by flag/optional-value actions.")
    help: str = Field(description="Declared argument help text.")
