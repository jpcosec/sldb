"""La cobertura de una vista: su resumen y sus elementos, o el payload vacío si el grafo no la tiene.

Migrado de `spec2viz.deskops` (`_project_view_payload`, `_empty_coverage_payload`), sobre `SpecView`.
"""

from __future__ import annotations

from statistics import mean

from sldb.api.matching.coverage_elements import element_payload
from sldb.api.matching.spec_view import SpecView


def _summary(elements: list[dict]) -> dict:
    ratios = [element["coverage_ratio"] for element in elements]
    return {
        "total_elements": len(elements),
        "elements_fully_covered": sum(1 for e in elements if e["expected_facets"] and not e["missing_facets"]),
        "avg_coverage_ratio": round(mean(ratios), 4) if ratios else 0.0,
        "expected_facet_count": sum(len(e["expected_facets"]) for e in elements),
        "covered_facet_count": sum(len({entry["facet"] for entry in e["covered_facets"]}) for e in elements),
        "missing_facet_count": sum(len(e["missing_facets"]) for e in elements),
    }


def empty_coverage_payload(view: SpecView) -> dict:
    """La cobertura de una vista que el grafo no tiene: sin elementos y con el resumen en cero."""
    return {"view_id": view.key, "view_node_id": None, "diagram_type": view.diagram_type or "", "title": view.title,
            "source_ref": "", "scope": view.scope or "", "summary": _summary([]), "elements": []}


def _elements(view_node: dict, nodes: dict[str, dict]) -> list[dict]:
    edges = sorted(view_node.get("edges", []), key=lambda edge: edge.get("target_id", ""))
    targets = [nodes.get(edge.get("target_id")) for edge in edges if edge.get("relation_type") == "contains"]
    return [element_payload(node, nodes) for node in targets if node]


def view_payload(view: SpecView, view_node: dict, nodes: dict[str, dict]) -> dict:
    """La cobertura de la vista según su nodo `view` del grafo y los elementos que contiene."""
    semantics, elements = view_node.get("semantics", {}), _elements(view_node, nodes)
    return {
        "view_id": view.key, "view_node_id": view_node.get("identity", {}).get("node_id"),
        "diagram_type": semantics.get("diagram_type") or view.diagram_type or "",
        "title": semantics.get("title") or view.title,
        "source_ref": semantics.get("source_ref") or view.source or "",
        "scope": semantics.get("scope") or view.scope or "",
        "summary": _summary(elements), "elements": sorted(elements, key=lambda element: element["element_id"]),
    }
