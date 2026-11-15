"""Resolución de los `refs: [Model:name]` de los elementos contra el store de cada vista, y las
aristas sldb de los átomos.

Migrado de `spec2viz.deskops` (`build_explicit_refs`, `attach_atom_edges`), sobre `SpecView` y
`StoreReader`, con findings `matching/unknown-ref` y `matching/no-store`.
"""

from __future__ import annotations

from sldb.api.matching.matching_findings import finding, raise_if_strict
from sldb.api.matching.spec_view import SpecView
from sldb.api.matching.spec_view_elements import collect_explicit_refs
from sldb.api.matching.store_documents import ref_payload
from sldb.api.matching.store_reader import StoreReader
from sldb.core.finding import Finding


def _ref(view: SpecView, key: str, ref: str, reader: StoreReader, strict: bool, findings: list[Finding]) -> dict | None:
    doc = reader.resolve_ref(view.store, ref) if view.store is not None else None
    if doc is not None:
        return ref_payload(doc) | {"edges": reader.edges_of(view.store, ref)}
    code, where = ("no-store", "sin store sldb para la vista") if view.store is None else ("unknown-ref", "no existe en el store sldb de la vista")
    fix = "declarar el store de la vista" if view.store is None else "crear el documento o corregir la ref"
    findings.append(finding(code, f"{view.key}#{key}", f"{view.id}: ref '{ref}' (nodo '{key}') {where}", fix, strict))
    return None


def _resolve_view(view: SpecView, reader: StoreReader, strict: bool, findings: list[Finding]) -> dict[str, list[dict]]:
    resolved: dict[str, list[dict]] = {}
    for key, refs in collect_explicit_refs(view).items():
        found = [doc for doc in (_ref(view, key, ref, reader, strict, findings) for ref in refs) if doc is not None]
        if found:
            resolved[key] = found
    return resolved


def build_explicit_refs(
    views: list[SpecView], reader: StoreReader | None = None, strict: bool = False
) -> tuple[dict[str, dict[str, list[dict]]], list[Finding]]:
    """`vista -> clave de etiqueta -> [{ref, model, name, title, path, store, summary, edges}]` y
    los findings; con `strict` una ref que no existe lanza `UnknownAtomError`."""
    reader = reader or StoreReader()
    findings: list[Finding] = []
    result = {view.key: _resolve_view(view, reader, strict, findings) for view in views}
    raise_if_strict(findings)
    return {key: resolved for key, resolved in result.items() if resolved}, findings


def _view_atoms(view: SpecView, explicit_atoms: dict, linked_atoms: dict, atoms_by_view: dict) -> list[dict]:
    explicit = [a for entry in (explicit_atoms.get(view.key) or {}).values() for a in entry.get("list") or []]
    fuzzy = [a for entry in (atoms_by_view.get(view.key) or {}).values() for a in (entry.get("atoms") or {}).values()]
    return [*explicit, *linked_atoms.values(), *fuzzy]


def attach_atom_edges(
    views: list[SpecView], explicit_atoms: dict[str, dict[str, dict]], linked_atoms: dict[str, dict],
    reader: StoreReader, atoms_by_view: dict[str, dict[str, dict]] | None = None,
) -> None:
    """Cuelga `edges` (las aristas sldb de `AtomDoc:<id>`) de cada atomo explicito, enlazado o difuso."""
    for view in (v for v in views if v.store is not None):
        for atom in _view_atoms(view, explicit_atoms, linked_atoms, atoms_by_view or {}):
            if atom.get("id") and "edges" not in atom:
                atom["edges"] = reader.edges_of(view.store, f"AtomDoc:{atom['id']}")
