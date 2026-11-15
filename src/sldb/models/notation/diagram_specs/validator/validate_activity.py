"""`validate_activity`."""

from __future__ import annotations

from sldb.models.notation.diagram_specs.activity import ActivityDiagram
from sldb.notations.exceptions import StructureError, UnknownReferenceError

def _check_step(d: ActivityDiagram, sid: str, step, valid: set) -> None:
    if step.next and step.next not in valid:
        raise UnknownReferenceError(f"Step '{sid}' next '{step.next}' unknown in {d.id}")
    for branch, target in step.branches.items():
        if target not in valid:
            raise UnknownReferenceError(f"Step '{sid}' branch '{branch}' target '{target}' unknown in {d.id}")
    if step.kind == "merge" and step.branches:
        raise StructureError(f"Step '{sid}' is a merge: it joins flows into one `next` and takes no branches in {d.id}")
    if step.partition is not None and not step.partition.strip():
        raise StructureError(f"Step '{sid}' has an empty partition in {d.id}")


def validate_activity(d: ActivityDiagram) -> None:
    valid = set(d.data.steps) | {d.data.end}
    if d.data.start not in d.data.steps:
        raise UnknownReferenceError(f"Start step '{d.data.start}' not found in {d.id}")
    for sid, step in d.data.steps.items():
        _check_step(d, sid, step, valid)
