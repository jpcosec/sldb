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
    return sorted(set(flatten_model_semantics(model_type)) | set(payload_tags(payload)))


def payload_tags(payload: dict) -> list[str]:
    """The document-level tags: the `semantic_tags` and `tags` fields, stripped, in order."""
    found: list[str] = []
    for field_name in ("semantic_tags", "tags"):
        values = payload.get(field_name) or []
        found += [t.strip() for t in values if isinstance(t, str) and t.strip()] if isinstance(values, list) else []
    return found


def split_namespace(tag: str) -> tuple[str | None, str]:
    """`(namespace, value)` of `namespace:value`, cut at the first colon; `(None, tag)` without one."""
    namespace, colon, value = tag.partition(":")
    return (namespace, value) if colon and namespace else (None, tag)


def namespaced_tags(payload: dict) -> list[tuple[str, str]]:
    """`(namespace, tag)` of each payload tag that has a namespace, in order, once each."""
    pairs: list[tuple[str, str]] = []
    for tag in payload_tags(payload):
        namespace = split_namespace(tag)[0]
        if namespace is not None and (namespace, tag) not in pairs:
            pairs.append((namespace, tag))
    return pairs


def tag_prefixes(value: str) -> list[str]:
    """`a.b.c` -> `['a', 'a.b', 'a.b.c']` (empty segments are skipped)."""
    parts = [part for part in value.split(".") if part]
    return [".".join(parts[: index + 1]) for index in range(len(parts))]


def _prefix_edges(tag: str) -> list[tuple[str, str]]:
    """Generates parent-child edges for a dotted semantic tag."""
    prefixes = tag_prefixes(tag)
    return list(zip(prefixes, prefixes[1:]))
