from typing import Any

def flatten_payload(payload: Any, prefix: str = "") -> list[tuple[str, Any]]:
    if isinstance(payload, dict):
        pairs: list[tuple[str, Any]] = []
        for key, value in payload.items():
            path = f"{prefix}.{key}" if prefix else key
            pairs.extend(flatten_payload(value, path))
        return pairs
    return [(prefix, payload)]
