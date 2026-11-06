"""Render a payload while recording where every marker wrote its value."""

from __future__ import annotations

from pathlib import Path
from typing import Any

from sldb.core.renderer import SLDBRenderer
from sldb.core.renderer_engine.span_recorder import SpanRecorder

SpanWithMeta = tuple[dict[str, Any], int, int]


def render_with_spans(
    model_type: type,
    payload: dict[str, Any],
    ref_root: Path | None = None,
    field_resolver: Any = None,
) -> tuple[str, list[SpanWithMeta]]:
    """The canonical render of ``payload`` plus every value span in it."""
    recorder = SpanRecorder()
    renderer = SLDBRenderer(recorder=recorder)
    if field_resolver is not None:
        renderer.field_resolver = field_resolver
    text = renderer.render(model_type(**payload), ref_root)
    return text, [(_meta(recorder, span_id), start, end) for span_id, start, end in renderer.spans]


def _meta(recorder: SpanRecorder, span_id: int) -> dict[str, Any]:
    return {**recorder.metas[span_id], "_order": span_id}
