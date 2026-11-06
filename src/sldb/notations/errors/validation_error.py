"""`ValidationError`."""

from __future__ import annotations

from sldb.notations.errors.notation_error import NotationError


class ValidationError(NotationError):
    """Error de validación semántica de una notación o paleta."""
