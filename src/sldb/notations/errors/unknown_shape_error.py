"""`UnknownShapeError`."""

from __future__ import annotations

from sldb.notations.errors.validation_error import ValidationError


class UnknownShapeError(ValidationError):
    """Una forma no es una primitiva reconocida."""
