"""Comprobacion de que un `where` parsea en la gramatica de sldb."""

from __future__ import annotations


def _check_where(expression: str) -> None:
    """Un `where` tiene que parsear en la gramatica de sldb; sin sldb instalado no se comprueba."""
    if not expression:
        return
    try:
        from sldb.api import where_matches
    except Exception:  # pragma: no cover
        return
    try:
        where_matches(expression, {})
    except Exception as exc:  # WherePredicateError y afines
        raise ValueError(f"where {expression!r} does not parse: {exc}") from exc
