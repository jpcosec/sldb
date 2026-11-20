"""Los átomos de cada vista: los `AtomDoc` del store de la vista, o los de una carpeta de respaldo.

Migrado de `spec2viz.deskops` (`build_atoms_by_view`, `_raw_atoms_by_view`), sobre `SpecView`
y `StoreReader`.
"""

from __future__ import annotations

import json
from pathlib import Path

from sldb.api.matching.atom_payload import parse_atoms
from sldb.api.matching.atom_tags import filter_atoms_payload
from sldb.api.matching.spec_view import SpecView
from sldb.api.matching.store_reader import StoreReader
from sldb.core.finding import Finding


def raw_atoms_by_view(
    views: list[SpecView], atoms_dir: Path | None = None, reader: StoreReader | None = None
) -> tuple[dict[str, dict[str, dict]], list[Finding]]:
    """`vista -> payload`: con `atoms_dir`, los átomos de esa carpeta para todas las vistas (no se consulta ningún store); sin él, los del store de cada vista."""
    reader = reader or StoreReader()
    findings: list[Finding] = []
    if atoms_dir:
        payload = json.loads(parse_atoms(atoms_dir, findings))
        atoms_by_view = {view.key: payload for view in views}
    else:
        atoms_by_view = {view.key: reader.atoms(view.store) if view.store is not None else {} for view in views}
    return atoms_by_view, [*reader.findings, *findings]


def build_atoms_by_view(
    views: list[SpecView], atoms_dir: Path | None = None, atoms_tags: list[str] | None = None, reader: StoreReader | None = None
) -> tuple[dict[str, dict[str, dict]], list[Finding]]:
    """`raw_atoms_by_view` filtrado por `atoms_tags` (sin tags no filtra)."""
    atoms_by_view, findings = raw_atoms_by_view(views, atoms_dir, reader)
    if atoms_tags:
        atoms_by_view = {k: filter_atoms_payload(v, atoms_tags) for k, v in atoms_by_view.items()}
    return atoms_by_view, findings
