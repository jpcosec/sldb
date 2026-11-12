"""`sldb.api.run_view(store, name, params)`: a composed ViewDoc evaluated (GD25).

Every section selects its rows (GD23) and adds what it declares: neighbours (`edges`), the
findings of named RuleDocs (`rules`), the holding and blocked edges (`transitions`), grouped
by `group_by` in the order of `group_order`. Nothing comes from code the consumer
registers (DA1): a fact sldb does not derive is a document the view reads like any other.
The result carries a `revision` that moves whenever something it read moves (q16)."""

from __future__ import annotations

from pathlib import Path
from typing import Any

from sldb.api.stores.open_store import open_store
from sldb.api.views.view_reading import ViewReading
from sldb.api.views.view_rules import named_rules, row_findings
from sldb.api.views.view_edges import row_neighbours
from sldb.api.views.view_links import view_needs_linked
from sldb.api.views.view_groups import grouped
from sldb.api.views.view_revision import revision
from sldb.api.views.view_rows import projected, resolve_params, section_rows
from sldb.api.views.view_transitions import row_transitions


def run_view(store: str | Path | None, name: str, params: dict[str, str] | None = None) -> dict[str, Any]:
    """The view `name` evaluated with `params`: `{view, params, revision, sections}`, each
    section `{rows: [...]}` or, with `group_by`, `{groups: [{value, rows}]}`; each row
    `{export_id, model, name, path, fields}` plus the keys its section declares (q17).

    Raises:
        SLDBDocumentTargetError: No such ViewDoc (local, or in a linked store: then read from
            that store's root and evaluated over this one, H9), several linked ViewDocs share
            the name, or a section names a RuleDoc the store lacks.
        SLDBValidationError: The view has no sections (a projection view), a param is not
            declared, required and absent, or not a string.
    """
    reading = ViewReading(open_store(store, mode="readonly").store_path)
    view, node = reading.view(name)
    values = resolve_params(view, dict(params or {}))
    if view_needs_linked(reading.store_path, view, values, reading.index):
        reading.widen()
    sections = {section.key: run_section(reading, view, section, values) for section in view.sections}
    stamp = revision(reading.store_path, reading.index, reading.rows, node, reading.rule_ids)
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
