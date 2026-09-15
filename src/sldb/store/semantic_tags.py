from __future__ import annotations


def flatten_model_semantics(model_type: type) -> list[str]:
    """Combine base and model-local semantics.

    StructuredNLDoc supplies the representation/source defaults. A concrete
    model replaces a key such as source instead of having to repeat the
    representation declaration.
    """
    semantics = {}
    for base in reversed(model_type.__mro__):
        semantics.update(base.__dict__.get("__semantics__", {}) or {})
    tags = []
    for k, v in semantics.items():
        if isinstance(v, str): tags.append(f"{k}.{v}")
        elif isinstance(v, (list, tuple)): tags.extend([".".join([k, *[str(p) for p in v]])] if v else [])
        elif isinstance(v, dict): tags.extend([".".join([k, ck, *([str(p) for p in cv] if isinstance(cv, (list, tuple)) else [str(cv)])]) for ck, cv in v.items()])
    return sorted(set(t for t in tags if t))


def collect_document_semantic_tags(model_type: type, payload: dict) -> list[str]:
    """
    Collects both model-level and document-level semantic tags.
    """
    tags = set(flatten_model_semantics(model_type))
    for field_name in ("semantic_tags", "tags"):
        payload_tags = payload.get(field_name) or []
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
