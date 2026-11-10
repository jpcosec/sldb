"""Whether a store's rules can read a linked store's document (rules.md §9, GO08): when they
cannot, they are evaluated over the store's own edge index, and the federation is not composed.

A local document reads the same in the store's own index as in the composed one (its node, its
local edges and its model family come first) except for what names a linked store's document:
a reference or a document anchor written `alias:Model:name`, which only the composed index
resolves; an edge of a linked store never points at a local document. So the rules read only
the store when (1) every local document's model family is the same in the store's own index,
(2) no path of any rule takes a `rel:` step (relation types, tags and models are one
vocabulary across stores: such a step may pass through them into a linked store), (3) no field
a path names holds, on a local document, a reference left unresolved that names a linked
store's document or an edge to a document that is not local, and (4) no document anchor of a
local document names a linked store's document. Anything else, including a rule that does not
parse, reads the federation: correct before fast.
"""

from __future__ import annotations

from typing import Any, Iterable

from sldb.store.edge_index.federation import federated_stores
from sldb.store.edge_index.node_ids import bare, kind, model_node_id
from sldb.store.graph.language.predicate_ast import walk
from sldb.store.graph.language.predicate_parser import parse_predicate
from sldb.store.io import load_store_index
from sldb.store.model_contract import doc_anchor

_ANCHOR_STATE = "__anchor_state"


def needs_linked(graph: Any) -> bool:
    """Whether the rules of `graph` (a `RuleGraph` over the store's own index) may read a
    linked store's document: never without links; else (1) to (4) of the module."""
    from sldb.api.rules.rule_subjects import rules_of

    linked = federated_stores(graph.store_path, True)[1:]
    if not linked:
        return False
    if not families_complete(graph.index, graph.local, {m.name for path, _ in linked for m in load_store_index(path).models}):
        return True
    return reads_linked(graph.index, graph.local, rules_of(graph))


def reads_linked(index: Any, local: frozenset[str], rules: Iterable[dict[str, Any]]) -> bool:
    """Whether `rules`, evaluated on the local documents of `index` (the store's own), may
    read a document of a linked store (see the module)."""
    steps = rule_steps(rules)
    if steps is None or any(step[0] == "rel" for step in steps):
        return True
    fields = {step[1] for step in steps}
    return _crosses(index, local, fields) or _anchors_linked(index, local)


def families_complete(index: Any, local: frozenset[str], linked_models: set[str]) -> bool:
    """Whether the model of every local document and its bases, transitively, read the same in
    `index` as composed: each has a model node here, or no linked store registers it (then the
    composed index has none either; a model node is its registering store's contribution)."""
    pending = {index.node(f"sldb://document/{node}").node_type for node in local}
    seen: set[str] = set()
    while pending:
        model = pending.pop()
        seen.add(model)
        record = index.node(model_node_id(model))
        if record is None and model in linked_models:
            return False
        pending |= set(record.semantics.get("base_models") or [] if record is not None else []) - seen
    return True


def rule_steps(rules: Iterable[dict[str, Any]]) -> set[tuple] | None:
    """Every path step of the rules' predicates (`subject`, `where`, `condition`); None when
    one does not parse (then nothing is known of where it reads)."""
    try:
        roots = [parse_predicate(text).root for rule in rules for text in _texts(rule)]
    except Exception:  # noqa: BLE001 - an unparseable rule reads as one that may read anywhere
        return None
    return {step for root in roots for node in walk(root) for step in _path(node)}


def qualified(export_id: Any) -> bool:
    """Whether an id names a linked store's document (`alias:Model:name`, also as an anchor
    `doc:alias:Model:name@...`)."""
    return isinstance(export_id, str) and export_id.removeprefix("doc:").split("@", 1)[0].split("#", 1)[0].count(":") >= 2


def _texts(rule: dict[str, Any]) -> list[str]:
    return [text for text in (rule.get(key) for key in ("subject", "where", "condition")) if isinstance(text, str) and text.strip()]


def _path(node: tuple) -> tuple:
    if node[0] == "quant":
        return node[3]
    return node[2] if node[0] == "count" else ()


def _crosses(index: Any, local: frozenset[str], fields: set[str]) -> bool:
    unresolved = (u for u in index.unresolved_references if u.field in fields and u.source in local)
    if any(qualified(u.target) or qualified(u.target_export_id) for u in unresolved):
        return True
    edges = (e for e in index.edges if e.relation == "references" and e.metadata.get("field") in fields)
    return any(kind(end) == "document" and bare(end) not in local for e in edges for end in (e.source, e.target))


def _anchors_linked(index: Any, local: frozenset[str]) -> bool:
    payloads = (index.node(f"sldb://document/{node}").payload for node in local)
    names = ((payload, key[: -len(_ANCHOR_STATE)]) for payload in payloads for key in payload if key.endswith(_ANCHOR_STATE))
    values = (v for payload, name in names for v in _listed(payload.get(name)))
    return any(qualified((doc_anchor(v) or ("",))[0]) for v in values)


def _listed(value: Any) -> list[Any]:
    return value if isinstance(value, list) else [value]
