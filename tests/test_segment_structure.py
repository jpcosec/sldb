"""Structural guarantees of a segmented document, on models built for the purpose.

The store-wide invariant in ``test_document_segments`` proves the text is right;
these tests pin the shape around it: field paths in the ``sldb fields`` space,
``editable`` taken from the marker, list items addressed by index, the zero-length
span an absent optional leaves behind, and the single-piece composition tiebreak
that once put a piece outside its own field.
"""

from __future__ import annotations

from typing import Any

from pydantic import Field

from sldb import StructuredNLDoc
from sldb.api.segments.segment_nodes import build_node
from sldb.core.segments.instrumented_render import render_with_spans
from sldb.core.segments.segment_tree import build_segment_tree
from sldb.runtime.validation import render_model_markdown


class SegmentedDoc(StructuredNLDoc):
    """A document with a required field, an optional one and a scalar list."""

    __template__ = "# ⸢rev•title⸥\n\nNote: ⸢optrev•note⸥ (end)\n\n- ⸢rev,list•tags⸥"

    title: str = Field(description="The document's title.")
    note: str | None = Field(default=None, description="An optional inline note.")
    tags: list[str] = Field(default_factory=list, description="Free-form tags.")


def _segments(payload: dict[str, Any]) -> tuple[str, list[Any]]:
    """The canonical text and full segment tree of a ``SegmentedDoc`` payload."""
    text, spans = render_with_spans(SegmentedDoc, payload)
    nodes = [build_node(meta, start, end, text, SegmentedDoc, payload) for meta, start, end in spans]
    return text, build_segment_tree(nodes, text)


def _fields(segments: list[Any]) -> dict[str, dict[str, Any]]:
    """Every field segment of a tree, flattened and keyed by its path."""
    out: dict[str, dict[str, Any]] = {}
    for segment in segments:
        if segment["type"] != "literal":
            out[segment["path"]] = segment
        out.update(_fields(segment.get("children") or []))
    return out


def test_field_paths_addresses_and_values_follow_the_fields_space() -> None:
    """Paths, kinds and typed values match what ``sldb fields`` would address."""
    text, segments = _segments({"title": "T", "note": "N", "tags": ["a", "b"]})
    fields = _fields(segments)
    assert sorted(fields) == ["note", "tags/0", "tags/1", "title"]
    assert fields["title"]["value"] == "T" and fields["title"]["kind"] == "string"
    assert fields["tags/1"]["value"] == "b" and fields["tags/1"]["kind"] == "string"
    assert text[fields["tags/1"]["start"]:fields["tags/1"]["end"]] == "b"


def test_editable_comes_from_the_marker_not_from_the_value() -> None:
    """``rev`` and ``optrev`` are editable; the flag ignores whether a value is set."""
    _, segments = _segments({"title": "T", "note": "N", "tags": []})
    fields = _fields(segments)
    assert fields["title"]["editable"] is True
    assert fields["note"]["editable"] is True
    assert fields["note"]["marker"] == "optrev"


def test_absent_optional_sharing_a_line_leaves_a_zero_length_insertion_point() -> None:
    """An unset ``optrev`` reports an empty span the UI can use as an insertion point.

    The marker has to share its line with other text. An ``optrev`` alone on its
    line is dropped line and all by ``_is_absent_optional_line``, so it leaves no
    trace in the render and therefore no span either.
    """
    text, segments = _segments({"title": "T", "note": None, "tags": ["a"]})
    note = _fields(segments)["note"]
    assert note["start"] == note["end"]
    assert note["text"] == "" and note["value"] is None
    assert text[note["start"]:note["start"] + 5] == " (end"


def test_literals_and_fields_tile_the_text_in_reading_order() -> None:
    """Concatenating the top-level segments rebuilds the text exactly."""
    text, segments = _segments({"title": "T", "note": "N", "tags": ["a", "b"]})
    assert "".join(segment["text"] for segment in segments) == text
    assert [segment["start"] for segment in segments] == sorted(segment["start"] for segment in segments)


def test_a_single_piece_composition_nests_inside_its_own_field() -> None:
    """At an identical range the span wrapped later is the outer one.

    A composition of exactly one piece covers the same characters as the ``render``
    field holding it. Without the wrap-order tiebreak the piece became the parent
    and the field its child, which is the inverse of the real containment.
    """
    piece = {"start": 0, "end": 4, "_order": 0, "children": [], "type": "composition", "text": "abcd"}
    field = {"start": 0, "end": 4, "_order": 1, "children": [], "type": "field", "text": "abcd"}
    roots = build_segment_tree([piece, field], "abcd")
    assert [root["type"] for root in roots] == ["field"]
    assert [child["type"] for child in roots[0]["children"]] == ["composition"]


class TrailingNewlineDoc(StructuredNLDoc):
    """A document whose composed-style field ends a block with blank lines."""

    __template__ = "# ⸢rev•title⸥\n\n## Body\n\n⸢render•body⸥\n\n## After"

    title: str = Field(description="The document's title.")
    body: str = Field(description="A block value that may end in newlines.")


def test_sentinels_do_not_shield_the_newline_jinja_drops() -> None:
    """A value ending in newlines renders identically with and without recording.

    Jinja renders with ``keep_trailing_newline=False`` and drops exactly one
    trailing newline. The recorder's CLOSE sentinel lands after that newline, so
    without ``unshield_trailing_newline`` the newline stops being trailing and
    survives: the instrumented render gained one character the plain one lacks.
    Found on a real composed document (``complete-systemprompt``), whose composed
    blocks end in a blank line.
    """
    for body in ("text\n\n", "text\n", "text", "a\nb\n\n\n"):
        payload = {"title": "T", "body": body}
        text, _ = render_with_spans(TrailingNewlineDoc, payload)
        assert text == render_model_markdown(TrailingNewlineDoc, payload), body
