"""`UnknownReferenceError`."""

from __future__ import annotations

from sldb.notations.errors.validation_error import ValidationError


class UnknownReferenceError(ValidationError):
    """Un spec o notación nombra un id que no existe."""
