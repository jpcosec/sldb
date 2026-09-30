"""Render a payload while recording where every marker wrote its value.

This is the one entry point that ties the three pieces together: a fresh
:class:`~sldb.core.renderer_engine.span_recorder.SpanRecorder` is handed to the
renderer, the renderer decodes its own sentinels, and the recorded metadata is
matched back to the offsets by span id. The resulting text is the canonical
render — identical to ``render_model_markdown`` — because the sentinels are
removed before the final strip.
"""

from __future__ import annotations

from typing import Any

from sldb.core.renderer import SLDBRenderer
from sldb.core.renderer_engine.span_recorder import SpanRecorder

SpanWithMeta = tuple[dict[str, Any], int, int]


def render_with_spans(model_type: type, payload: dict[str, Any]) -> tuple[str, list[SpanWithMeta]]:
    """The canonical render of ``payload`` plus every value span in it.

    Args:
        model_type: The ``StructuredNLDoc`` subclass to render through.
        payload: The payload to instantiate the model with.

    Returns:
        A tuple of the canonical text and a list of ``(meta, start, end)``, where
        ``meta`` carries the field ``path``, ``marker`` kind, ``traits`` and the
        wrap order under ``_order``.
    """
    recorder = SpanRecorder()
    renderer = SLDBRenderer(recorder=recorder)
    text = renderer.render(model_type(**payload))
    return text, [(_meta(recorder, span_id), start, end) for span_id, start, end in renderer.spans]


def _meta(recorder: SpanRecorder, span_id: int) -> dict[str, Any]:
    """The recorded metadata of one span, tagged with its wrap order.

    Args:
        recorder: The recorder that collected the span.
        span_id: Index of the span in wrap order.

    Returns:
        A copy of the metadata carrying ``_order``, the nesting tiebreak.
    """
    return {**recorder.metas[span_id], "_order": span_id}
