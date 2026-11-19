"""The findings of the built-in family `builtin:tag_namespace:*` (GD27) and the evaluations
behind them (H6): the pass over documents that `rules check`, `on_write`, `on_check` and
`tags check` share; the evaluation of one document is `builtin_tag_rules.evaluate`."""

from __future__ import annotations

from pathlib import Path
from typing import Any

from sldb.api.rules.builtin_tag_rules import PREFIX, evaluate, in_scope, payload_of, tag_rules, tag_scope
from sldb.api.rules.rule_graph import RuleGraph, rule_graph
from sldb.api.stores.open_store import open_store
from sldb.core.finding import Finding
from sldb.store.semantic_tags import namespaced_tags


def store_findings(store: str | Path | None) -> list[Finding]:
    """The family over every local document; a store without namespaces is not read."""
    store_path = open_store(store, mode="readonly").store_path
    return family_findings(rule_graph(store_path, None), None) if tag_rules(store_path) else []


def family_evaluations(graph: RuleGraph, nodes: list[str] | None) -> list[tuple[str, dict[str, Any]]]:
    """Every evaluation of the family on `nodes` (every local document when None), by document
    then namespace: `(namespace, eval finding)`. Findings and `tag_evaluations` read this one pass."""
    rules, models = tag_rules(graph.store_path), tag_scope(graph.store_path)
    scoped = [node for node in (sorted(graph.local) if nodes is None else nodes) if in_scope(graph, models, node)] if rules else []
    return [(name, evaluate(graph, rules, name, node)) for node in scoped for name in _names(graph, node)]


def family_findings(graph: RuleGraph, nodes: list[str] | None) -> list[Finding]:
    """The findings on `nodes` (every local document when None), by document then namespace."""
    return findings_of(graph, family_evaluations(graph, nodes))


def findings_of(graph: RuleGraph, evaluations: list[tuple[str, dict[str, Any]]]) -> list[Finding]:
    """The error findings of the evaluations that do not hold."""
    return [_finding(graph, name, result) for name, result in evaluations if result["holds"] != "true"]


def _names(graph: RuleGraph, node: str) -> list[str]:
    return sorted({namespace for namespace, _ in namespaced_tags(payload_of(graph, node))})


def _finding(graph: RuleGraph, name: str, found: dict[str, Any]) -> Finding:
    from sldb.api.rules.rules_check import explanation

    what = explanation({"name": PREFIX + name}, found)
    return Finding("error", f"rules/{PREFIX}{name}", found["node"], what, _fix(graph, name, found), graph.semantics(found["node"]).get("path"))


def _fix(graph: RuleGraph, name: str, found: dict[str, Any]) -> str:
    """What to do about a failing evaluation: declare the namespace, or anchor what is missing."""
    seen = found["seen"]
    if "missing" in seen:
        anchored = tag_rules(graph.store_path)[name].anchored_by
        where = f"a {anchored['model']} document whose `{anchored['field']}` anchors it"
        return f"Create {where} for each of: {', '.join(seen['missing'])}; or change the tags {', '.join(seen['tags'])} of {found['node']} to anchored ones."
    declared = ", ".join(seen.get("declared", [])) or "none"
    tags = ", ".join(seen.get("tags", []))
    return (f"Declare the namespace `{name}` under `tag_namespaces` in .sldb/store.yaml (`- name: {name}`), "
            f"or change the tags {tags} of {found['node']} to a declared namespace (declared: {declared}; `sldb tags namespaces` lists them).")
