"""`sldb.api.run_view(store, name, params)`: a composed ViewDoc evaluated (GD25).

Every section selects its rows (GD23) and adds what it declares: neighbours (`edges`), the
findings of named RuleDocs (`rules`), the holding and blocked edges (`transitions`), grouped
by `group_by` in the order of `group_order`. Nothing comes from code the consumer
registers (DA1): a fact sldb does not derive is a document the view reads like any other.
The result carries a `revision` that moves whenever something it read moves (q16)."""

from __future__ import annotations

from pathlib import Path
from typing import Any

from sldb.api.edges.edge_reading import load_edge_index
from sldb.api.edges.project_graph.store_project_graph import project_graph
from sldb.api.rules.rule_graph import rule_graph
from sldb.api.rules.rules_on_transition import has_rules
from sldb.api.stores.open_store import open_store
from sldb.api.stores.store_declaration import load_declaration
from sldb.api.views.list_views import load_view
from sldb.api.views.view_edges import row_neighbours
from sldb.api.views.view_groups import grouped
from sldb.api.views.view_revision import revision
from sldb.api.views.view_rows import projected, resolve_params, section_rows
from sldb.api.views.view_rules import SharedRules, named_rules, row_findings
from sldb.api.views.view_transitions import row_transitions


def run_view(store: str | Path | None, name: str, params: dict[str, str] | None = None) -> dict[str, Any]:
    """The view `name` evaluated with `params`: `{view, params, revision, sections}`, each
    section `{rows: [...]}` or, with `group_by`, `{groups: [{value, rows}]}`; each row
    `{export_id, model, name, path, fields}` plus the keys its section declares (q17).

    Raises:
        SLDBDocumentTargetError: No such ViewDoc, or a section names a RuleDoc the store lacks.
        SLDBValidationError: The view has no sections (a projection view), a param is not
            declared, required and absent, or not a string.
    """
    reading = ViewReading(open_store(store, mode="readonly").store_path)
    view = load_view(reading.store_path, name, reading.index)
    values = resolve_params(view, dict(params or {}))
    sections = {section.key: run_section(reading, view, section, values) for section in view.sections}
    stamp = revision(reading.store_path, reading.index, reading.rows, f"ViewDoc:{view.name}", reading.rule_ids)
    return {"view": view.name, "params": values, "revision": stamp, "sections": sections}


def run_section(reading: "ViewReading", view: Any, section: Any, values: dict[str, str]) -> dict[str, Any]:
    rows = section_rows(reading.store_path, reading.index, section, values)
    rules = named_rules(reading.rules(), view.name, section.key, section.rules) if section.rules else []
    reading.rule_ids += [rule["id"] for rule in rules]
    for row in rows:
        reading.rows.add(row["export_id"])
        add_row_keys(reading, section, rules, row)
    return {"groups": grouped(rows, section.group_by, section.group_order)} if section.group_by else {"rows": rows}


def add_row_keys(reading: "ViewReading", section: Any, rules: list[dict[str, Any]], row: dict[str, Any]) -> None:
    for edge in section.edges:
        row[edge.row_key()] = row_neighbours(reading.index, reading.project(), row, edge)
    if section.rules:
        row["findings"] = row_findings(reading.rules(), rules, row["export_id"])
    if section.transitions:
        subject = projected(reading.index, row["export_id"])
        row.update(row_transitions(reading.index, reading.transition_rules(), row["export_id"], subject, section.transitions))


class ViewReading:
    """What one evaluation reads, loaded once and shared by every section and row."""

    def __init__(self, store_path: Path) -> None:
        self.store_path = store_path
        self.index = load_edge_index(store_path, include_linked=True)
        self.rows: set[str] = set()
        self.rule_ids: list[str] = []
        self._rules: SharedRules | None = None
        self._transitions: tuple | None = None
        self._project: Any = None

    def rules(self) -> SharedRules:
        if self._rules is None:
            self._rules = SharedRules(rule_graph(self.store_path))
        return self._rules

    def transition_rules(self) -> tuple | None:
        """`(rules, on_transition rules)`, or None in a store without RuleDoc (then no rule
        runs, as in `edges_holding`)."""
        if self._transitions is None and has_rules(self.store_path):
            self._transitions = (self.rules(), [r for r in self.rules().rules() if r.get("moment") == "on_transition"])
        return self._transitions

    def project(self) -> Any:
        """The declared project graph (GD21), or None when `store.yaml` is absent or declares none."""
        if self._project is None and declares_project_graph(self.store_path):
            self._project = project_graph(self.store_path)
        return self._project


def declares_project_graph(store_path: Path) -> bool:
    try:
        return load_declaration(store_path).project_graph is not None
    except FileNotFoundError:
        return False
