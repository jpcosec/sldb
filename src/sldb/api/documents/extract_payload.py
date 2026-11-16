"""Extract a payload from Markdown already read, without touching any store."""

from __future__ import annotations

from typing import Any

from sldb.runtime.validation import extract_model_data


def extract_payload(model_type: type, markdown: str) -> dict[str, Any]:
    """The payload `model_type`'s template extracts from `markdown`.

    Args:
        model_type: A StructuredNLDoc subclass.
        markdown: The document text, already read by the caller.
    """
    return extract_model_data(model_type, markdown)
