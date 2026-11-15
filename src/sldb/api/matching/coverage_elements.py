"""La cobertura de un elemento de diagrama: facetas esperadas, cubiertas por átomos y faltantes.

Migrado de `spec2viz.deskops` (`_project_element_payload`, `_source_field_for`).
"""

from __future__ import annotations

_SOURCE_FIELDS = {
    ("component", "node", "what"): "label",
    ("component", "edge", "how"): "semantics.relation",
    ("component", "edge", "why"): "semantics.relation",
    ("state", "state", "what"): "label",
    ("state", "transition", "how"): "semantics.action",
    ("state", "transition", "when"): "semantics.on",
    ("state", "transition", "why"): "semantics.guard",
}


def source_field_for(semantics: dict, facet: str) -> str:
    """El campo del elemento que responde una faceta, por tipo de diagrama y de elemento."""
    return _SOURCE_FIELDS.get((semantics.get("diagram_type"), semantics.get("element_kind"), facet), "label")


def _expected(edge: dict, semantics: dict, nodes: dict[str, dict]) -> dict | None:
    metadata = edge.get("metadata", {})
    facet_node = nodes.get(edge.get("target_id"))
    facet_name = metadata.get("facet") or facet_node.get("semantics", {}).get("facet") if facet_node else None
    if not facet_name:
        return None
    return {"facet": facet_name, "facet_node_id": edge.get("target_id"), "source_field": metadata.get("source_field") or source_field_for(semantics, facet_name)}


def _covered(edge: dict) -> dict | None:
    metadata = edge.get("metadata", {})
    facet_name, atom_id = metadata.get("facet"), metadata.get("atom_id")
    if not facet_name or not atom_id:
        return None
    return {"facet": facet_name, "facet_node_id": f"facet:{facet_name}", "atom_id": atom_id, "atom_node_id": edge.get("target_id"),
            "score": metadata.get("score", 0.0), "match_basis": metadata.get("match_basis"), "evidence": metadata.get("evidence")}


def _facets(element_node: dict, nodes: dict[str, dict]) -> tuple[list[dict], list[dict]]:
    semantics, edges = element_node.get("semantics", {}), element_node.get("edges", [])
    expected = [e for e in (_expected(x, semantics, nodes) for x in edges if x.get("relation_type") == "expects_facet") if e]
    covered = [c for c in (_covered(x) for x in edges if x.get("relation_type") == "covers_facet") if c]
    return sorted(expected, key=lambda item: item["facet"]), sorted(covered, key=lambda item: (item["facet"], item["atom_id"]))


def _ratio(expected: list[dict], covered: list[dict]) -> float:
    names = {entry["facet"] for entry in expected}
    return round(len({item["facet"] for item in covered if item["facet"] in names}) / len(expected), 4) if expected else 0.0


def element_payload(element_node: dict, nodes: dict[str, dict]) -> dict:
    """element_id, nodo, kind, label, source, target, facetas esperadas, cubiertas, faltantes y ratio."""
    semantics = element_node.get("semantics", {})
    expected, covered = _facets(element_node, nodes)
    covered_names = {item["facet"] for item in covered}
    return {
        "element_id": semantics.get("element_id") or "", "element_node_id": element_node.get("identity", {}).get("node_id"),
        "element_kind": semantics.get("element_kind") or "", "label": semantics.get("label"),
        "source": semantics.get("source"), "target": semantics.get("target"),
        "expected_facets": expected, "covered_facets": covered,
        "missing_facets": [item for item in expected if item["facet"] not in covered_names], "coverage_ratio": _ratio(expected, covered),
    }
