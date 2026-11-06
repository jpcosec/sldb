"""`sldb rules check`: the local rules evaluated, each failure a core `Finding` (GO06).

With a subject, every rule that applies to that document, of any moment; without one, the
`on_check` rules over every local document they apply to. Only `false` and `incomplete` become
findings: `false` at the rule's severity with code `rules/<name>`, `incomplete` always an alert
with code `rules/<name>/incomplete`. Nothing of the result is stored.
"""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from sldb.api.rules.rule_graph import RuleGraph, rule_graph
from sldb.api.rules.rule_subjects import applies, resolve_subject, rules_of
from sldb.core.finding import Finding


def rules_check(store: str | Path | None, subject: str | None = None, pythonpath: str | None = None) -> list[Finding]:
    """The findings of the store's rules (see the module); `subject` is a document reference
    (`Model:name`, `store:Model:name` or a path). An unknown subject is `SLDBDocumentTargetError`."""
    graph = rule_graph(store)
    rules = rules_of(graph)
    if subject is not None:
        node = resolve_subject(graph, subject, pythonpath)
        pairs = [(rule, node) for rule in rules if applies(graph, rule, node) is None]
    else:
        pairs = [(r, n) for r in rules if r.get("moment") == "on_check" for n in graph.domain(r["subject"]) if applies(graph, r, n) is None]
    return [f for f in (rule_finding(graph, rule, node) for rule, node in pairs) if f is not None]


def rule_finding(graph: RuleGraph, rule: dict[str, Any], node: str) -> Finding | None:
    """The finding of `rule` on `node` (None when its condition holds)."""
    found = graph.holds(rule["condition"], node)
    if found["holds"] == "true":
        return None
    incomplete = found["holds"] == "incomplete"
    level = "alert" if incomplete else rule.get("severity", "error")
    code = f"rules/{rule['name']}" + ("/incomplete" if incomplete else "")
    return Finding(level, code, node, explanation(rule, found), "", graph.semantics(node).get("path"))


def explanation(rule: dict[str, Any], found: dict[str, Any]) -> str:
    """`<clause> (seen: <seen as compact JSON>)`, after `<message> | ` when the rule has one."""
    seen = json.dumps(found["seen"], sort_keys=True, ensure_ascii=False, separators=(",", ":"))
    text = f"{found['clause']} (seen: {seen})"
    return f"{rule['message']} | {text}" if rule.get("message") else text
