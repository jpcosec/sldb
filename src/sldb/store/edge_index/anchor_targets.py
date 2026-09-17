"""What an anchor document names: the node ids its `ref` points at."""

from __future__ import annotations

import re
from typing import Any

from sldb.store.edge_index.form_targets import form_targets
from sldb.store.edge_index.node_ids import doc_node_id, field_node_id, model_node_id, relation_type_node_id
from sldb.store.edge_index.ref_form import read_form

_ACTION_FIELD = re.compile(r"\b([A-Za-z_]\w*)\.([A-Za-z_]\w*)=")


def anchor_targets(payload: dict[str, Any]) -> list[str]:
    """Targets of an anchor's `ref`, written as a form (`(model Table)`) or as `kind:rest`."""
    ref = str(payload.get("ref", ""))
    if ref.lstrip().startswith("("):
        return form_targets(read_form(ref))
    head, _, rest = ref.partition(":")
    if head == "compose":
        return _compose_targets(payload.get("steps") or [])
    return _scheme_targets(head, rest)


def _scheme_targets(head: str, rest: str) -> list[str]:
    if head == "field":
        return [field_node_id(*rest.split(".", 1))] if "." in rest else []
    if head == "action":
        return [field_node_id(m, f) for m, f in _ACTION_FIELD.findall(rest)]
    simple = {"model": model_node_id(rest), "predicate": model_node_id(rest.split(":", 1)[0]), "relation": relation_type_node_id(rest), "doc": doc_node_id(rest)}
    return [simple[head]] if head in simple else []


def _compose_targets(steps: list) -> list[str]:
    targets: list[str] = []
    for step in (s for s in steps if isinstance(s, dict)):
        if step.get("model"):
            targets.append(model_node_id(step["model"]))
        if step.get("relation"):
            targets.append(relation_type_node_id(step["relation"]))
    return targets
