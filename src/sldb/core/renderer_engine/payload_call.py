"""Call ``render_payload`` without forcing subclasses to know about recorders or ref roots.

Models outside sldb (deskops' ``TaskDoc`` and ``RoleDoc``, for instance) override
``StructuredNLDoc.render_payload`` with the original ``(self)`` signature. Passing
``recorder=`` or ``ref_root=`` unconditionally would raise ``TypeError`` on those models,
so each parameter is only forwarded when the override actually accepts it. Such a model
still renders and still records every marker span; only the composed-field provenance
of :mod:`sldb.models.structured_doc` and the ref root are skipped.
"""

from __future__ import annotations

import inspect
from pathlib import Path
from typing import Any


def render_payload_of(model: Any, recorder: Any, ref_root: Path | None = None) -> dict[str, Any]:
    """The model's render payload, passing only the arguments the model accepts.

    Args:
        model: The document instance to take the payload from.
        recorder: The active ``SpanRecorder``, or None when not recording.
        ref_root: Directory composition refs resolve against, or None.

    Returns:
        The payload mapping the renderer feeds to the template.
    """
    wanted = {"recorder": recorder, "ref_root": ref_root}
    kwargs = {k: v for k, v in wanted.items() if v is not None and accepts_param(model.render_payload, k)}
    return model.render_payload(**kwargs)


def accepts_param(method: Any, name: str) -> bool:
    """Whether a ``render_payload`` implementation takes the argument ``name``.

    Args:
        method: The bound ``render_payload`` of a document instance.
        name: The keyword to look for.

    Returns:
        True when the signature declares ``name`` or absorbs keywords.
    """
    try:
        params = inspect.signature(method).parameters
    except (TypeError, ValueError):
        return False
    return name in params or any(p.kind is p.VAR_KEYWORD for p in params.values())


def accepts_recorder(method: Any) -> bool:
    """Whether a ``render_payload`` implementation takes a ``recorder`` argument."""
    return accepts_param(method, "recorder")
