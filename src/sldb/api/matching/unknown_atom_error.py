"""`UnknownAtomError`: un spec referencia un átomo o una ref que no existe (modo estricto).

Migrado de `spec2viz.deskops`; ahora lleva los findings de nivel error que la causaron.
"""

from __future__ import annotations

from sldb.core.finding import Finding


class UnknownAtomError(ValueError):
    """Un spec referencia un atomo que no existe entre los cargados (`--strict-atoms`)."""

    def __init__(self, findings: list[Finding]):
        self.findings = list(findings)
        super().__init__("; ".join(f.line() for f in self.findings))
