"""What a model's `__compositions__` contribute: one `composes` edge per ref it reads.

A composed field is a `render` marker: its text is assembled out of other documents and is
never extracted back, so the parent's payload holds the refs but not the result. Those refs
were the one declaration that named another document and did not reach the graph, which left
impact radius unable to follow the recursion -- change a child and nothing said which composed
parent went stale.

A ref is a project path (`desk/tasks/task-a.md`), not an export id, so the target cannot be
resolved here: which document owns a path is another document's business, and a shard may not
read one. The edge is emitted with the path in `metadata["ref_path"]` and a placeholder target;
`composition_targets.resolve_composition_edges` rewrites it when the index is composed, where
the cross-document rules already live. A ref that no document owns is dropped there, like any
other `origin: "schema"` edge that dangles.
"""

from __future__ import annotations

from typing import Any

from sldb.store.models import EdgeRecord

COMPOSES = "composes"
UNRESOLVED_TARGET = "sldb://unresolved_path/"
Payload = dict[str, Any]


def composition_edges(source: str, model_type: Any | None, payload: Payload | None) -> list[EdgeRecord]:
    """One edge per ref held by a composed field's source field, in declaration order.

    Args:
        source: Node id of the composing document.
        model_type: The imported model class, or None when it cannot be imported.
        payload: The document's extracted payload, or None when it cannot be read.

    Returns:
        `composes` edges whose target is still a path, to be resolved at compose time.
    """
    if model_type is None or payload is None:
        return []
    compositions: dict[str, dict[str, Any]] = getattr(model_type, "__compositions__", {}) or {}
    return [e for name, spec in compositions.items() for e in _field_edges(source, name, spec, payload)]


def _field_edges(source: str, field: str, spec: dict[str, Any], payload: Payload) -> list[EdgeRecord]:
    """The edges one composed field declares, read from the field its spec composes."""
    source_field = spec.get("source_field")
    if not source_field:
        return []
    return [_edge(source, field, source_field, spec, ref, index) for index, ref in enumerate(_refs(payload.get(source_field)))]


def _edge(source: str, field: str, source_field: str, spec: dict[str, Any], ref: str, index: int) -> EdgeRecord:
    """One `composes` edge, carrying which field composed it and the ref as authored."""
    metadata = {"origin": "schema", "field": field, "source_field": source_field, "ref_path": ref, "ref_index": index}
    if spec.get("model"):
        metadata["composed_model"] = str(spec["model"]).rsplit(":", 1)[-1]
    return EdgeRecord(source=source, target=f"{UNRESOLVED_TARGET}{ref}", relation=COMPOSES, metadata=metadata)


def _refs(value: Any) -> list[str]:
    """The refs held by a composed field's source field, normalized as `compose_field` reads them."""
    raw = value if isinstance(value, list) else [value]
    return [item.strip().strip("`") for item in raw if isinstance(item, str) and item.strip().strip("`")]
