"""What an anchor's `ref` names when it is written as a pron form (spec 13)."""

from __future__ import annotations

from typing import Any, Callable

from sldb.store.edge_index.node_ids import doc_node_id, field_node_id, model_node_id, relation_type_node_id
from sldb.store.edge_index.ref_symbol import RefSymbol

_KERNEL_WRITES = ("change", "add", "remove", "clean", "forget")
_ONE_ARG: dict[str, Callable[[str], str]] = {
    "model": model_node_id, "where": model_node_id, "value": model_node_id, "create": model_node_id,
    "relation": relation_type_node_id, "assert": relation_type_node_id, "doc": doc_node_id,
}


def form_targets(form: Any) -> list[str]:
    """Node ids of the models, fields, relation types and documents a form names."""
    if not isinstance(form, list) or not form or not isinstance(form[0], RefSymbol):
        return []
    head, args = str(form[0]), form[1:]
    if head == "move":
        return [t for step in args for t in form_targets(step)]
    if head == "field":
        return [field_node_id(str(args[0]), str(args[1]))] if len(args) >= 2 else []
    if head in _KERNEL_WRITES:
        return _write_targets(args)
    return [_ONE_ARG[head](str(args[0]))] if head in _ONE_ARG and args else []


def _write_targets(args: list) -> list[str]:
    """A kernel write `(change (it of Model) field ...)` names the field it writes."""
    if len(args) < 2:
        return []
    noun = args[0]
    if isinstance(noun, list) and len(noun) >= 3 and str(noun[0]) in ("it", "them"):
        return [field_node_id(str(noun[2]), str(args[1]))]
    return []
