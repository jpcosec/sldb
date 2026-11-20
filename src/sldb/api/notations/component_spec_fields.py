"""Label, kind and group of a component-spec node taken from a document's payload.

`--label-field`, `--kind-field` and `--group-field` of `sldb notations from-graph`: a field name
reads `payload[field]`; `tag:<namespace>` reads the first entry of `payload["tags"]` that starts
with `<namespace>:` and uses what follows. A value that is missing or empty falls back to what
the node had (the id, the model).
"""

from __future__ import annotations

from typing import Any

from sldb.api.notations.component_spec_ids import sanitize_id

TAG_PREFIX = "tag:"


def field_value(payload: dict | None, field: str | None) -> str | None:
    """The text a field (or `tag:<namespace>`) holds in `payload`, or None if missing/empty."""
    if not payload or not field:
        return None
    if field.startswith(TAG_PREFIX):
        return _tag_value(payload.get("tags"), field[len(TAG_PREFIX):])
    value = payload.get(field)
    return str(value).strip() or None if isinstance(value, (str, int, float, bool)) else None


def _tag_value(tags: Any, namespace: str) -> str | None:
    prefix = f"{namespace}:"
    for tag in tags if isinstance(tags, list) else []:
        if isinstance(tag, str) and tag.startswith(prefix) and tag[len(prefix):].strip():
            return tag[len(prefix):].strip()
    return None


def apply_fields(node: dict, payload: dict | None, label_field: str | None, kind_field: str | None) -> dict:
    """`node` with its label/kind replaced by the payload's values, where there are any."""
    node["label"] = field_value(payload, label_field) or node["label"]
    node["kind"] = field_value(payload, kind_field) or node["kind"]
    return node


def add_groups(spec_nodes: dict, members: dict[str, str | None]) -> None:
    """One container node per group value, with `contains` of its members (spec id -> value)."""
    for spec_id, value in members.items():
        if value is None:
            continue
        container = _container(spec_nodes, value)
        container.setdefault("contains", []).append(spec_id)


def _container(spec_nodes: dict, value: str) -> dict:
    cid = sanitize_id(f"group_{value}")
    while cid in spec_nodes and spec_nodes[cid].get("kind") != "group":
        cid += "_g"
    return spec_nodes.setdefault(cid, {"label": value, "kind": "group"})
