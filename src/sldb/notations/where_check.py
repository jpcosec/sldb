"""Comprobacion de que un `where` parsea: un puerto que `sldb.api.notations` conecta al parser."""

from __future__ import annotations

from typing import Callable

_parser: Callable[[str], object] | None = None


def connect_where_check(parser: Callable[[str], object] | None) -> None:
    """Conecta (o desconecta) el parser de `where`; sin parser no se comprueba."""
    global _parser
    _parser = parser


def _check_where(expression: str) -> None:
    """Un `where` tiene que parsear en la gramatica de sldb; sin parser conectado no se comprueba."""
    if not expression or _parser is None:
        return
    try:
        _parser(expression)
    except Exception as exc:  # WherePredicateError y afines
        raise ValueError(f"where {expression!r} does not parse: {exc}") from exc
