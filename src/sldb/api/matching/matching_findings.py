"""Los avisos del emparejamiento con el formato de findings de sldb (level, code, subject, what, fix).

Sustituyen a `AtomBuildWarning` y `CoverageBuildWarning` de `spec2viz.deskops`. Nivel warning;
con `strict`, error, y `raise_if_strict` lanza `UnknownAtomError` con ellos. La lógica no
imprime: imprime quien llama.
"""

from __future__ import annotations

from sldb.api.matching.unknown_atom_error import UnknownAtomError
from sldb.core.finding import Finding


def finding(code: str, subject: str, what: str, fix: str = "", strict: bool = False) -> Finding:
    """Un finding `matching/<code>`: warning, o error con `strict`."""
    return Finding("error" if strict else "warning", f"matching/{code}", subject, what, fix)


def raise_if_strict(findings: list[Finding]) -> None:
    """Lanza `UnknownAtomError` con los findings de nivel error, si hay alguno."""
    errors = [f for f in findings if f.level == "error"]
    if errors:
        raise UnknownAtomError(errors)
