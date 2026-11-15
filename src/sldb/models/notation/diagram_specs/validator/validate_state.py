"""`validate_state`."""

from __future__ import annotations

from sldb.models.notation.diagram_specs.state import StateDiagram
from sldb.notations.exceptions import ValidationError

def validate_state(d: StateDiagram) -> None:
    ids = {s.id for s in d.data.states}
    if d.data.initial not in ids:
        raise ValidationError(f"Initial state '{d.data.initial}' not in states in {d.id}")
    for t in d.data.transitions:
        if t.from_ not in ids:
            raise ValidationError(f"Transition 'from' references unknown state '{t.from_}' in {d.id}")
        if t.to not in ids:
            raise ValidationError(f"Transition 'to' references unknown state '{t.to}' in {d.id}")
