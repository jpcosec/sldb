"""`check_containment_cycles`: ciclos de contención de paquetes o nodos."""

from __future__ import annotations

from sldb.notations.exceptions import StructureError

def check_containment_cycles(parent: dict[str, str], ids, what: str, diagram_id: str) -> None:
    for pid in ids:
        seen, current = [pid], parent.get(pid)
        while current is not None:
            if current in seen:
                cycle = " > ".join([*reversed(seen[seen.index(current):]), current])
                raise StructureError(f"{what} containment has a cycle ({cycle}) in {diagram_id}")
            seen.append(current)
            current = parent.get(current)
