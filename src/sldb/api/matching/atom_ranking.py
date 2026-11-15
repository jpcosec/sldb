"""Emparejamiento difuso de un texto (la etiqueta de un nodo) con los átomos de un payload.

No es un matcher nuevo: indexa por átomo su título, sus alias y su cuerpo en un `DocumentIndex`
y ordena con `DocumentIndex.rank` (difflib sin red, o el `Embedder` que traiga el `Matcher`).
En spec2viz esto lo hacía el template en el navegador (`findAtomData`).
"""

from __future__ import annotations

import hashlib
from pathlib import Path

from sldb.api.matching.document_index import DocumentIndex
from sldb.api.matching.matcher import Matcher


def atom_index_items(payload: dict[str, dict]) -> list[tuple[str, str, str]]:
    """`(id del átomo, hash del texto, texto)` con el título, los alias y el cuerpo de cada átomo."""
    items: list[tuple[str, str, str]] = []
    for entry in payload.values():
        for atom in (entry.get("atoms") or {}).values():
            if atom.get("id"):
                text = " ".join([str(entry.get("title") or ""), *(entry.get("aliases") or []), str(atom.get("body") or "")])
                items.append((str(atom["id"]), hashlib.sha256(text.encode("utf-8")).hexdigest(), text))
    return items


def rank_atoms(
    payload: dict[str, dict], query: str, cache_path: Path, matcher: Matcher | None = None,
    k: int | None = None, threshold: float = 0.0,
) -> list[tuple[str, float]]:
    """`[(id del átomo, puntaje)]` de mejor a peor para `query`, sobre `threshold`.

    `cache_path` es el archivo derivado del índice (fuera de git); con difflib guarda los textos.
    """
    index = DocumentIndex(matcher or Matcher(), cache_path)
    index.index(atom_index_items(payload))
    return index.rank(query, k=k, threshold=threshold)
