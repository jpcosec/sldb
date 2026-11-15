"""Los `atoms:` y `refs:` de los elementos de los specs de una vista, por clave de etiqueta.

Migrado de `spec2viz.deskops` (`_spec_elements`, `collect_explicit_atoms`, `collect_explicit_refs`);
las colecciones por tipo y la lectura de una colección (mapa o lista) se reutilizan de
`sldb.api.notations`. Se indexa por etiqueta e id normalizados porque el template solo ve el
texto del nodo renderizado.
"""

from __future__ import annotations

from sldb.api.matching.atom_keys import label_key
from sldb.api.matching.spec_view import SpecView
from sldb.api.notations.spec_element import pairs
from sldb.api.notations.spec_sync_constants import _ELEMENT_COLLECTIONS


def _element(eid: str, el: object) -> tuple[str, str, list[str], list[str]]:
    el = el if isinstance(el, dict) else {}
    atoms = [str(a) for a in (el.get("atoms") or [])]
    refs = [str(r) for r in (el.get("refs") or [])]
    return (str(eid), str(el.get("label") or eid), atoms, refs)


def spec_view_elements(spec: dict) -> list[tuple[str, str, list[str], list[str]]]:
    """(id, label, atoms, refs) de cada elemento del spec que el catalogo puede mostrar."""
    data = spec.get("data") or {}
    collections = _ELEMENT_COLLECTIONS.get(str(spec.get("type")), ())
    return [_element(eid, el) for c in collections for eid, el in pairs(data.get(c) or {}) if eid]


def _add(explicit: dict[str, list[str]], eid: str, label: str, values: list[str]) -> None:
    for key in {label_key(label), label_key(eid)}:
        bucket = explicit.setdefault(key, [])
        bucket.extend(v for v in values if v not in bucket)


def collect_explicit_atoms(view: SpecView) -> tuple[dict[str, list[str]], int, int]:
    """Mapa `clave de etiqueta -> [atom-id]` de los specs de la vista, total de elementos y cuantos traen `atoms`."""
    explicit: dict[str, list[str]] = {}
    total = with_atoms = 0
    for spec in view.specs:
        for eid, label, atoms, _refs in spec_view_elements(spec):
            total += 1
            if atoms:
                with_atoms += 1
                _add(explicit, eid, label, atoms)
    return explicit, total, with_atoms


def collect_explicit_refs(view: SpecView) -> dict[str, list[str]]:
    """Mapa `clave de etiqueta -> [ref]` de los `refs:` de los elementos de la vista."""
    explicit: dict[str, list[str]] = {}
    for spec in view.specs:
        for eid, label, _atoms, refs in spec_view_elements(spec):
            if refs:
                _add(explicit, eid, label, refs)
    return explicit
