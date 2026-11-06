"""Composed views (GD25): a `ViewDoc` with `params` and `sections` evaluated by `run_view`.

The store: an `Item` (status, owner, depends_on) with a lifecycle of `Stage` documents joined
by `moves_to` edges, a `RuleDoc` on the owner, and a `Receipt` that records a fact sldb does
not compute (a receipt of an external event) pointing at an item. The tablero view groups the
items by status in a declared order and adds neighbours, findings and transitions per row.
"""

from __future__ import annotations

import json
import statistics
import sys
import time
from pathlib import Path

import pytest

from sldb import api
from sldb.cli import main as cli_main
from sldb.core.exceptions import SLDBDocumentTargetError, SLDBValidationError

MODULE = "sldb_gd25_view_models"
MODELS = '''from pydantic import Field
from sldb import StructuredNLDoc


class Stage(StructuredNLDoc):
    __template__ = "# ⸢rev•title⸥"
    title: str = Field(description="Title.")


class Item(StructuredNLDoc):
    __references__ = ["depends_on"]
    __template__ = "---\\nstatus: ⸢rev•status⸥\\nowner: ⸢optrev•owner⸥\\nstage: ⸢rev•stage⸥\\ndepends_on: ⸢rev,list•depends_on⸥\\n---\\n\\n# ⸢rev•title⸥"
    title: str = Field(description="Title.")
    status: str = Field(description="Column of the tablero.")
    owner: str = Field(default="", description="Who works on it.")
    stage: str = Field(description="The lifecycle node the item is at (`Stage:<name>`).")
    depends_on: list = Field(default_factory=list, description="Items this one waits for.")


class Receipt(StructuredNLDoc):
    __references__ = ["item"]
    __template__ = "---\\nitem: ⸢rev•item⸥\\nkind: ⸢rev•kind⸥\\n---\\n\\n# ⸢rev•title⸥"
    title: str = Field(description="Title.")
    item: str = Field(description="The item the external fact is about.")
    kind: str = Field(description="What kind of fact.")
'''
RULE = {"title": "owned", "subject": "model <= Item", "condition": "nonempty(owner)", "severity": "error", "moment": "on_transition", "message": "needs an owner"}
TABLERO = {
    "id": "tablero", "name": "tablero", "title": "Tablero",
    "params": [{"name": "owner", "default": "ana"}],
    "sections": [
        {"key": "cards", "select": {"model": "Item"}, "fields": ["title", "status", "owner"], "group_by": "status", "group_order": ["open", "review", "done"],
         "edges": [{"relation": "depends_on", "direction": "out", "as": "depends_on"}, {"relation": "depends_on", "direction": "in", "as": "blocked_by"}, {"relation": "item", "direction": "in", "as": "receipts"}],
         "rules": ["owned"], "transitions": {"from_field": "stage", "relation": "moves_to"}},
        {"key": "mine", "select": {"model": "Item", "where": "owner = {owner}"}, "fields": ["title"]},
    ],
}
ITEMS = [("i1", "open", "ana", []), ("i2", "open", "", ["i1"]), ("i3", "review", "bo", ["i1", "i2"]), ("i4", "done", "ana", [])]


class World:
    def __init__(self, base: Path) -> None:
        self.root, self.py = base / "world", str(base)
        self.root.mkdir()
        self.store = api.init_store(self.root).store_path
        for ref in (f"{MODULE}:Stage", f"{MODULE}:Item", f"{MODULE}:Receipt", "sldb.models.rule_doc:RuleDoc", "sldb.models.notation_models:ViewDoc"):
            api.add_model(self.store, ref, self.py)
        api.init_relations(self.store, self.py)
        self._lifecycle()
        for name, status, owner, depends_on in ITEMS:
            self.item(name, status, owner, depends_on)
        self.doc("RuleDoc", "owned", RULE)
        self.doc("Receipt", "r1", {"title": "merged upstream", "item": "Item:i1", "kind": "evidence"})
        self.doc("ViewDoc", "tablero", TABLERO)

    def _lifecycle(self) -> None:
        for stage in ("open", "review", "done"):
            self.doc("Stage", stage, {"title": stage})
        self.doc("RelationTypeDoc", "rt-moves", {"title": "moves", "name": "moves_to", "source_types": ["Stage"], "target_types": ["Stage"], "description": "A transition."})
        self.doc("RelationDoc", "e-review", {"title": "review", "source_id": "Stage:open", "target_id": "Stage:review", "relation_type": "moves_to", "condition": 'status = "open"', "attributes": {"sets": {"status": "review"}}})
        self.doc("RelationDoc", "e-done", {"title": "done", "source_id": "Stage:review", "target_id": "Stage:done", "relation_type": "moves_to", "attributes": {"sets": {"status": "done"}, "terminal": True}})

    def doc(self, model: str, name: str, payload: dict) -> None:
        api.create_document(self.store, model, self.root / model.lower() / f"{name}.md", payload, name, self.py)

    def item(self, name: str, status: str, owner: str, depends_on: list[str]) -> None:
        self.doc("Item", name, {"title": name.upper(), "status": status, "owner": owner, "stage": f"Stage:{status}", "depends_on": [f"Item:{d}" for d in depends_on]})

    def save(self, model: str, name: str, payload: dict) -> None:
        api.save_document_payload(self.store, model, name, payload, self.py)

    def cli(self, capsys, *argv: str) -> dict:
        cli_main(["--envelope", *argv, "--store", str(self.store), "--pythonpath", self.py])
        return json.loads(capsys.readouterr().out)


@pytest.fixture
def world(tmp_path: Path):
    (tmp_path / f"{MODULE}.py").write_text(MODELS, encoding="utf-8")
    sys.path.insert(0, str(tmp_path))
    try:
        yield World(tmp_path)
    finally:
        sys.path.remove(str(tmp_path))
        sys.modules.pop(MODULE, None)


def _cards(result: dict) -> dict[str, dict]:
    return {row["name"]: row for group in result["sections"]["cards"]["groups"] for row in group["rows"]}


def test_the_tablero_groups_the_columns_in_the_declared_order_and_a_column_without_rows_stays(world: World) -> None:
    result = api.run_view(world.store, "tablero")
    assert result["view"] == "tablero" and result["params"] == {"owner": "ana"}
    groups = result["sections"]["cards"]["groups"]
    assert [(g["value"], [r["name"] for r in g["rows"]]) for g in groups] == [("open", ["i1", "i2"]), ("review", ["i3"]), ("done", ["i4"])]
    world.save("Item", "i4", {"title": "I4", "status": "open", "owner": "ana", "stage": "Stage:open", "depends_on": []})
    groups = api.run_view(world.store, "tablero")["sections"]["cards"]["groups"]
    assert [(g["value"], len(g["rows"])) for g in groups] == [("open", 3), ("review", 1), ("done", 0)]


def test_a_row_has_its_fields_and_the_keys_its_section_declares(world: World) -> None:
    row = _cards(api.run_view(world.store, "tablero"))["i3"]
    assert {k: row[k] for k in ("export_id", "model", "name", "path", "fields")} == {"export_id": "Item:i3", "model": "Item", "name": "i3", "path": "item/i3.md", "fields": {"title": "I3", "status": "review", "owner": "bo"}}
    assert sorted(row) == ["blocked", "blocked_by", "depends_on", "export_id", "fields", "findings", "holding", "model", "name", "path", "receipts"]


def test_edges_add_the_incoming_and_outgoing_depends_on_ids(world: World) -> None:
    cards = _cards(api.run_view(world.store, "tablero"))
    assert cards["i3"]["depends_on"] == ["Item:i1", "Item:i2"] and cards["i3"]["blocked_by"] == []
    assert cards["i1"]["depends_on"] == [] and cards["i1"]["blocked_by"] == ["Item:i2", "Item:i3"]


def test_rules_add_the_findings_with_the_clause_that_decided_them(world: World) -> None:
    cards = _cards(api.run_view(world.store, "tablero"))
    assert cards["i1"]["findings"] == []
    [finding] = cards["i2"]["findings"]
    assert (finding["level"], finding["code"], finding["subject"]) == ("error", "rules/owned", "Item:i2")
    assert finding["what"] == 'needs an owner | nonempty(owner) (seen: {"owner":""})'


def test_transitions_give_the_holding_edges_with_effects_and_the_blocked_ones_with_their_finding(world: World) -> None:
    cards = _cards(api.run_view(world.store, "tablero"))
    [edge] = cards["i1"]["holding"]
    assert (edge["source"], edge["target"], edge["effects"], edge["findings"]) == ("sldb://document/Stage:open", "sldb://document/Stage:review", {"sets": {"status": "review"}, "terminal": False}, [])
    assert cards["i1"]["blocked"] == []
    assert cards["i2"]["holding"] == []
    [blocked] = cards["i2"]["blocked"]
    assert blocked["target"] == "sldb://document/Stage:review" and [f["code"] for f in blocked["findings"]] == ["rules/owned"]
    assert cards["i3"]["holding"][0]["effects"] == {"sets": {"status": "done"}, "terminal": True}
    assert cards["i4"]["holding"] == [] and cards["i4"]["blocked"] == []


def test_a_param_filters_and_its_default_applies_when_absent(world: World) -> None:
    names = lambda result: [row["name"] for row in result["sections"]["mine"]["rows"]]
    assert names(api.run_view(world.store, "tablero")) == ["i1", "i4"]
    assert names(api.run_view(world.store, "tablero", {"owner": "bo"})) == ["i3"]
    assert api.run_view(world.store, "tablero", {"owner": "bo"})["params"] == {"owner": "bo"}


def test_a_receipt_of_an_external_fact_reaches_the_item_row_through_edges_without_consumer_code(world: World) -> None:
    cards = _cards(api.run_view(world.store, "tablero"))
    assert cards["i1"]["receipts"] == ["Receipt:r1"] and cards["i2"]["receipts"] == []
    world.doc("Receipt", "r2", {"title": "reviewed", "item": "Item:i2", "kind": "evidence"})
    assert _cards(api.run_view(world.store, "tablero"))["i2"]["receipts"] == ["Receipt:r2"]


def test_the_revision_moves_when_an_item_a_rule_or_a_new_edge_moves_and_not_otherwise(world: World) -> None:
    first = api.run_view(world.store, "tablero")["revision"]
    assert api.run_view(world.store, "tablero")["revision"] == first
    world.save("Item", "i1", {"title": "I1 again", "status": "open", "owner": "ana", "stage": "Stage:open", "depends_on": []})
    second = api.run_view(world.store, "tablero")["revision"]
    assert second != first
    world.save("RuleDoc", "owned", {**RULE, "message": "an owner, please"})
    third = api.run_view(world.store, "tablero")["revision"]
    assert third not in (first, second)
    world.doc("Receipt", "r2", {"title": "reviewed", "item": "Item:i2", "kind": "evidence"})
    assert api.run_view(world.store, "tablero")["revision"] not in (first, second, third)


def test_a_view_doc_whose_selector_does_not_parse_is_refused_on_write(world: World) -> None:
    bad = {**TABLERO, "id": "bad", "name": "bad", "sections": [{"key": "k", "select": {"model": "Item", "where": "owner = = 1"}}]}
    with pytest.raises(Exception, match="where"):
        world.doc("ViewDoc", "bad", bad)
    unknown = {**TABLERO, "id": "bad", "name": "bad", "sections": [{"key": "k", "select": {"colour": "red"}}]}
    with pytest.raises(Exception, match="unknown selector keys"):
        world.doc("ViewDoc", "bad", unknown)
    undeclared = {**TABLERO, "id": "bad", "name": "bad", "sections": [{"key": "k", "select": {"model": "Item", "where": "owner = {who}"}}]}
    with pytest.raises(Exception, match="undeclared params"):
        world.doc("ViewDoc", "bad", undeclared)
    assert not api.doc_exists(world.store, "ViewDoc/bad")


def test_a_view_doc_named_projection_is_refused_on_write(world: World) -> None:
    with pytest.raises(Exception, match="reserved"):
        world.doc("ViewDoc", "projection", {**TABLERO, "id": "projection", "name": "projection"})
    assert not api.doc_exists(world.store, "ViewDoc/projection")


def test_run_view_refuses_a_projection_view_naming_it_and_an_unknown_view(world: World) -> None:
    world.doc("ViewDoc", "graph", {"id": "graph", "name": "graph", "title": "Graph", "nodes": [{"model": "Item"}]})
    with pytest.raises(SLDBValidationError, match="'graph' is a projection view"):
        api.run_view(world.store, "graph")
    with pytest.raises(SLDBDocumentTargetError, match="Unknown view: nope"):
        api.run_view(world.store, "nope")
    assert [v["name"] for v in api.list_views(world.store)] == ["tablero"]


def test_a_rule_the_store_lacks_is_an_error_naming_it_when_the_view_runs(world: World) -> None:
    orphan = {**TABLERO, "id": "orphan", "name": "orphan", "sections": [{"key": "k", "select": {"model": "Item"}, "rules": ["nope"]}]}
    world.doc("ViewDoc", "orphan", orphan)
    with pytest.raises(SLDBDocumentTargetError, match="view 'orphan', section 'k': unknown RuleDoc 'nope'"):
        api.run_view(world.store, "orphan")


def test_params_are_checked_against_the_declaration(world: World) -> None:
    strict = {**TABLERO, "id": "strict", "name": "strict", "params": [{"name": "owner", "required": True}], "sections": [TABLERO["sections"][1]]}
    world.doc("ViewDoc", "strict", strict)
    with pytest.raises(SLDBValidationError, match=r"requires params \['owner'\]"):
        api.run_view(world.store, "strict")
    with pytest.raises(SLDBValidationError, match=r"declares no params \['who'\]"):
        api.run_view(world.store, "strict", {"owner": "ana", "who": "x"})
    with pytest.raises(SLDBValidationError, match="must be strings"):
        api.run_view(world.store, "strict", {"owner": 3})
    with pytest.raises(SLDBValidationError, match="double quote"):
        api.run_view(world.store, "strict", {"owner": 'a"b'})
    assert [r["name"] for r in api.run_view(world.store, "strict", {"owner": "bo"})["sections"]["mine"]["rows"]] == ["i3"]


def test_list_views_describes_the_composed_views_only(world: World) -> None:
    world.doc("ViewDoc", "graph", {"id": "graph", "name": "graph", "title": "Graph", "nodes": [{"model": "Item"}]})
    assert api.list_views(world.store) == [{"name": "tablero", "title": "Tablero", "params": [{"name": "owner", "required": False, "default": "ana"}], "sections": ["cards", "mine"]}]
    assert [v["ref"] for v in api.list_projection_views(world.store, world.py)] == ["ViewDoc:graph", "ViewDoc:tablero"]


def test_the_cli_runs_and_lists_views_with_the_envelope(world: World, capsys) -> None:
    run = world.cli(capsys, "views", "run", "tablero", "--param", "owner=bo", "--format", "json")
    assert run["ok"] is True and run["command"] == "views run"
    assert run["data"] == api.run_view(world.store, "tablero", {"owner": "bo"})
    listed = world.cli(capsys, "views", "list", "--format", "json")
    assert listed["ok"] is True and listed["data"] == {"views": api.list_views(world.store)}
    missing = world.cli(capsys, "views", "run", "nope", "--format", "json")
    assert (missing["ok"], missing["error"]["type"], missing["exit"]) == (False, "docs/missing", 1)
    undeclared = world.cli(capsys, "views", "run", "tablero", "--param", "who=x", "--format", "json")
    assert (undeclared["error"]["type"], undeclared["exit"]) == ("validate/rejected", 3)
    repeated = world.cli(capsys, "views", "run", "tablero", "--param", "owner=a", "--param", "owner=b")
    assert (repeated["error"]["type"], repeated["exit"]) == ("cli/usage", 6)
    malformed = world.cli(capsys, "views", "run", "tablero", "--param", "owner")
    assert malformed["error"]["type"] == "cli/usage"


def test_the_cli_prints_a_text_tablero(world: World, capsys) -> None:
    assert cli_main(["views", "run", "tablero", "--store", str(world.store), "--pythonpath", world.py]) == 0
    out = capsys.readouterr().out
    assert "cards" in out and "open" in out and "Item:i1" in out
    assert cli_main(["views", "list", "--store", str(world.store), "--pythonpath", world.py]) == 0
    assert "tablero" in capsys.readouterr().out


def test_the_tablero_over_two_hundred_items_runs_warm_under_a_second(world: World) -> None:
    for n in range(5, 205):
        world.item(f"i{n}", ("open", "review", "done")[n % 3], ("ana", "bo", "")[n % 3], [f"i{n - 1}"])
    api.run_view(world.store, "tablero")
    timings = []
    for _ in range(5):
        start = time.perf_counter()
        result = api.run_view(world.store, "tablero")
        timings.append(time.perf_counter() - start)
    assert sum(len(g["rows"]) for g in result["sections"]["cards"]["groups"]) == 204
    print(f"\nq12 tablero over 204 items, warm, median of 5: {statistics.median(timings):.3f} s (runs: {[round(t, 3) for t in timings]})")
    assert statistics.median(timings) < 1.0
