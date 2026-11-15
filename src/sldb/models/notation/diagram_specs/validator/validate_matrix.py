"""`validate_matrix`."""

from __future__ import annotations

from sldb.models.notation.diagram_specs.matrix import MatrixDiagram
from sldb.notations.exceptions import ValidationError

def _check_components(diagram_id, view_id, valid_stages, components):
    for comp in components:
        for sid in comp.stages.get(view_id, []):
            if sid not in valid_stages:
                raise ValidationError(
                    f"Component '{comp.name}' references unknown stage '{sid}' "
                    f"in view '{view_id}' in {diagram_id}"
                )
        _check_components(diagram_id, view_id, valid_stages, comp.children)


def validate_matrix(d: MatrixDiagram) -> None:
    for view in d.data.views:
        valid_stages = {s.id for s in view.stages}
        _check_components(d.id, view.id, valid_stages, d.data.components)
