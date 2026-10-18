import hashlib
import json
from typing import Any

from sldb.store.codec import StoreCodec, default_codec
from sldb.store.models import DocumentsIndex, ModelsIndex
from sldb.store.semantic_tags import flatten_model_semantics


def hash_text(text: str) -> str:
    return hashlib.sha256(text.encode("utf-8")).hexdigest()


def hash_payload(payload: Any) -> str:
    """content_hash of an already extracted payload."""
    normalized = json.dumps(payload, sort_keys=True, ensure_ascii=False)
    return hashlib.sha256(normalized.encode("utf-8")).hexdigest()


def hash_fields(model_type: Any, markdown_text: str, codec: StoreCodec = default_codec) -> str:
    return hash_payload(codec.extract(model_type, markdown_text))


def hash_field_map_of(payload: dict[str, Any]) -> dict[str, str]:
    """One hash per field of an already extracted payload.

    `content_hash` signs the payload as a whole, so a single changed field moves it and
    nothing says which one. This signs each field on its own: a diff against the map an index
    holds names the fields that actually moved, which is what `stores check` reports and what
    a per-field consumer (an embedding index keyed `Model/doc#field`) needs to re-embed one
    field instead of all of them.

    Each value goes through `hash_payload`, so a field's hash is the same function of its value
    that `content_hash` is of the whole payload: order-independent for dicts, exact for scalars.
    This is a sibling of `content_hash`, never a replacement — `content_hash` stays the
    optimistic-concurrency token `/save` compares against `expected`.
    """
    return {name: hash_payload(value) for name, value in payload.items()}


def hash_field_map(model_type: Any, markdown_text: str, codec: StoreCodec = default_codec) -> dict[str, str]:
    """`hash_field_map_of` for text that has not been extracted yet.

    Prefer `hash_field_map_of` where the payload is already in hand (`index_refresh` caches
    it): extraction is the expensive half, and this would pay it twice.
    """
    return hash_field_map_of(codec.extract(model_type, markdown_text))


def hash_fields_with_map(
    model_type: Any, markdown_text: str, codec: StoreCodec = default_codec
) -> tuple[str, dict[str, str]]:
    """A document's `content_hash` and its per-field map, from a single extraction.

    What a write site wants: calling `hash_fields` and `hash_field_map` separately would
    extract the same text twice.
    """
    payload = codec.extract(model_type, markdown_text)
    return hash_payload(payload), hash_field_map_of(payload)


def hash_documents_index(documents_index: DocumentsIndex) -> str:
    """PLAN 15 capa 7: keyed by `name` and sorted — order-independent (documents_index.
    documents used to be insertion-ordered, so roster_hash used to depend on write order too; a
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
    """A model's contract: fields, template, and the class metadata the store derives from."""
    return hash_payload(_contract_parts(model_type))


def _contract_parts(model_type: Any) -> dict[str, Any]:
    declared = getattr(model_type, "__reference_models__", None)  # only when declared: no other contract moves
    return {**_core_contract_parts(model_type), **({"reference_models": declared} if declared else {})}


def _core_contract_parts(model_type: Any) -> dict[str, Any]:
    return {"fields": _field_schema(model_type), "template": getattr(model_type, "__template__", ""),
            "family": getattr(model_type, "__family__", None), "semantics": flatten_model_semantics(model_type),
            "base_models": _base_names(model_type), "references": getattr(model_type, "__references__", None) or [],
            "containment": getattr(model_type, "__containment__", None) or {}, "compositions": getattr(model_type, "__compositions__", None) or {}}


def _field_schema(model_type: Any) -> dict[str, list[str]]:
    return {name: [str(info.annotation), info.description or ""] for name, info in model_type.model_fields.items()}


def _base_names(model_type: Any) -> list[str]:
    from sldb.models.structured_doc import StructuredNLDoc
    return [b.__name__ for b in model_type.__mro__[1:]
            if isinstance(b, type) and issubclass(b, StructuredNLDoc) and b is not StructuredNLDoc]


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
