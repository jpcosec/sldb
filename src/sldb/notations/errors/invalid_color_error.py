"""`InvalidColorError`."""

from __future__ import annotations

from sldb.notations.errors.validation_error import ValidationError


class InvalidColorError(ValidationError):
    """Un color no es un token de paleta ni un hex `#rrggbb`."""
