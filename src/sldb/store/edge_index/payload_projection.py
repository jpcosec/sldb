"""A document node's projection (GO04): its payload's scalar fields, its index entry's hashes and
the model's contract signature, stored on the node so a query reads them without re-extracting.

What is left out: a field holding a dict, or a list with any non-scalar item (a table, a nested
model), and every field outside the model's `__indexed__` when it declares one. A field the
extracted payload does not carry (null, so dropped by the extraction) is absent too.
"""

from __future__ import annotations

import logging
from typing import Any, Callable

from sldb.store.edge_index.payload_types import is_projectable
from sldb.store.exceptions import SLDBError
from sldb.store.models import DocumentEntry, EdgeNodeRecord

logger = logging.getLogger(__name__)


def project_payload(payload: dict[str, Any] | None, indexed: list[str] | None) -> dict[str, Any]:
    """The flat map field -> scalar / list of scalars; `indexed` (when given) picks the names."""
    if not payload:
        return {}
    names = sorted(payload) if indexed is None else indexed
    return {n: payload[n] for n in names if n in payload and is_projectable(payload[n])}


def with_projection(nodes: list[EdgeNodeRecord], node_id: str, doc: DocumentEntry, model_type: Any | None, payload_of: Callable[[], dict[str, Any] | None]) -> list[EdgeNodeRecord]:
    """`nodes` with the document's own node (`node_id`) carrying its projection; others untouched."""
    from sldb.store.model_contract import contract_signature, indexed_fields

    if not any(n.id == node_id for n in nodes):
        return nodes
    payload = {} if model_type is None else project_payload(read_payload(payload_of, doc), indexed_fields(model_type))
    update = {"payload": payload, "field_hashes": dict(doc.field_hashes), "source_hash": doc.source_hash, "contract_signature": contract_signature(model_type)}
    return [n.model_copy(update=update) if n.id == node_id else n for n in nodes]


def read_payload(payload_of: Callable[[], dict[str, Any] | None], doc: DocumentEntry) -> dict[str, Any] | None:
    """The payload, or None when the file no longer extracts (an edit from outside sldb broke it,
    or its model rejects it): the node is still contributed, without a projection or declared
    edges, and the next rebuild tries again. `stores check` names it (`store/doc-invalid`)."""
    try:
        return payload_of()
    except (SLDBError, ValueError, OSError) as exc:
        logger.debug("edges: payload of %s not projected: %s", doc.name, exc)
        return None
