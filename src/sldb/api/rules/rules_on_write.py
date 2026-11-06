"""`on_write` (GO08, rules.md §9): the rules a write must pass before anything is persisted.

A step of `save_document_payload`, right after the document anchors are pinned (GO07): the rule
reads the pinned payload, with the anchors' states (`<field>__anchor_state`) as the index would
compose them; paths follow the index as it is before the write. An `error` finding refuses the
write (`SLDBRuleViolationError`, nothing written); alerts are routed (`sldb.core.finding_route`)
whether the write passes or not. The document and its neighbours enter the dirty set.
The built-in family `builtin:tag_namespace:*` (GD27) runs beside the RuleDocs, also in a store
that registers none but declares `tag_namespaces`.
"""

from __future__ import annotations

from pathlib import Path
from typing import Any

from sldb.api.edges.edge_reading import model_type_of
from sldb.api.rules.builtin_tag_rules import family_findings, tag_rules
from sldb.api.rules.dirty_set import mark_dirty
from sldb.api.rules.rule_graph import rule_graph
from sldb.api.rules.rules_on_transition import has_rules, payload_findings
from sldb.core.exceptions import SLDBRuleViolationError
from sldb.core.finding import split
from sldb.core.finding_route import route
from sldb.store.edge_index.doc_anchor_states import SUFFIX, field_states, store_current
from sldb.store.model_contract import doc_anchor_fields


def check_on_write(store_path: Path, model_type: type, node: str, payload: dict[str, Any]) -> None:
    """Evaluate the `on_write` rules on `node` (`Model:name`) as `payload`; raise on an error."""
    declared = has_rules(store_path)
    if not declared and not tag_rules(store_path):
        return
    graph, read = rule_graph(store_path), anchored(store_path, model_type, payload)
    found = payload_findings(graph, "on_write", node, read) if declared else []
    errors, alerts = split(found + family_findings(graph.with_payload(node, read), [node]))
    mark_dirty(store_path, graph.index, node)
    route(alerts)
    if errors:
        raise SLDBRuleViolationError(errors)


def anchored(store_path: Path, model_type: type, payload: dict[str, Any]) -> dict[str, Any]:
    """`payload` with the state of each of its `__doc_anchors__` fields, as the index adds it."""
    names = [name for name in doc_anchor_fields(model_type) if payload.get(name)]
    if not names:
        return payload
    current = store_current(store_path, model_type_of)
    return {**payload, **{name + SUFFIX: field_states(payload[name], current) for name in names}}
