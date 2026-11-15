"""`check_inheritance_cycles`."""

from __future__ import annotations

from sldb.notations.exceptions import ValidationError

def _visit(ident: str, parents: dict, active: set, done: set, d_id: str) -> None:
    if ident in active:
        raise ValidationError(f"Inheritance/realization cycle at '{ident}' in {d_id}")
    if ident in done:
        return
    active.add(ident)
    for parent in parents[ident]:
        _visit(parent, parents, active, done, d_id)
    active.remove(ident)
    done.add(ident)


def check_inheritance_cycles(parents: dict[str, list[str]], d_id: str) -> None:
    active, done = set(), set()
    for ident in parents:
        _visit(ident, parents, active, done, d_id)
