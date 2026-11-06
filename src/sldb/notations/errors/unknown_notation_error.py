"""`UnknownNotationError`."""

from __future__ import annotations

from sldb.notations.errors.validation_error import ValidationError


class UnknownNotationError(ValidationError):
    """Una notación no resuelve a un archivo, builtin ni documento del store."""
