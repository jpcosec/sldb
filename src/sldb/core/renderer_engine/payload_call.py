"""Call ``render_payload`` without forcing subclasses to know about recorders or ref roots."""

from __future__ import annotations

import inspect
from pathlib import Path
from typing import Any


def render_payload_of(
    model: Any,
    recorder: Any,
    ref_root: Path | None = None,
    field_resolver: Any = None,
) -> dict[str, Any]:
    """The model's render payload, passing only the arguments the model accepts."""
    wanted = {"recorder": recorder, "ref_root": ref_root, "field_resolver": field_resolver}
    kwargs = {k: v for k, v in wanted.items() if v is not None and accepts_param(model.render_payload, k)}
    return model.render_payload(**kwargs)


def accepts_param(method: Any, name: str) -> bool:
    """Whether a ``render_payload`` implementation takes the argument ``name``."""
    try:
        params = inspect.signature(method).parameters
    except (TypeError, ValueError):
        return False
    return name in params or any(p.kind is p.VAR_KEYWORD for p in params.values())


def accepts_recorder(method: Any) -> bool:
    """Whether a ``render_payload`` implementation takes a ``recorder`` argument."""
    return accepts_param(method, "recorder")
