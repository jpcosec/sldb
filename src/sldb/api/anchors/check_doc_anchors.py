"""Every document anchor of a store against its target now (GO07, anchoring.md §6): one alert
per anchor that is not `intact`. A `__doc_anchors__` field is read from the payload the index
composes (`<field>__anchor_state`); a `doc:` item of the provenance `from:` from the document's
index entry, against the same targets. Read-only: a `lost` anchor is pinned by the next write
of the document that holds it, never here; there is no `reconnected` for documents.
"""

from __future__ import annotations

from functools import cache, partial
from pathlib import Path

from sldb.api.edges.edge_reading import model_type_of
from sldb.api.stores.open_store import open_store
from sldb.core.exceptions import SLDBModelError
from sldb.core.finding import Finding, alert
from sldb.models.anchor_state import AnchorState
from sldb.store import documents_hash
from sldb.store.edge_index.compose import compose_edge_index
from sldb.store.edge_index.doc_anchor_states import SUFFIX, Current, anchor_state, nodes_current, store_classes
from sldb.store.edge_index.node_ids import bare, kind
from sldb.store.io import load_store_index
from sldb.store.model_contract import doc_anchor
from sldb.store.models import EdgeNodeRecord

_ALERTS = (AnchorState.CHANGED.value, AnchorState.LOST.value)


def check_doc_anchors(store: str | Path | None, pythonpath: str | None = None) -> list[Finding]:
    """The `anchors/doc_{changed,lost}` and `anchors/provenance_{changed,lost}` alerts of the
    store's own documents, by document id; [] when every anchor is intact."""
    store_path, resolver = open_store(store, mode="readonly").store_path.resolve(), _resolver(pythonpath)
    nodes = compose_edge_index(store_path, include_linked=False, model_type_of=resolver).nodes
    current = nodes_current(nodes, store_classes([store_path], resolver))
    docs = sorted((n for n in nodes.values() if kind(n.id) == "document"), key=lambda n: n.id)
    froms = {f"{m.name}:{e.name}": (e.provenance or {}).get("from") or [] for m in load_store_index(store_path).models for e in documents_hash.entries_of(store_path, m.name)}
    return [f for n in docs for f in _field_findings(n) + _from_findings(n, froms.get(bare(n.id), []), current)]


@cache
def _resolver(pythonpath: str | None):
    """The class loader: `pythonpath` first when given, then as the index reads (one per path,
    so the composed index stays cached)."""
    return model_type_of if pythonpath is None else partial(_with_pythonpath, pythonpath)


def _with_pythonpath(pythonpath: str, model_ref: str, root: Path):
    from sldb.api.documents.payload_save_steps import model_class

    try:
        return model_class(model_ref, pythonpath, root)
    except SLDBModelError:
        return model_type_of(model_ref, root)


def _field_findings(node: EdgeNodeRecord) -> list[Finding]:
    keys = [k for k in node.payload if k.endswith(SUFFIX)]
    pairs = [(k[: -len(SUFFIX)], v, s) for k in keys for v, s in _aligned(node.payload.get(k[: -len(SUFFIX)]), node.payload[k])]
    return [_finding(node, "doc", field, value, state) for field, value, state in pairs if state in _ALERTS]


def _from_findings(node: EdgeNodeRecord, items: list, current: Current) -> list[Finding]:
    states = [(item, anchor_state(item, current)) for item in items if isinstance(item, str)]
    return [_finding(node, "provenance", "from", item, state) for item, state in states if state in _ALERTS]


def _aligned(values, states) -> list[tuple]:
    if isinstance(values, list) and isinstance(states, list):
        return list(zip(values, states))
    return [(values, states)]


def _finding(node: EdgeNodeRecord, family: str, field: str, value: str, state: str) -> Finding:
    target = (doc_anchor(value) or (value, None))[0]
    return alert(f"anchors/{family}_{state}", bare(node.id), f"{field} -> {target}: {state} ({value})", "", node.semantics.get("path"))
