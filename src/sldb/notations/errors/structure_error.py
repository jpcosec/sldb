"""`StructureError`."""

from __future__ import annotations

from sldb.notations.errors.validation_error import ValidationError


class StructureError(ValidationError):
    """Estructura inválida."""
