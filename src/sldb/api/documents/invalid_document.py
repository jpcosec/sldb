"""A tracked document its model rejects, as ``load_runtime_documents(..., on_invalid="skip")`` names it."""

from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class InvalidDocument:
    """A tracked document its model rejects: path relative to its project root, the model's
    name and the text of the validation error."""

    path: str
    model: str
    error: str
