"""`sldb rules explain RULE SUBJECT`: the eval finding of one rule on one document (GO06).

The answer is `{"rule", "subject", "finding"}` with the finding exactly as `GraphBackend.eval`
returns it (node, holds, clause, seen), also when it holds. When the rule does not apply to the
document it is `{"rule", "subject", "applies": false, "reason", "detail"}` and has no finding.
"""

from __future__ import annotations

from pathlib import Path
from typing import Any

from sldb.api.rules.rule_graph import rule_graph
from sldb.api.rules.rule_subjects import applies, resolve_rule, resolve_subject

EXITS = {"true": 0, "false": 1, "incomplete": 2}
NOT_APPLIED_EXIT = 3


def rules_explain(store: str | Path | None, rule: str, subject: str, pythonpath: str | None = None) -> dict[str, Any]:
    """The explanation of `rule` (`RuleDoc:name`, `name` or path) on `subject` (`Model:name`,
    `store:Model:name` or path); an unknown reference is `SLDBDocumentTargetError`."""
    graph = rule_graph(store)
    found, node = resolve_rule(graph, rule), resolve_subject(graph, subject, pythonpath)
    answer = {"rule": found["id"], "subject": node}
    missing = applies(graph, found, node)
    if missing is not None:
        return {**answer, "applies": False, "reason": missing[0], "detail": missing[1]}
    return {**answer, "finding": graph.holds(found["condition"], node)}


def explain_exit(answer: dict[str, Any]) -> int:
    """0 true, 1 false, 2 incomplete, 3 when the rule does not apply; severity never counts."""
    return EXITS[answer["finding"]["holds"]] if "finding" in answer else NOT_APPLIED_EXIT
