"""`on_transition` (GO08, rules.md §9): the rules a transition of a document must pass.

The subject is the document that transitions, read with the payload the edge conditions read
(not its projection): the edges' ends are states, not subjects. Every `on_transition` rule that
applies to it is evaluated once; the same findings hold for every edge it may take
(`edges_holding`, `edges_blocked`). A store that registers no RuleDoc has none.
"""

from __future__ import annotations

from pathlib import Path
from typing import Any

from sldb.api.rules.rule_graph import RuleGraph, rule_graph
from sldb.api.rules.rule_subjects import RULE_MODEL, applies, rules_of, subject_in
from sldb.api.rules.rules_check import rule_finding
from sldb.api.stores.open_store import open_store
from sldb.core.finding import Finding
from sldb.store.io import load_models_index, load_store_index
from sldb.store.layout import project_root


def transition_findings(store: str | Path | None, document: str, subject: dict[str, Any], pythonpath: str | None = None) -> list[Finding]:
    """The findings of the `on_transition` rules on `document` (a reference, as in `rules check
    --subject`) reading `subject`, ordered by the rule's export id."""
    store_path = open_store(store, mode="readonly").store_path
    if not has_rules(store_path):
        return []
    graph, node = subject_in(rule_graph(store_path, None), document, pythonpath)
    return payload_findings(graph, "on_transition", node, subject)


def payload_findings(graph: RuleGraph, moment: str, node: str, payload: dict[str, Any]) -> list[Finding]:
    """The findings of the rules of `moment` that apply to `node` read as `payload`."""
    seen = graph.with_payload(node, payload)
    rules = [rule for rule in rules_of(graph) if rule.get("moment") == moment]
    found = (rule_finding(seen, rule, node) for rule in rules if applies(seen, rule, node) is None)
    return [finding for finding in found if finding is not None]


def has_rules(store_path: Path) -> bool:
    """Whether the store registers RuleDoc or a model built on it: without one, no rule runs."""
    root = project_root(store_path)
    indexes = (load_models_index(root / m.models_index) for m in load_store_index(store_path).models)
    return any(RULE_MODEL == i.name or RULE_MODEL in i.base_models for i in indexes)
