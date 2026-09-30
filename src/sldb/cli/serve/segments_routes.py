"""GET /document/segments: one document as literals plus editable field spans.

Built by ``sldb.api.build_document_segments``; nothing here renders or parses.
``document_routes`` owns the ``id`` parameter and the 404 for an untracked doc,
so this module only has to turn a render failure into a 422: a document that
exists but whose payload no longer instantiates its model must not take the
endpoint down.
"""

from __future__ import annotations

from pathlib import Path
from typing import Any

from sldb.api.segments import build_document_segments

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
