"""Segments of a document must reconstruct its canonical render exactly.

The whole design rests on one invariant: the instrumented render produces the
same bytes as ``render_model_markdown``, because the sentinels are removed before
the renderer's final strip. The store-wide test below asserts that over every
tracked document of this repo, which is the only sample large enough to cover the
template shapes in use (front matter, lists, tables, compositions, nesting).
"""

from __future__ import annotations

from pathlib import Path
from typing import Any

import pytest

from sldb.api.documents.runtime_documents import load_runtime_documents
from sldb.api.segments import build_document_segments
from sldb.core.segments.instrumented_render import render_with_spans
from sldb.runtime.validation import render_model_markdown

ROOT = Path(__file__).resolve().parents[1]
STORE = ROOT / ".sldb"


def _store_documents() -> list[Any]:
    """Every runtime document of the repo's own store, or none when absent."""
    if not STORE.is_dir():
        return []
    return load_runtime_documents(STORE, str(ROOT))


DOCUMENTS = _store_documents()


@pytest.mark.skipif(not DOCUMENTS, reason="the repo's own .sldb store is required")
def test_instrumented_render_matches_canonical_render_for_every_document() -> None:
    """The decoded text equals ``render_model_markdown`` byte for byte, store-wide."""
    mismatches = [doc.name for doc in DOCUMENTS if not _renders_identically(doc)]
    assert mismatches == []


def _renders_identically(doc: Any) -> bool:
    """Whether the instrumented render of one document matches the plain one."""
    text, _ = render_with_spans(doc.model_type, doc.payload)
    return text == render_model_markdown(doc.model_type, doc.payload)


@pytest.mark.skipif(not DOCUMENTS, reason="the repo's own .sldb store is required")
def test_segments_concatenate_back_into_the_document_text() -> None:
    """Top-level segments tile the text with no gap and no overlap, store-wide."""
    broken = [doc.name for doc in DOCUMENTS if not _segments_tile(doc.name)]
    assert broken == []


def _segments_tile(name: str) -> bool:
    """Whether a document's top-level segments concatenate back into its text."""
    result = build_document_segments(STORE, str(ROOT), name)
    return "".join(segment.text for segment in result.segments) == result.text


@pytest.mark.skipif(not DOCUMENTS, reason="the repo's own .sldb store is required")
def test_every_segment_text_matches_its_own_offsets() -> None:
    """Each segment's ``text`` is exactly the slice its offsets address, nested included."""
    offenders = [doc.name for doc in DOCUMENTS if _offset_mismatch(doc.name)]
    assert offenders == []


def _offset_mismatch(name: str) -> str | None:
    """The first segment path whose text disagrees with its offsets, if any."""
    result = build_document_segments(STORE, str(ROOT), name)
    for segment in _flatten(result.segments):
        if result.text[segment.start:segment.end] != segment.text:
            return getattr(segment, "path", "") or segment.type
    return None


def _flatten(segments: list[Any]) -> list[Any]:
    """Every segment of a tree, parents before children."""
    out: list[Any] = []
    for segment in segments:
        out.append(segment)
        out.extend(_flatten(getattr(segment, "children", None) or []))
    return out
