"""Las aristas declaradas de un documento, en ambos sentidos, sobre `edges_from`/`edges_to` de sldb.api.

Migrado de `spec2viz.deskops.SldbAtomResolver.edges_of`. Las relaciones que el índice de aristas
fabrica solo de la estructura (secciones, tags, campos, modelos) no las declaró nadie y se omiten.
"""

from __future__ import annotations

from pathlib import Path

from sldb.api.edges.edge_reading import edges_from, edges_to, load_edge_index

STRUCTURAL_RELATIONS = frozenset(
    {
        "has_section", "tagged_as", "has_document", "has_field", "has_model", "names",
        "semantic_parent", "semantic_equivalent", "applies_to_source", "applies_to_target",
    }
)
_DOC_NODE_PREFIX = "sldb://document/"


def _edge(record, direction: str, titles: dict[str, str]) -> dict:
    other = str(record.target if direction == "out" else record.source)
    other_ref = other[len(_DOC_NODE_PREFIX):] if other.startswith(_DOC_NODE_PREFIX) else ""
    return {"relation": str(record.relation), "direction": direction, "node": other, "ref": other_ref, "title": titles.get(other_ref, other_ref or other)}


def edges_of(store_path: Path, ref: str, titles: dict[str, str]) -> list[dict]:
    """`relation`, `direction` (`out`/`in`), `node`, `ref` (`Model:name` o vacío) y `title` de
    cada arista declarada que toca `ref`. Sin índice de aristas, lanza lo que lance sldb."""
    return [
        _edge(record, direction, titles)
        for direction, records in (("out", edges_from(store_path, ref)), ("in", edges_to(store_path, ref)))
        for record in records
        if record.relation not in STRUCTURAL_RELATIONS
    ]


def edges_of_index(index, ref: str, titles: dict[str, str]) -> list[dict]:
    """Lo mismo que `edges_of`, sobre un índice ya cargado (una carga por store, no por referencia)."""
    return [
        _edge(record, direction, titles)
        for direction, records in (("out", index.edges_from(ref, None)), ("in", index.edges_to(ref, None)))
        for record in records
        if record.relation not in STRUCTURAL_RELATIONS
    ]


def load_index(store_path: Path):
    """El índice de aristas del store con enlaces, el que leen `edges_from` y `edges_to`."""
    return load_edge_index(store_path)
