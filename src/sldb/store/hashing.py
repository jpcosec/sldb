import hashlib
import json
from typing import Any

from sldb.store.codec import StoreCodec, default_codec
from sldb.store.models import DocumentsIndex, ModelsIndex


def hash_text(text: str) -> str:
    return hashlib.sha256(text.encode("utf-8")).hexdigest()


def hash_payload(payload: Any) -> str:
    """hash_d of an already extracted payload."""
    normalized = json.dumps(payload, sort_keys=True, ensure_ascii=False)
    return hashlib.sha256(normalized.encode("utf-8")).hexdigest()


def hash_fields(model_type: Any, markdown_text: str, codec: StoreCodec = default_codec) -> str:
    return hash_payload(codec.extract(model_type, markdown_text))


def hash_documents_index(documents_index: DocumentsIndex) -> str:
    """PLAN 15 capa 7: keyed by `name` and sorted — order-independent (documents_index.
    documents used to be insertion-ordered, so hash_b used to depend on write order too; a
    store's Merkle root should depend only on content). The same value however documents
    were gathered: a full scan (stores update) or the incremental per-document child-hash
    map (sldb.store.documents_hash — a write's own hot path)."""
    return hash_document_entries((d.name, d.hash_c, d.hash_d) for d in documents_index.documents)


def hash_document_entries(entries) -> str:
    """`entries`: iterable of (name, hash_c, hash_d) triples, any order."""
    state = json.dumps(
        sorted([{"name": n, "hash_c": hc, "hash_d": hd} for n, hc, hd in entries], key=lambda d: d["name"]),
        sort_keys=True,
    )
    return hashlib.sha256(state.encode("utf-8")).hexdigest()


def hash_model_contract(model_type: Any) -> str:
    """The model's contract: the field schema a payload must satisfy, plus the template that
    renders it. Two documents with identical field values render differently under different
    templates, and a field added to the class changes what extraction yields from unchanged
    text — both belong in the model's node, so both move it."""
    fields = {name: [str(info.annotation), info.description or ""] for name, info in model_type.model_fields.items()}
    return hash_payload({"fields": fields, "template": getattr(model_type, "__template__", "")})


def hash_model_layer(roster_hash: str, contract_hash: str) -> str:
    """A model node from its two children: the document roster and the model's contract.

    Both are persisted next to it (`ModelsIndex.roster_hash`/`contract_hash`) so a node that
    disagrees can be attributed to one child instead of reported as a bare mismatch.
    """
    return hash_payload({"contract_hash": contract_hash, "roster_hash": roster_hash})


def hash_models_layer(models_indices: list[ModelsIndex]) -> str:
    state = json.dumps(
        [{"name": m.name, "hash_b": m.hash_b} for m in models_indices],
        sort_keys=True,
    )
    return hashlib.sha256(state.encode("utf-8")).hexdigest()
