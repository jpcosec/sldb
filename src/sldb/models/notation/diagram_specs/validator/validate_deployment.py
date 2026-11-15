"""`validate_deployment`."""

from __future__ import annotations

from sldb.models.notation.diagram_specs.deployment import DeploymentDiagram
from sldb.models.notation.diagram_specs.validator.check_connections import check_connections
from sldb.models.notation.diagram_specs.validator.containment import check_containment_cycles
from sldb.models.notation.diagram_specs.validator.deployment_parents import node_parents
from sldb.notations.exceptions import StructureError

def validate_deployment(d: DeploymentDiagram) -> None:
    nodes, artifacts = d.data.nodes, d.data.artifacts
    for both in sorted(set(nodes) & set(artifacts)):
        raise StructureError(f"Id '{both}' is both a node and an artifact in {d.id}")
    kind_of = {**{a: "artifact" for a in artifacts}, **{n: "node" for n in nodes}}
    parent = node_parents(d, kind_of)
    check_containment_cycles(parent, nodes, "Node", d.id)
    check_connections(d, kind_of)
