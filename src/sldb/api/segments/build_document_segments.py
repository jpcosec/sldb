"""Build the ``DocumentSegments`` view of one tracked document."""

from __future__ import annotations

from pathlib import Path

from sldb.api.documents.document_payload import runtime_document
from sldb.api.segments.document_segments import DocumentSegments
from sldb.api.segments.field_ref_resolver import FieldRefResolver
from sldb.api.segments.segment_nodes import build_node
from sldb.core.segments.instrumented_render import render_with_spans
from sldb.core.segments.segment_tree import build_segment_tree
from sldb.store.source_guard import target_text


def build_document_segments(store_path: Path, pythonpath: str | None, doc: str) -> DocumentSegments:
    """The segmented canonical render of a tracked document."""
    record = runtime_document(store_path, pythonpath, doc)
    resolver = FieldRefResolver(store_path, pythonpath)
    text, spans = render_with_spans(record.model_type, record.payload, store_path.parent, field_resolver=resolver)
    nodes = [build_node(m, s, e, text, record.model_type, record.payload, store_path, pythonpath) for m, s, e in spans]
    return DocumentSegments(
        id=doc, doc=record.name, model=record.model_name, path=record.path, text=text,
        canonical=_is_canonical(store_path, record.path, text), payload=dict(record.payload),
        segments=build_segment_tree(nodes, text),
    )


def _is_canonical(store_path: Path, path: str | None, text: str) -> bool | None:
    if not path:
        return None
    return _read_stripped(store_path.parent, path, text)


def _read_stripped(root: Path, path: str, text: str) -> bool | None:
    """Whether the file, block aside, is the canonical render; read through the guard (a path
    outside the root, or a symlink, fails as `SLDBDocumentTargetError` naming its finding)."""
    try:
        from sldb.models.provenance_block import strip_block

        return strip_block(target_text(root, root / path, path)).strip() == text
    except OSError:
        return None
