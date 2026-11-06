"""Resolves field references against an SLDB store."""

from __future__ import annotations

from pathlib import Path
from typing import Any

from sldb.api.documents.payload_path_reading import deep_get
from sldb.api.model_registry.model_reference import resolve_model_ref
from sldb.core.exceptions import SLDBDocumentTargetError
from sldb.store.query import load_runtime_documents


class FieldRefResolver:
    """Resolves field references against an SLDB store."""

    def __init__(self, store_path: Path | str, pythonpath: str | None = None) -> None:
        self.store_path = Path(store_path)
        self.pythonpath = pythonpath
        self._docs_cache: list[Any] | None = None

    def _get_docs(self) -> list[Any]:
        if self._docs_cache is None:
            self._docs_cache = load_runtime_documents(self.store_path, resolve_model_ref, self.pythonpath)
        return self._docs_cache

    def resolve(self, ref_str: str) -> dict[str, Any]:
        """Resolves Model:name#field, docs/Model/name/field or docs/name/field."""
        doc_ref, field_path = _parse_ref(ref_str.strip().strip("`"))
        doc = _find_doc(self._get_docs(), doc_ref)
        normalized_field = field_path.replace("/", ".")
        return _pack_resolution(doc, normalized_field)


def _pack_resolution(doc: Any, field: str) -> dict[str, Any]:
    return {
        "model": doc.model_name, "doc": doc.name, "path": doc.path or "",
        "field": field, "value": deep_get(doc.payload, field), "payload": doc.payload,
    }


def _parse_ref(ref: str) -> tuple[str, str]:
    if "#" in ref:
        doc_part, _, field_part = ref.partition("#")
        return doc_part.strip(), field_part.strip()
    if ref.startswith("docs/"):
        return _parse_docs_ref(ref[5:])
    raise SLDBDocumentTargetError(f"Invalid field reference format: {ref!r}")


def _parse_docs_ref(rest: str) -> tuple[str, str]:
    parts = rest.split("/")
    if len(parts) >= 3:
        return f"{parts[0]}/{parts[1]}", "/".join(parts[2:])
    if len(parts) == 2:
        return parts[0], parts[1]
    raise SLDBDocumentTargetError(f"Expected docs/<Model>/<doc>/<field> or docs/<doc>/<field>, got: {rest!r}")


def _find_doc(docs: list[Any], doc_ref: str) -> Any:
    matches = [d for d in docs if _matches(d, doc_ref)]
    if not matches:
        raise SLDBDocumentTargetError(f"Unknown document target in field reference: {doc_ref!r}")
    if len(matches) > 1:
        raise SLDBDocumentTargetError(f"Ambiguous document target in field reference: {doc_ref!r}")
    return matches[0]


def _matches(doc: Any, doc_ref: str) -> bool:
    if ":" in doc_ref:
        m, _, n = doc_ref.partition(":")
        return doc.model_name == m and doc.name == n
    if "/" in doc_ref:
        m, _, n = doc_ref.partition("/")
        return doc.model_name == m and doc.name == n
    return doc.name == doc_ref
