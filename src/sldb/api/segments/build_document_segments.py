"""Build the ``DocumentSegments`` view of one tracked document.

The document is rendered through its own model with a span recorder attached, so
the resulting ``text`` is byte-for-byte the canonical render
(``render_model_markdown``) and every offset is exact by construction rather than
re-parsed. ``canonical`` then compares that text against the file on disk, which
can legitimately differ when a composed field's source changed after the parent
was last saved.
"""

from __future__ import annotations

from pathlib import Path
from typing import Any

from sldb.api.documents.document_payload import runtime_document
from sldb.api.segments.document_segments import DocumentSegments
from sldb.api.segments.segment_nodes import build_node
from sldb.core.segments.instrumented_render import render_with_spans
from sldb.core.segments.segment_tree import build_segment_tree


def build_document_segments(store_path: Path, pythonpath: str | None, doc: str) -> DocumentSegments:
    """The segmented canonical render of a tracked document.

    Args:
        store_path: Path of the ``.sldb`` store holding the document.
        pythonpath: Import root for resolving the document's model, or None.
        doc: Document reference: a name, a tracked path or ``Model/name``.

    Returns:
        The document's literals and field spans over its canonical text.

    Raises:
        ValueError: When the reference names no document or more than one.
    """
    record = runtime_document(store_path, pythonpath, doc)
    text, spans = render_with_spans(record.model_type, record.payload)
    nodes = [build_node(meta, start, end, text, record.model_type, record.payload) for meta, start, end in spans]
    return DocumentSegments(
        id=doc, doc=record.name, model=record.model_name, path=record.path, text=text,
        canonical=_is_canonical(store_path, record.path, text), payload=dict(record.payload),
        segments=build_segment_tree(nodes, text),
    )


def _is_canonical(store_path: Path, path: str | None, text: str) -> bool | None:
    """Whether the document file on disk already holds the canonical text.

    Args:
        store_path: Path of the store, whose parent is the project root.
        path: The document's path relative to that root, or None.
        text: The canonical render to compare against.

    Returns:
        True or False after a successful read, None when the file is unreadable.
    """
    if not path:
        return None
    return _read_stripped(store_path.parent / path, text)


def _read_stripped(file_path: Path, text: str) -> bool | None:
    """Compare a file's stripped contents with ``text``.

    Args:
        file_path: Absolute path of the document file.
        text: The canonical render to compare against.

    Returns:
        The comparison result, or None when the file cannot be read.
    """
    try:
        return file_path.read_text(encoding="utf-8").strip() == text
    except OSError:
        return None
