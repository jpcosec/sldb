from __future__ import annotations


def flatten_model_semantics(model_type: type) -> list[str]:
    """
    Flattens model-level semantic metadata into a list of dotted tags.
    """
    semantics = getattr(model_type, "__semantics__", {}) or {}
    tags: list[str] = []
    for key, value in semantics.items():
        if isinstance(value, str):
            tags.append(f"{key}.{value}")
        elif isinstance(value, (list, tuple)):
            if value:
                tags.append(".".join([key, *[str(part) for part in value]]))
        elif isinstance(value, dict):
            for child_key, child_value in value.items():
                if isinstance(child_value, (list, tuple)):
                    tags.append(".".join([key, child_key, *[str(p) for p in child_value]]))
                else:
                    tags.append(f"{key}.{child_key}.{child_value}")
    return sorted(set(tag for tag in tags if tag))


def collect_document_semantic_tags(model_type: type, payload: dict) -> list[str]:
    """
    Collects both model-level and document-level semantic tags.
    """
    tags = set(flatten_model_semantics(model_type))
    payload_tags = payload.get("semantic_tags") or []
    if isinstance(payload_tags, list):
        for tag in payload_tags:
            if isinstance(tag, str) and tag.strip():
                tags.add(tag.strip())
    return sorted(tags)


def _prefix_edges(tag: str) -> list[tuple[str, str]]:
    """Generates parent-child edges for a dotted semantic tag."""
    parts = [part for part in tag.split(".") if part]
    edges: list[tuple[str, str]] = []
    for index in range(1, len(parts)):
        parent = ".".join(parts[:index])
        child = ".".join(parts[: index + 1])
        edges.append((parent, child))
    return edges
