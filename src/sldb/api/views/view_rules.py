"""The findings a section's `rules` add to each row (GD25): the RuleDocs named, evaluated as
`rules check` evaluates them (GO06) on the row's document.

`SharedRules` is the store's rule graph read over one view built once: `GraphBackend.eval`
builds the index's view on every call, which a view of hundreds of rows cannot afford."""

from __future__ import annotations

from typing import Any

from sldb.api.rules.rule_subjects import applies, resolve_rule, rules_of
from sldb.api.rules.rules_check import rule_finding
from sldb.core.exceptions import SLDBDocumentTargetError
from sldb.store.graph.backend.index_view import index_view
from sldb.store.graph.language.predicate_api import node_finding


class SharedRules:
    """A `RuleGraph` whose `holds` and `located` read one view of the index, built once; a node
    the index lacks is answered by the graph itself."""

    def __init__(self, graph: Any) -> None:
        self.graph = graph
        self.view = index_view(graph.index)

    def holds(self, predicate: str, node: str) -> dict[str, Any]:
        item = self.view["node"](node)
        return self.graph.holds(predicate, node) if item is None else node_finding(predicate, self.view, item)

    def located(self, node: str) -> tuple[dict[str, Any], dict[str, Any]]:
        item = self.view["node"](node)
        return self.graph.located(node) if item is None else (self.view, item)

    def semantics(self, node: str) -> dict[str, Any]:
        return self.graph.semantics(node)

    def rules(self) -> list[dict[str, Any]]:
        """Every local rule (`rules_of`), read once."""
        if not hasattr(self, "_rules"):
            self._rules = rules_of(self.graph)
        return self._rules


def named_rules(shared: SharedRules, view: str, section: str, names: list[str]) -> list[dict[str, Any]]:
    """The rules the section names; one the store lacks is an error naming it and the section."""
    found = []
    for name in names:
        try:
            found.append(resolve_rule(shared.graph, name))
        except SLDBDocumentTargetError as exc:
            raise SLDBDocumentTargetError(f"view {view!r}, section {section!r}: unknown RuleDoc {name!r}") from exc
    return found


def row_findings(shared: SharedRules, rules: list[dict[str, Any]], export_id: str) -> list[dict[str, Any]]:
    """The findings (as dicts) of the rules that apply to the row's document and do not hold."""
    found = (rule_finding(shared, rule, export_id) for rule in rules if applies(shared, rule, export_id) is None)
    return [finding.as_dict() for finding in found if finding is not None]
