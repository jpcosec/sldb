"""`UnknownIconError`."""

from __future__ import annotations

from sldb.notations.errors.validation_error import ValidationError


class UnknownIconError(ValidationError):
    """Un icono no está en el conjunto de iconos declarado."""
