"""The two segment endpoints: a tracked document, or raw markdown read as a model.

Both are built by ``sldb.api``; nothing here renders, parses or aligns.

``GET /document/segments`` — ``document_routes`` owns the ``id`` parameter and
the 404 for an untracked doc, so only a render failure has to become a 422.

``POST /extract/segments`` — the two ways this can fail are different questions
and get different answers: an unregistered or unimportable model is about the
*request* (404), while markdown that does not satisfy the model is about the
*content* (422). Collapsing them would leave a client unable to tell a typo in a
model name from a document that needs fixing.
"""

from __future__ import annotations

from pathlib import Path
from typing import Any

from sldb.api.segments import build_document_segments, extract_markdown_segments
from sldb.core.exceptions import SLDBModelError, SLDBStoreError, SLDBValidationError

JsonDict = dict[str, Any]


def segments_response(store_path: Path, pythonpath: str, name: str) -> tuple[JsonDict, int]:
    """The segments of a tracked document, or a 422 when it does not render.

    Args:
        store_path: Path of the ``.sldb`` store being served.
        pythonpath: Import root for resolving the document's model.
        name: The tracked document's name.

    Returns:
        The serialized ``DocumentSegments`` and 200, or an error body and 422.
    """
    try:
        return build_document_segments(store_path, pythonpath, name).model_dump(mode="json"), 200
    except Exception as exc:
        return {"ok": False, "error": str(exc)}, 422


def extract_segments_response(body: JsonDict, store_path: Path, pythonpath: str) -> tuple[JsonDict, int]:
    """Answer ``POST /extract/segments`` with ``{model, markdown}``.

    Args:
        body: The decoded JSON request body.
        store_path: Path of the ``.sldb`` store being served.
        pythonpath: Import root for resolving the named model.

    Returns:
        The extraction and 200; 400 for a malformed body, 404 for a model that
        is not registered or cannot be imported, 422 for markdown that does not
        extract as that model.
    """
    model, markdown = body.get("model"), body.get("markdown")
    if not isinstance(model, str) or not model or not isinstance(markdown, str):
        return {"ok": False, "error": "Expected {model: str, markdown: str}."}, 400
    return _extract(store_path, pythonpath, model, markdown)


def _extract(store_path: Path, pythonpath: str, model: str, markdown: str) -> tuple[JsonDict, int]:
    """Run the extraction, mapping each kind of failure to its own status.

    Args:
        store_path: Path of the ``.sldb`` store being served.
        pythonpath: Import root for resolving the named model.
        model: Name of a model registered in the store.
        markdown: The raw markdown to read.

    Returns:
        The serialized ``ExtractionSegments`` and 200, or a typed error body.
    """
    try:
        return extract_markdown_segments(store_path, pythonpath, model, markdown).model_dump(mode="json"), 200
    except (SLDBStoreError, SLDBModelError) as exc:
        return {"ok": False, "error": str(exc), "kind": "model"}, 404
    except SLDBValidationError as exc:
        return {"ok": False, "error": str(exc), "kind": "extraction", "details": exc.details}, 422
