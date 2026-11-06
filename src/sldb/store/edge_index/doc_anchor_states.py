"""The state of a document anchor (GO07, docs/architecture/anchoring.md §6): `intact` when the
contract hash it saw is the target's now, `changed` when not, `lost` when the target is not
tracked or the anchor carries no hash. Computed when the index is composed or a save pins,
never written to a shard: the target's contract hash comes from its `field_hashes` (GO04) and
its class (`model_type_of`, as for `contract_signature`); a class that cannot be loaded hashes
by the rule of an absent `__contract__` (rules-language.md §5).

`with_anchor_states` adds `<field>__anchor_state` to the payload of each document node whose
model declares the field in `__doc_anchors__` and whose payload holds it: a scalar for a str
field, a list aligned by index for a list[str] one (an empty item reads null).
"""

from __future__ import annotations

from pathlib import Path
from typing import Any, Callable, Iterable

from sldb.store.edge_index.live_stale import ModelTypeOf
from sldb.store.edge_index.node_ids import doc_node_id, kind
from sldb.store.graph.language.contract_hash import contract_hash
from sldb.store.io import load_store_index
from sldb.store.io.shards import load_document_shard
from sldb.store.layout import documents_shard_path, project_root
from sldb.store.models import EdgeNodeRecord

INTACT, CHANGED, LOST = "intact", "changed", "lost"
SUFFIX = "__anchor_state"
#: export id -> (the target is tracked, its contract hash now or None).
Current = Callable[[str], tuple[bool, str | None]]


class _NoContract:
    """Stands for a class that could not be loaded: no `__contract__`, so every field counts."""


def anchor_contract_hash(model_type: Any | None, field_hashes: dict[str, str]) -> str | None:
    """The target's contract hash; None when its `__contract__` is declared empty (H11)."""
    try:
        return contract_hash(model_type if model_type is not None else _NoContract, field_hashes)
    except ValueError:
        return None


def anchor_state(value: Any, current: Current) -> str | None:
    """`intact`, `changed` or `lost` of one value; None for an empty value or a non-anchor."""
    from sldb.store.model_contract import doc_anchor

    if (parsed := doc_anchor(value)) is None:
        return None
    exists, now = current(parsed[0])
    if not exists or parsed[1] is None:
        return LOST
    return INTACT if parsed[1] == now else CHANGED


def field_states(value: Any, current: Current) -> Any:
    """The state of a str field, or the states of a list[str] field aligned by index."""
    return [anchor_state(v, current) for v in value] if isinstance(value, list) else anchor_state(value, current)


def store_current(store_path: Path, model_type_of: ModelTypeOf) -> Current:
    """Targets read from a store's document shards (the save pins with it)."""
    models = {m.name: m.model_ref for m in load_store_index(store_path).models}

    def current(export_id: str) -> tuple[bool, str | None]:
        model, _, name = export_id.partition(":")
        entry = load_document_shard(documents_shard_path(store_path, model, name)) if model in models and name else None
        if entry is None:
            return False, None
        return True, anchor_contract_hash(model_type_of(models[model], project_root(store_path)), entry.field_hashes)

    return current


def nodes_current(nodes: dict[str, EdgeNodeRecord], classes: dict[tuple[str, str], Any], prefix: str = "") -> Current:
    """Targets read from composed nodes; `prefix` qualifies an id read in a linked store."""

    def current(export_id: str) -> tuple[bool, str | None]:
        node = nodes.get(doc_node_id(prefix + export_id))
        return (False, None) if node is None else (True, anchor_contract_hash(classes.get(class_key(node)), node.field_hashes))

    return current


def store_classes(store_paths: Iterable[Path], model_type_of: ModelTypeOf) -> dict[tuple[str, str], Any]:
    """(store path, model name) -> class or None, for every model the stores register."""
    return {(str(path), m.name): model_type_of(m.model_ref, project_root(path)) for path in store_paths for m in load_store_index(path).models}


def class_key(node: EdgeNodeRecord) -> tuple[str, str]:
    """The `store_classes` key of a composed document node (its `source` facet names its store)."""
    return str((node.facets.get("source") or {}).get("store_path", "")), node.node_type


def with_anchor_states(nodes: dict[str, EdgeNodeRecord], store_paths: list[Path], model_type_of: ModelTypeOf | None, fields: dict[str, list[str]]) -> dict[str, EdgeNodeRecord]:
    """`nodes` with the derived entries on copies of the anchoring documents' nodes; `fields`
    (the projected names per model) gains them. Without `model_type_of` nothing is derived."""
    if model_type_of is None:
        return nodes
    classes = store_classes(store_paths, model_type_of)
    return {node_id: _derived(node, nodes, classes, fields) for node_id, node in nodes.items()}


def _derived(node: EdgeNodeRecord, nodes: dict[str, EdgeNodeRecord], classes: dict, fields: dict[str, list[str]]) -> EdgeNodeRecord:
    from sldb.store.model_contract import doc_anchor_fields

    names = [f for f in doc_anchor_fields(classes.get(class_key(node))) if f in node.payload] if kind(node.id) == "document" else []
    if not names:
        return node
    store = node.semantics.get("store")
    current = nodes_current(nodes, classes, f"{store}:" if store else "")
    fields[node.node_type] = sorted(set(fields.get(node.node_type) or []) | {f + SUFFIX for f in names})
    return node.model_copy(update={"payload": {**node.payload, **{f + SUFFIX: field_states(node.payload[f], current) for f in names}}})
