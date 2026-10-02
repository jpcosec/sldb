"""Extract segments from raw markdown, naming a model registered in a store.

Two failures are possible here and they are not the same thing: the model may
not be registered (the caller named something that does not exist), or the
markdown may not satisfy the model (the caller's text is the problem). Raising
distinct typed errors lets a boundary answer 404 for the first and 422 for the
second instead of collapsing both into one opaque status.
"""

from __future__ import annotations

from pathlib import Path

from sldb.api.model_registry.load_registered_model import load_registered_model
from sldb.api.segments.build_extraction_segments import build_extraction_segments
from sldb.api.segments.extraction_segments import ExtractionSegments
from sldb.core.exceptions import SLDBValidationError


def extract_markdown_segments(store_path: Path, pythonpath: str | None, model: str, markdown: str) -> ExtractionSegments:
    """Locate the fields of a registered model inside raw markdown.

    Args:
        store_path: Path of the ``.sldb`` store the model is registered in.
        pythonpath: Import root for resolving the model class, or None.
        model: Name of a model registered in the store.
        markdown: The raw markdown to read.

    Returns:
        The extraction with every field's span over the raw text.

    Raises:
        SLDBStoreError: When no such model is registered in the store.
        SLDBModelError: When the registered model class cannot be imported.
        SLDBValidationError: When the markdown does not satisfy the model; the
            underlying reason is kept in ``details``.
    """
    model_type = load_registered_model(store_path, model, pythonpath).model_type
    try:
        return build_extraction_segments(model_type, markdown, store_path.parent)
    except Exception as exc:
        raise SLDBValidationError(_reason(model, exc), {"model": model, "cause": type(exc).__name__}) from exc


def _reason(model: str, exc: Exception) -> str:
    """A message saying the markdown, not the model, is what failed.

    Args:
        model: Name of the model the markdown was read with.
        exc: The error extraction raised.

    Returns:
        A single-line, human-readable explanation.
    """
    detail = " ".join(str(exc).split())
    return f"The markdown does not extract as '{model}': {detail}"
