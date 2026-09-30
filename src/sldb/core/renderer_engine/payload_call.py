"""Call ``render_payload`` without forcing subclasses to know about recorders.

Models outside sldb (deskops' ``TaskDoc`` and ``RoleDoc``, for instance) override
``StructuredNLDoc.render_payload`` with the original ``(self)`` signature. Passing
``recorder=`` unconditionally would raise ``TypeError`` on those models, so the
parameter is only forwarded when the override actually accepts it. Such a model
still renders and still records every marker span; only the composed-field
provenance of :mod:`sldb.models.structured_doc` is skipped.
"""

from __future__ import annotations

import inspect
from typing import Any


def render_payload_of(model: Any, recorder: Any) -> dict[str, Any]:
    """The model's render payload, recorder-aware only when the model is.

    Args:
        model: The document instance to take the payload from.
        recorder: The active ``SpanRecorder``, or None when not recording.

    Returns:
        The payload mapping the renderer feeds to the template.
    """
    if recorder is None or not accepts_recorder(model.render_payload):
        return model.render_payload()
    return model.render_payload(recorder=recorder)


def accepts_recorder(method: Any) -> bool:
    """Whether a ``render_payload`` implementation takes a ``recorder`` argument.

    Args:
        method: The bound ``render_payload`` of a document instance.

    Returns:
        True when the signature declares ``recorder`` or absorbs keywords.
    """
    try:
        params = inspect.signature(method).parameters
    except (TypeError, ValueError):
        return False
    return "recorder" in params or any(p.kind is p.VAR_KEYWORD for p in params.values())
