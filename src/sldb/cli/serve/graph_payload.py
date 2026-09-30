"""GET /graph: every tracked document, plus the models whose documents are missing.

A model that cannot be imported takes every document it tracks out of the
listing, because ``sldb.store.query._load_one`` resolves each model and skips it
when resolution fails. That silence is what makes a partially broken store look
like a small one, so the models responsible are declared alongside the documents.
"""

from __future__ import annotations

from pathlib import Path
from typing import Any

from sldb.api import serialize_document
from sldb.cli.model_utils import resolve_model_ref
from sldb.cli.serve.unavailable_models import unavailable_models
from sldb.store.query import load_runtime_documents


def graph_documents(store_path: Path, pythonpath: str) -> list[dict[str, Any]]:
    """Every tracked document of the store, serialized for the graph surface.

    Args:
        store_path: Path of the ``.sldb`` store being served.
        pythonpath: Import root for resolving the document models.

    Returns:
        One serialized record per document that could be loaded.
    """
    docs = load_runtime_documents(store_path, resolve_model_ref, pythonpath)
    return [serialize_document(doc) for doc in docs]


def graph_payload(store_path: Path, pythonpath: str) -> dict[str, Any]:
    """The documents of the store together with any unavailable models.

    Args:
        store_path: Path of the ``.sldb`` store being served.
        pythonpath: Import root for resolving the document models.

    Returns:
        ``{documents, unavailable}``; ``unavailable`` is empty for a healthy store.
    """
    unavailable = unavailable_models(store_path, pythonpath)
    return {
        "documents": graph_documents(store_path, pythonpath),
        "unavailable": [model.model_dump(mode="json") for model in unavailable],
    }
