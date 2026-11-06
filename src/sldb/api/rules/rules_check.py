"""`sldb rules check`: the local rules evaluated, each failure a core `Finding` (GO06).

With a subject, every rule that applies to that document, of any moment; without one, the
`on_check` rules over every local document they apply to. Only `false` and `incomplete` become
findings: `false` at the rule's severity with code `rules/<name>`, `incomplete` always an alert
with code `rules/<name>/incomplete`. Nothing of the result is stored. The built-in family
`builtin:tag_namespace:*` (GD27) follows the RuleDocs' findings, on the same documents.
"""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from sldb.api.rules.builtin_tag_rules import family_findings
from sldb.api.rules.fixpoint import witness
from sldb.api.rules.rule_graph import RuleGraph, rule_graph
from sldb.api.rules.rule_subjects import applies, resolve_subject, rules_of
from sldb.core.finding import Finding


def rules_check(store: str | Path | None, subject: str | None = None, pythonpath: str | None = None) -> list[Finding]:
    """The findings of the store's rules (see the module); `subject` is a document reference
    (`Model:name`, `store:Model:name` or a path). An unknown subject is `SLDBDocumentTargetError`."""
    graph = rule_graph(store)
    rules = rules_of(graph)
    nodes = None if subject is None else [resolve_subject(graph, subject, pythonpath)]
    if nodes is not None:
        pairs = [(rule, nodes[0]) for rule in rules if applies(graph, rule, nodes[0]) is None]
    else:
        pairs = [(r, n) for r in rules if r.get("moment") == "on_check" for n in graph.domain(r["subject"]) if applies(graph, r, n) is None]
    found = [f for f in (rule_finding(graph, rule, node) for rule, node in pairs) if f is not None]
    return found + family_findings(graph, nodes)


def rule_finding(graph: RuleGraph, rule: dict[str, Any], node: str) -> Finding | None:
    """The finding of `rule` on `node` (None when its condition holds)."""
    found = graph.holds(rule["condition"], node)
    if found["holds"] == "true":
        return None
    incomplete = found["holds"] == "incomplete"
    level = "alert" if incomplete else rule.get("severity", "error")
    code = f"rules/{rule['name']}" + ("/incomplete" if incomplete else "")
    named = witness(graph, rule["condition"], found)
    return Finding(level, code, node, explanation(rule, found, named), "", graph.semantics(node).get("path"))


def explanation(rule: dict[str, Any], found: dict[str, Any], named: tuple[str, dict] | None = None) -> str:
    """`<clause> (seen: <seen as compact JSON>)`, after `<message> | ` when the rule has one,
    then ` (witness: <Model:name> <its seen>)` when a quantifier decided it (GO08, `fixpoint.witness`)."""
    seen = _compact(found["seen"])
    text = f"{found['clause']} (seen: {seen})" + (f" (witness: {named[0]} {_compact(named[1])})" if named else "")
    return f"{rule['message']} | {text}" if rule.get("message") else text


def _compact(value: Any) -> str:
    return json.dumps(value, sort_keys=True, ensure_ascii=False, separators=(",", ":"))
