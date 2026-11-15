"""`node_parents`: el padre de cada nodo de un despliegue."""

from __future__ import annotations

from sldb.models.notation.diagram_specs.deployment import DeploymentDiagram
from sldb.notations.exceptions import StructureError, UnknownReferenceError

def _add_child(parent: dict, kind_of: dict, nid: str, ref: str, d_id: str) -> None:
    if ref not in kind_of:
        raise UnknownReferenceError(f"Node '{nid}' contains unknown node or artifact '{ref}' in {d_id}")
    if kind_of[ref] != "node":
        return
    if ref == nid:
        raise StructureError(f"Node '{nid}' contains itself in {d_id}")
    if ref in parent:
        raise StructureError(f"Node '{ref}' is contained by both '{parent[ref]}' and '{nid}' in {d_id}")
    parent[ref] = nid


def node_parents(d: DeploymentDiagram, kind_of: dict) -> dict[str, str]:
    parent: dict[str, str] = {}
    for nid, node in d.data.nodes.items():
        for ref in node.contains:
            _add_child(parent, kind_of, nid, ref, d.id)
    return parent
