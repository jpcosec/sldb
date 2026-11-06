"""The built-in rule family `builtin:tag_namespace:<name>` (GD27, docs/architecture/tags.md):
the `tag_namespaces` of `store.yaml`, checked where the RuleDocs are (`on_write`, `on_check`,
`rules check`, `rules explain`) and reported as their findings (code `rules/<id>`).

On a document, the rule of namespace `<name>` holds when every tag `<name>:value` it carries
names a declared namespace and, with `anchored_by`, every tag the namespace requires for the
value (`TagNamespace.required`) is the `field` of a local document of `model`, the document
being written included. Without `tag_namespaces` the family reads nothing.
"""

from __future__ import annotations

from pathlib import Path
from typing import Any

from sldb.api.rules.rule_graph import RuleGraph, rule_graph
from sldb.api.stores.open_store import open_store
from sldb.api.stores.store_declaration import declaration_path, load_declaration
from sldb.api.stores.tag_namespace import TagNamespace
from sldb.core.exceptions import SLDBDocumentTargetError
from sldb.core.finding import Finding
from sldb.store.semantic_tags import namespaced_tags, split_namespace

PREFIX = "builtin:tag_namespace:"


def tag_rules(store_path: Path) -> dict[str, TagNamespace]:
    """The declared namespaces by name; empty without a declaration or without the key."""
    if not declaration_path(store_path).is_file():
        return {}
    return {namespace.name: namespace for namespace in load_declaration(store_path).tag_namespaces}


def store_findings(store: str | Path | None) -> list[Finding]:
    """The family over every local document; a store without namespaces is not read."""
    store_path = open_store(store, mode="readonly").store_path
    return family_findings(rule_graph(store_path), None) if tag_rules(store_path) else []


def family_findings(graph: RuleGraph, nodes: list[str] | None) -> list[Finding]:
    """The findings on `nodes` (every local document when None), by document then namespace."""
    rules = tag_rules(graph.store_path)
    found = [(node, name) for node in (sorted(graph.local) if nodes is None else nodes) for name in _names(graph, node)] if rules else []
    results = [(name, evaluate(graph, rules, name, node)) for node, name in found]
    return [_finding(graph, name, result) for name, result in results if result["holds"] != "true"]


def explain(graph: RuleGraph, rule: str, node: str) -> dict[str, Any]:
    """`rules explain` of a built-in rule: its eval finding on `node`; no namespaces, no rule."""
    rules = tag_rules(graph.store_path)
    if not rules:
        raise SLDBDocumentTargetError(f"Unknown document target: {rule}")
    return {"rule": rule, "subject": node, "finding": evaluate(graph, rules, rule.removeprefix(PREFIX), node)}


def evaluate(graph: RuleGraph, rules: dict[str, TagNamespace], name: str, node: str) -> dict[str, Any]:
    """The eval finding (node, holds, clause, seen) of `builtin:tag_namespace:<name>` on `node`."""
    tags = [tag for namespace, tag in namespaced_tags(payload_of(graph, node)) if namespace == name]
    if name not in rules:
        return _found(node, not tags, "namespace declared", {"namespace": name, "tags": tags, "declared": sorted(rules)})
    if rules[name].anchored_by is None:
        return _found(node, True, "namespace declared", {"namespace": name, "tags": tags})
    missing = _missing(rules[name], tags, anchors_of(graph, rules[name]))
    clause = f"each prefix anchored by {rules[name].anchored_by['model']}.{rules[name].anchored_by['field']}"
    return _found(node, not missing, clause, {"namespace": name, "tags": tags, "missing": missing})


def anchors_of(graph: RuleGraph, namespace: TagNamespace) -> dict[str, str]:
    """Anchor tag -> export id of the local document of `anchored_by.model` whose `field` is
    that tag, as `graph` reads it (a payload being written included)."""
    model, field = namespace.anchored_by["model"], namespace.anchored_by["field"]
    found: dict[str, str] = {}
    for node in sorted(graph.local | ({graph.override[0]} if graph.override else set())):
        item = graph.located(node)[1]
        value = item["payload"].get(field) if model in (item["model"], *item["base_models"]) else None
        if isinstance(value, str) and split_namespace(value)[0] == namespace.name:
            found.setdefault(value, node)
    return found


def payload_of(graph: RuleGraph, node: str) -> dict[str, Any]:
    """The payload `graph` reads for `node` (its projection, or the payload overriding it)."""
    return graph.located(node)[1]["payload"]


def _names(graph: RuleGraph, node: str) -> list[str]:
    return sorted({namespace for namespace, _ in namespaced_tags(payload_of(graph, node))})


def _missing(namespace: TagNamespace, tags: list[str], anchors: dict[str, str]) -> list[str]:
    """The required tags without an anchor, top-down, once each."""
    missing: list[str] = []
    for tag in tags:
        missing += [t for t in namespace.required(tag) if t not in anchors and t not in missing]
    return missing


def _found(node: str, holds: bool, clause: str, seen: dict[str, Any]) -> dict[str, Any]:
    return {"node": node, "holds": "true" if holds else "false", "clause": clause, "seen": seen}


def _finding(graph: RuleGraph, name: str, found: dict[str, Any]) -> Finding:
    from sldb.api.rules.rules_check import explanation

    what = explanation({"name": PREFIX + name}, found)
    return Finding("error", f"rules/{PREFIX}{name}", found["node"], what, "", graph.semantics(found["node"]).get("path"))
