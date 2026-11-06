"""What a model's `__doc_anchors__` fields contribute (GO07): one `references` edge per anchor,
named by the field and pointing at `doc:Model:name` without its `@sha256` suffix, so `^field`
exists in the graph. `declared` keeps the value as written (hash included): the language reads
an element's `anchor_state` by finding that value in the field (`predicate_reach`). An empty
value, or one that is not an anchor, contributes nothing; `from:` of the provenance never does.
"""

from __future__ import annotations

from typing import Any

from sldb.store.edge_index.node_ids import doc_node_id
from sldb.store.edge_index.records import edge
from sldb.store.models import EdgeRecord

REFERENCES = "references"


def doc_anchor_edges(source: str, model_type: Any | None, payload: dict[str, Any] | None) -> list[EdgeRecord]:
    """The anchor edges of one document (`source` is its node id), in declaration then value order."""
    from sldb.store.model_contract import doc_anchor_fields

    if payload is None:
        return []
    return [e for field in doc_anchor_fields(model_type) for e in _field_edges(source, field, payload.get(field))]


def _field_edges(source: str, field: str, value: Any) -> list[EdgeRecord]:
    from sldb.store.model_contract import doc_anchor

    raw = value if isinstance(value, list) else [value]
    pairs = [(item, parsed) for item in raw if (parsed := doc_anchor(item)) is not None]
    return [edge(source, doc_node_id(parsed[0]), REFERENCES, "schema", field=field, declared=item) for item, parsed in pairs]
