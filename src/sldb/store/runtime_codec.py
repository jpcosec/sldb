from __future__ import annotations
from typing import Any

from sldb.models.provenance_block import index_block  # noqa: F401 - the seam: the store reads a document's provenance block through here


class RuntimeCodec:
    """Default codec wrapping the runtime's extract_model_data (local import)."""
    def extract(self, model_type: Any, markdown_text: str) -> dict[str, Any]:
        from sldb.runtime.validation import extract_model_data
        return extract_model_data(model_type, markdown_text)
