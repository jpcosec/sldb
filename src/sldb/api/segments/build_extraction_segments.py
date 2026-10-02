"""Locate a model's fields inside raw markdown that is not a tracked document.

Three steps, all reusing machinery that already exists: extract the payload, do
an instrumented render of it to get exact spans over the canonical text, then
carry those spans to the raw text through a character-level alignment. Nothing
re-parses the markdown looking for fields — the render remains the only thing
that knows where a value goes.
"""

from __future__ import annotations

from pathlib import Path
from typing import Any

from sldb.api.segments.extraction_segments import ExtractionSegments
from sldb.api.segments.segment_nodes import build_node
from sldb.core.segments.canonical_alignment import align, map_offset
from sldb.core.segments.instrumented_render import render_with_spans
from sldb.core.segments.unmatched_runs import unmatched_runs


def build_extraction_segments(model_type: type, markdown: str, ref_root: Path | None = None) -> ExtractionSegments:
    """The fields of ``model_type`` located in ``markdown``.

    Args:
        model_type: The ``StructuredNLDoc`` subclass to extract with.
        markdown: The raw markdown to read.
        ref_root: Directory a composed field's refs resolve against, or None.

    Returns:
        The extracted payload, the canonical render, and every field's span over
        the raw text with its alignment quality and the overall coverage.

    Raises:
        Exception: Whatever extraction raises when the markdown does not satisfy
            the model; callers at a boundary are expected to classify it.
    """
    from sldb.runtime.validation import extract_model_data

    payload = extract_model_data(model_type, markdown)
    canonical, spans = render_with_spans(model_type, payload, ref_root)
    opcodes = align(canonical, markdown)
    fields = _located_fields(spans, canonical, markdown, opcodes, model_type, payload)
    return ExtractionSegments(
        model=model_type.__name__, text=markdown, payload=payload, canonical_text=canonical,
        fields=fields, unmatched=unmatched_runs(opcodes, markdown), coverage=_coverage(fields, markdown),
    )


def _located_fields(spans: list[Any], canonical: str, markdown: str, opcodes: list[Any], model_type: type, payload: dict[str, Any]) -> list[dict[str, Any]]:
    """Every field span carried from the canonical text over to the raw text.

    Args:
        spans: The ``(meta, start, end)`` spans of the instrumented render.
        canonical: The canonical text the spans address.
        markdown: The raw markdown to map onto.
        opcodes: The alignment between the two texts.
        model_type: The model being extracted with.
        payload: The extracted payload.

    Returns:
        Field dicts addressed against the raw text, sorted by start offset.
    """
    located = [_relocate(build_node(meta, start, end, canonical, model_type, payload), markdown, opcodes) for meta, start, end in spans]
    return sorted([field for field in located if field is not None], key=lambda field: field["start"])


def _relocate(node: dict[str, Any], markdown: str, opcodes: list[Any]) -> dict[str, Any] | None:
    """Re-address one canonical segment against the raw text.

    Args:
        node: A segment dict built over the canonical text.
        markdown: The raw markdown to map onto.
        opcodes: The alignment between the two texts.

    Returns:
        The field dict over raw offsets, or None for a composed piece, which
        has no address of its own in this payload.
    """
    if node["type"] != "field":
        return None
    start, exact_start = map_offset(opcodes, node["start"])
    end, exact_end = map_offset(opcodes, node["end"], is_end=True)
    keep = {key: node[key] for key in ("path", "marker", "traits", "editable", "display", "kind", "value") if key in node}
    return {**keep, "type": "field", "start": start, "end": max(start, end), "text": markdown[start:max(start, end)],
            "alignment": "exact" if exact_start and exact_end else "approximate"}


def _coverage(fields: list[dict[str, Any]], markdown: str) -> float:
    """Fraction of the raw text's meaningful length that fields cover.

    Args:
        fields: The located field dicts.
        markdown: The raw markdown they address.

    Returns:
        A value in ``[0, 1]``; the denominator ignores border whitespace.
    """
    covered = sum(field["end"] - field["start"] for field in fields if field["end"] > field["start"])
    return round(min(1.0, covered / (len(markdown.strip()) or 1)), 4)
