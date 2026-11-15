"""`validate_sequence`."""

from __future__ import annotations

from sldb.models.notation.diagram_specs.sequence import SequenceDiagram
from sldb.notations.exceptions import ValidationError

def validate_sequence(d: SequenceDiagram) -> None:
    ids = {p.id for p in d.data.participants}
    for msg in d.data.messages:
        if msg.from_ not in ids:
            raise ValidationError(f"Message 'from' references unknown participant '{msg.from_}' in {d.id}")
        if msg.to not in ids:
            raise ValidationError(f"Message 'to' references unknown participant '{msg.to}' in {d.id}")
