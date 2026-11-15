"""`ParseError`."""

from __future__ import annotations

from sldb.notations.errors.notation_error import NotationError


class ParseError(NotationError):
    """El fichero de un spec no se pudo leer: no existe, YAML mal formado, tipo desconocido o esquema inválido."""
