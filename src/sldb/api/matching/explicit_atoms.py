"""Resolución de los `atoms: [id]` de los elementos de los specs contra los átomos cargados.

Migrado de `spec2viz.deskops` (`_atom_index`, `build_explicit_atoms`), sobre `SpecView` en vez
de `CatalogItem` y con findings `matching/unknown-atom` en vez de `AtomBuildWarning`.
"""

from __future__ import annotations

import re

from sldb.api.matching.matching_findings import finding, raise_if_strict
from sldb.api.matching.spec_view import SpecView
from sldb.api.matching.spec_view_elements import collect_explicit_atoms
from sldb.core.finding import Finding

_WIKILINK = re.compile(r"\[\[([^\[\]]+?)\]\]")


def atom_index(payload: dict[str, dict]) -> dict[str, dict]:
    """`id -> {id, title, question, body}` de los átomos de un payload por título."""
    return {
        str(atom["id"]): {"id": atom["id"], "title": entry.get("title", ""), "question": question, "body": atom.get("body", "")}
        for entry in payload.values()
        for question, atom in (entry.get("atoms") or {}).items()
        if atom.get("id")
    }


def _link(found: list[dict], index: dict[str, dict], linked: dict[str, dict]) -> None:
    """Los átomos que los encontrados enlazan con `[[id]]`, un nivel."""
    for atom in found:
        for target in _WIKILINK.findall(atom.get("body") or ""):
            if target.strip() in index:
                linked[target.strip()] = index[target.strip()]


def _found(view: SpecView, key: str, ids: list[str], index: dict[str, dict], strict: bool, findings: list[Finding]) -> list[dict]:
    for atom_id in (a for a in ids if a not in index):
        what = f"{view.id}: atomo '{atom_id}' (nodo '{key}') no existe entre los atomos cargados"
        findings.append(finding("unknown-atom", f"{view.key}#{key}", what, "crear el átomo o corregir el id", strict))
    return [index[a] for a in ids if a in index]


def _resolve_view(view: SpecView, payload: dict[str, dict], strict: bool, findings: list[Finding], linked: dict[str, dict]) -> tuple[dict[str, dict], bool]:
    """`clave -> {title, explicit, list}` de la vista y si todos sus elementos son explícitos."""
    explicit, total, with_atoms = collect_explicit_atoms(view)
    index, resolved = atom_index(payload), {}
    for key, ids in explicit.items():
        found = _found(view, key, ids, index, strict, findings)
        if found:
            resolved[key] = {"title": key, "explicit": True, "list": found}
            _link(found, index, linked)
    return resolved, bool(explicit and total and with_atoms == total and len(resolved) == len(explicit))


def build_explicit_atoms(
    views: list[SpecView], raw_atoms_by_view: dict[str, dict[str, dict]], strict: bool = False
) -> tuple[dict[str, dict[str, dict]], set[str], list[Finding], dict[str, dict]]:
    """(`vista -> clave -> {title, explicit, list}`, vistas totalmente explícitas, findings,
    `id -> átomo` de los enlazados con `[[id]]` desde los explícitos, un nivel). Con `strict`,
    un átomo que no existe lanza `UnknownAtomError`."""
    linked: dict[str, dict] = {}
    result: dict[str, dict[str, dict]] = {}
    complete: set[str] = set()
    findings: list[Finding] = []
    for view in views:
        resolved, full = _resolve_view(view, raw_atoms_by_view.get(view.key) or {}, strict, findings, linked)
        result.update({view.key: resolved} if resolved else {})
        complete.update({view.key} if full else set())
    raise_if_strict(findings)
    return result, complete, findings, linked
