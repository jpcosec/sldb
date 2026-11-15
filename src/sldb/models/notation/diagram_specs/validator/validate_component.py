"""`validate_component`."""

from __future__ import annotations

from sldb.models.notation.diagram_specs.component import ComponentDiagram
from sldb.notations.exceptions import ValidationError

def validate_component(d: ComponentDiagram) -> None:
    node_ids = set(d.data.nodes)
    for edge in d.data.edges:
        if edge.from_ not in node_ids:
            raise ValidationError(f"Edge 'from' references unknown node '{edge.from_}' in {d.id}")
        if edge.to not in node_ids:
            raise ValidationError(f"Edge 'to' references unknown node '{edge.to}' in {d.id}")
