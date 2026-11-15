"""`check_connections`: las conexiones de un despliegue."""

from __future__ import annotations

from sldb.models.notation.diagram_specs.deployment import DeploymentDiagram
from sldb.models.notation.diagram_specs.validator.deployment_ends import DEPLOYMENT_ENDS
from sldb.notations.exceptions import EndpointKindError, UnknownReferenceError

def _check_ends(conn, kind_of: dict, d_id: str) -> None:
    for end, ref in (("from", conn.from_), ("to", conn.to)):
        if ref not in kind_of:
            raise UnknownReferenceError(f"Connection '{end}' references unknown node or artifact '{ref}' in {d_id}")


def check_connections(d: DeploymentDiagram, kind_of: dict) -> None:
    for conn in d.data.connections:
        _check_ends(conn, kind_of, d.id)
        ends = (kind_of[conn.from_], kind_of[conn.to])
        if ends not in DEPLOYMENT_ENDS[conn.kind]:
            allowed = ", ".join(f"{a} -> {b}" for a, b in sorted(DEPLOYMENT_ENDS[conn.kind]))
            raise EndpointKindError(
                f"Connection '{conn.from_}' -> '{conn.to}' ({conn.kind}) goes {ends[0]} -> {ends[1]}; "
                f"a {conn.kind} connection goes {allowed} in {d.id}"
            )
