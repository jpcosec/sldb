import hashlib
import json
from typing import Type

from sldb.models.structured_doc import StructuredNLDoc
from sldb.runtime.validation import extract_model_data
from sldb.store.models import DocumentsIndex, ModelsIndex


def hash_text(text: str) -> str:
    return hashlib.sha256(text.encode("utf-8")).hexdigest()


def hash_fields(model_type: Type[StructuredNLDoc], markdown_text: str) -> str:
    payload = extract_model_data(model_type, markdown_text)
    normalized = json.dumps(payload, sort_keys=True, ensure_ascii=False)
    return hashlib.sha256(normalized.encode("utf-8")).hexdigest()


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
