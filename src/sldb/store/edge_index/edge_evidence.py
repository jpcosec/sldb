"""Evidence on an edge: the states it stands on, named by hash.

`metadata.evidence` carries `ref_hash` (the target as it was: a document's `content_hash`, a
model's `model_hash`; for a section, its document's, flagged `ref: document`, because a section
has no hash of its own), `contract` (the source model's `contract_hash`), and who made the edge:
`actor` (`relation_doc:<name>`) for an authored edge, else `engine` (`{name, version}`). No
timestamp: evidence names states, not moments. Stamped on read, never written into a shard: a
source shard would otherwise go stale every time its target changed. Because it is read now,
`ref_hash` is the target's current hash: telling an edge went stale takes a consumer that kept
an earlier evidence and compares (deskops, inbox 20261019-140852).
"""

from __future__ import annotations

from sldb.store.models import EdgeRecord

_DOCUMENT, _SECTION, _MODEL = "sldb://document/", "sldb://section/", "sldb://model/"


def stamp(edges: list[EdgeRecord], hashes: dict[str, str], contracts: dict[str, str], engine: dict) -> list[EdgeRecord]:
    """Copies of `edges` with `metadata.evidence`; `hashes` and `contracts` are keyed by node id
    (documents, models) and by model name."""
    return [e.model_copy(update={"metadata": {**e.metadata, "evidence": _evidence(e, hashes, contracts, engine)}}) for e in edges]


def _evidence(edge: EdgeRecord, hashes: dict[str, str], contracts: dict[str, str], engine: dict) -> dict:
    target, ref = _owner(edge.target)
    evidence = {"ref_hash": hashes.get(target), "contract": contracts.get(_model_of(edge.source))}
    if ref:
        evidence["ref"] = ref
    authored = edge.metadata.get("origin") == "relation_doc"
    return {**evidence, **({"actor": f"relation_doc:{edge.metadata.get('relation_doc')}"} if authored else {"engine": engine})}


def _owner(node_id: str) -> tuple[str, str | None]:
    """The node whose hash stands for `node_id`: a section's document, else the node itself."""
    if node_id.startswith(_SECTION):
        return _DOCUMENT + node_id[len(_SECTION):].split("#", 1)[0], "document"
    return node_id, None


def _model_of(node_id: str) -> str | None:
    """The model a document, section or model node belongs to (`store:Model:name` qualified ids too)."""
    for prefix in (_DOCUMENT, _SECTION):
        if node_id.startswith(prefix):
            export_id = node_id[len(prefix):].split("#", 1)[0]
            return export_id.split(":")[-2] if export_id.count(":") >= 1 else None
    return node_id[len(_MODEL):] if node_id.startswith(_MODEL) else None
