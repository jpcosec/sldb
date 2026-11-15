"""El filtro de átomos por etiqueta. Migrado de `spec2viz.deskops` (`_tag_matches`, `filter_atoms_payload`)."""

from __future__ import annotations


def tag_matches(tag: str, wanted: str) -> bool:
    """`wanted` calza con el tag completo (`ns:valor`) o con su valor sin namespace."""
    tag = str(tag).strip().lower()
    wanted = wanted.strip().lower()
    return tag == wanted or (":" in tag and tag.split(":", 1)[1] == wanted)


def _kept(entry: dict, tags: list[str]) -> dict:
    return {
        question: atom
        for question, atom in (entry.get("atoms") or {}).items()
        if any(tag_matches(t, w) for t in (atom.get("tags") or []) for w in tags)
    }


def filter_atoms_payload(payload: dict[str, dict], tags: list[str] | None) -> dict[str, dict]:
    """Deja solo los atomos que tengan al menos uno de `tags`; sin `tags` no filtra."""
    if not tags:
        return payload
    filtered: dict[str, dict] = {}
    for key, entry in payload.items():
        kept = _kept(entry, tags)
        if kept:
            filtered[key] = {**entry, "atoms": kept}
    return filtered
