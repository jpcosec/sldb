"""Locating a model's fields inside raw markdown that is not a tracked document.

Extraction is lossy in surface: the payload read from raw markdown re-renders to
a canonical text whose whitespace, YAML quoting and line folding may differ. The
field spans are exact over that canonical text, so they reach the raw text
through a character diff — ``exact`` when both borders land on identical text,
``approximate`` when they had to be clamped to a changed run's edge.
"""

from __future__ import annotations

from pydantic import Field

from sldb import StructuredNLDoc
from sldb.api.segments import build_extraction_segments
from sldb.core.segments.canonical_alignment import align, map_offset
from sldb.core.segments.unmatched_runs import unmatched_runs
from sldb.runtime.validation import render_model_markdown


class ExtractableDoc(StructuredNLDoc):
    """A document simple enough to round-trip through extraction cleanly."""

    __template__ = "# ⸢rev•title⸥\n\n## Body\n\n⸢rev•body⸥"

    title: str = Field(description="The document's title.")
    body: str = Field(description="The document's body text.")


def test_canonical_markdown_locates_every_field_exactly() -> None:
    """Markdown that already is the canonical render aligns with no drift."""
    markdown = render_model_markdown(ExtractableDoc, {"title": "T", "body": "B"})
    result = build_extraction_segments(ExtractableDoc, markdown)
    assert result.model == "ExtractableDoc"
    assert result.text == markdown and result.canonical_text == markdown
    assert result.payload == {"title": "T", "body": "B"}
    assert {field.alignment for field in result.fields} == {"exact"}
    assert [field.path for field in result.fields] == ["title", "body"]
    assert result.unmatched == []


def test_field_offsets_address_the_raw_text_not_the_canonical_one() -> None:
    """Every reported span slices the submitted markdown, byte for byte."""
    markdown = "#    T\n\n## Body\n\nB"
    result = build_extraction_segments(ExtractableDoc, markdown)
    for field in result.fields:
        assert result.text[field.start:field.end] == field.text, field.path


def test_fields_come_back_in_reading_order() -> None:
    """The list is sorted by start offset, whatever order the render wrapped them."""
    markdown = render_model_markdown(ExtractableDoc, {"title": "T", "body": "B"})
    starts = [field.start for field in build_extraction_segments(ExtractableDoc, markdown).fields]
    assert starts == sorted(starts)


def test_coverage_is_a_fraction_of_the_meaningful_text() -> None:
    """Coverage stays within [0, 1] and grows with how much the fields explain."""
    small = build_extraction_segments(ExtractableDoc, "# T\n\n## Body\n\nB")
    large = build_extraction_segments(ExtractableDoc, "# TTTTTTTTTT\n\n## Body\n\nBBBBBBBBBB")
    assert 0.0 <= small.coverage <= 1.0 and 0.0 <= large.coverage <= 1.0
    assert large.coverage > small.coverage


def test_changed_text_yields_approximate_borders() -> None:
    """A span over a run the diff calls 'replace' is reported as approximate.

    Mapping cannot be exact when the characters themselves changed, so the
    border is clamped to the run's edge and the span says so instead of
    pretending precision it does not have.
    """
    opcodes = align("a HOLA b", "a hola b")
    start, exact_start = map_offset(opcodes, 2)
    end, exact_end = map_offset(opcodes, 6, is_end=True)
    assert (start, end) == (2, 6)
    assert not exact_start and not exact_end


def test_unmatched_runs_are_trimmed_and_blank_ones_dropped() -> None:
    """Only raw content with non-blank text is reported as unexplained."""
    opcodes = align("ab", "a   \n  b")
    runs = unmatched_runs(opcodes, "a   \n  b")
    assert runs == []
    opcodes = align("ab", "a EXTRA b")
    runs = unmatched_runs(opcodes, "a EXTRA b")
    assert [run["text"] for run in runs] == ["EXTRA"]
    assert all(run["text"] == run["text"].strip() for run in runs)
