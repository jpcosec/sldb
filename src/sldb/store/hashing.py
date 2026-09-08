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
    state = json.dumps(
        [
            {"path": d.path, "hash_c": d.hash_c, "hash_d": d.hash_d}
            for d in documents_index.documents
        ],
        sort_keys=True,
    )
    return hashlib.sha256(state.encode("utf-8")).hexdigest()


def hash_models_layer(models_indices: list[ModelsIndex]) -> str:
    state = json.dumps(
        [{"name": m.name, "hash_b": m.hash_b} for m in models_indices],
        sort_keys=True,
    )
    return hashlib.sha256(state.encode("utf-8")).hexdigest()
