from __future__ import annotations
from typing import Any

class RuntimeDocProxy:
    """Proxy object for runtime document evaluation."""
    payload: dict[str, Any]
    name: str
    model_type: type

    def __init__(self, payload: dict[str, Any], name: str, model_type: type) -> None:
        self.payload = payload
        self.name = name
        self.model_type = model_type
