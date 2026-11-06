"""`AmbiguousPathError`."""

from __future__ import annotations

from sldb.notations.errors.validation_error import ValidationError


class AmbiguousPathError(ValidationError):
    """Ruta ambigua en la resolución."""
