"""Declared field values that name the target (GD22): where the edge index places them
(`schema_hits`) and what a document's payload becomes when they are rewritten or removed
(`rewritten_payload`). A rewritten value keeps the form the original named the target in
(`reshaped`): a bare name, `Model:name`, `Model/name`, a tracked path, or a document anchor
`doc:Model:name[@sha256:...]`, which is written back without its hash so the save pins it
again (GO07). A replacement that is no tracked document is written as given.
"""

from __future__ import annotations

from pathlib import Path
from typing import TYPE_CHECKING, Any

from sldb.api.edges.edge_reading import load_edge_index
from sldb.api.edges.referrer import Referrer
from sldb.models.doc_anchor_value import parse_doc_anchor

if TYPE_CHECKING:
    from sldb.api.edges.referrers import Target

_DOC = "sldb://document/"


def schema_hits(store_path: Path, export_id: str) -> list[tuple[Referrer, str]]:
    """(referrer, value as written) of every declared field reaching `export_id`, by source, field and position."""
    index = load_edge_index(store_path, include_linked=False)
    found: list[tuple[Referrer, str]] = []
    for edge in index.edges_to(export_id):
        field, declared = edge.metadata.get("field"), edge.metadata.get("declared")
        if edge.metadata.get("origin") == "schema" and field and isinstance(declared, str):
            node = index.nodes.get(edge.source)
            position = position_of(node.payload.get(field) if node is not None else None, declared)
            found.append((Referrer(source=edge.source[len(_DOC):], field=field, index=position, origin="schema"), declared))
    return sorted(found, key=lambda hit: (hit[0].source, hit[0].field or "", -1 if hit[0].index is None else hit[0].index))


def position_of(value: Any, declared: str) -> int | None:
    """Where `declared` sits in a list value; None for a scalar or when it is not there."""
    if not isinstance(value, list):
        return None
    return next((i for i, item in enumerate(value) if same_value(item, declared)), None)


def same_value(item: Any, declared: str) -> bool:
    """Whether a payload item is the declared value (the index strips spaces and backticks)."""
    return isinstance(item, str) and item.strip().strip("`").strip() == declared.strip()


def rewritten_payload(payload: dict[str, Any], hits: list[tuple[Referrer, str]], target: Target, replacement: Target | None) -> tuple[dict[str, Any], list[dict[str, Any]]]:
    """A copy of `payload` with every hit rewritten (or removed when `replacement` is None), and the changes made."""
    new, changes = dict(payload), []
    for referrer, declared in hits:
        after = None if replacement is None else reshaped(declared, target, replacement)
        current = new.get(referrer.field or "")
        new[referrer.field or ""] = list_rewritten(current, declared, after) if isinstance(current, list) else after
        changes.append({"source": referrer.source, "field": referrer.field, "index": referrer.index, "location": None, "before": declared, "after": after})
    return new, changes


def list_rewritten(items: list[Any], declared: str, after: str | None) -> list[Any]:
    """`items` with the declared value replaced by `after` (or dropped), in place, without duplicating `after`."""
    kept = [after if same_value(item, declared) else item for item in items if after is not None or not same_value(item, declared)]
    return [item for i, item in enumerate(kept) if after is None or item != after or kept.index(after) == i]


def reshaped(before: str, target: Target, replacement: Target) -> str:
    """The replacement written the way `before` named the target; as given when it is no document."""
    if replacement.model is None or target.model is None:
        return replacement.given
    anchor = parse_doc_anchor(before)
    if anchor is not None and anchor[0] == target.export_id:
        return f"doc:{replacement.export_id}"
    forms = {target.name: replacement.name, target.export_id: replacement.export_id, f"{target.model}/{target.name}": f"{replacement.model}/{replacement.name}", target.path: replacement.path, f"./{target.path}": f"./{replacement.path}"}
    return str(forms.get(before.strip().strip("`").strip(), replacement.given))
