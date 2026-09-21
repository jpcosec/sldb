"""Render and extract one document through its model, the wiki's path.

``sldb render`` runs ``render_model_markdown`` over a payload and ``sldb extract``
runs ``extract_model_data`` over markdown; this module reuses those exact runtime
functions against a tracked document's payload and model type, so the HTTP
surface renders with the same template engine the CLI (and AntonIA's wiki) uses.
"""

from __future__ import annotations

from pathlib import Path
from typing import Any

from sldb.api.documents.document_payload import runtime_document
from sldb.api.model_registry.load_registered_model import load_registered_model


def render_document_markdown(store_path: Path, pythonpath: str | None, doc_ref: str) -> str:
    """The document rendered from its template, via the CLI's renderer."""
    from sldb.runtime.validation import render_model_markdown

    doc = runtime_document(store_path, pythonpath, doc_ref)
    return render_model_markdown(doc.model_type, doc.payload)


def render_model_template(store_path: Path, pythonpath: str | None, model_name: str) -> str:
    """The model's rendering recipe: its ``__template__``, as sample text."""
    return load_registered_model(store_path, model_name, pythonpath).model_type.__template__


def extract_document_payload(store_path: Path, pythonpath: str | None, doc_ref: str) -> dict[str, Any]:
    """The extracted payload only, no markdown — the runtime payload as extracted."""
    doc = runtime_document(store_path, pythonpath, doc_ref)
    return dict(doc.payload)