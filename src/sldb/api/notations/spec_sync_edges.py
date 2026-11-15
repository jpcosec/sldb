"""Los `RelationDoc` de las aristas de un spec y los tipos de relacion que usan.

Migrado del cuerpo de `spec2viz.sldb_sync.SpecSync.sync` (tipos de relacion y aristas).
"""

from __future__ import annotations

from pathlib import Path
from typing import Any

from sldb.api.notations.spec_refs import edge_name, node_ref, relation_doc_has_attributes
from sldb.api.notations.sync_report import SyncReport


def ensure_spec_relations(writer: Any, existing: dict, report: SyncReport, edges: list[dict]) -> None:
    """Crea el `RelationTypeDoc` de cada relacion que el spec usa y el store no conoce."""
    for relation in sorted({e["relation"] for e in edges}):
        description = f"Relacion `{relation}` declarada por las aristas del spec `{report.spec_id}`."
        writer.ensure_relation_type(existing, report, relation, description)


def edge_payload(spec_id: str, edge: dict, with_attributes: bool) -> dict[str, Any]:
    """El payload del `RelationDoc` de una arista (con `attributes` si el modelo los tiene)."""
    payload = {
        "title": f"{edge['from']} {edge['relation']} {edge['to']}", "source_id": node_ref(spec_id, edge["from"]),
        "target_id": node_ref(spec_id, edge["to"]), "relation_type": edge["relation"], "condition": edge.get("condition", ""),
        "notes": edge["label"],
    }
    if with_attributes:
        payload["attributes"] = dict(edge.get("attributes") or {})
    return payload


def upsert_edges(writer: Any, existing: dict, report: SyncReport, edges: list[dict], out: Path) -> set[tuple[str, str]]:
    """Upsert de un `RelationDoc` por arista; devuelve sus claves `(modelo, nombre)`."""
    spec_id, with_attributes = report.spec_id, relation_doc_has_attributes()
    names = [edge_name(spec_id, index, len(edges), edge) for index, edge in enumerate(edges, start=1)]
    for name, edge in zip(names, edges):
        payload = edge_payload(spec_id, edge, with_attributes)
        writer.upsert(existing, report, "RelationDoc", name, out / "edges" / f"{name}.md", payload)
    return {("RelationDoc", name) for name in names}
