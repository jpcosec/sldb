"""GO08: the rules evaluated when they are due (docs/architecture/rules.md §9).

`on_write` refuses a write on an error (nothing persisted, the explanation in the envelope) and
lets an alert pass (persisted, in `warnings`); `on_transition` keeps the edges of
`edges_holding` with their alerts and moves an edge an error blocks to `edges_blocked`;
`stores check` reports the `on_check` rules and the document anchors, exit 1 only on an error;
the `on_check` cache recomputes nothing when nothing changed, a whole family when its rule
changes, and gives the same findings without `.sldb_cache`; a closure terminates on a cycle;
`edges check` fails on a condition that does not parse.
"""

from __future__ import annotations

import importlib
import json
import shutil
import sys
from pathlib import Path

import pytest

from sldb import api
from sldb.cli import main
from sldb.core.exceptions import SLDBRuleViolationError
from sldb.store.layout import cache_dir

on_check_module = importlib.import_module("sldb.api.rules.rules_on_check")
MODULE = "sldb_go08_rule_models"
MODELS = '''from pydantic import Field
from sldb import StructuredNLDoc


class X(StructuredNLDoc):
    __references__ = ["depends_on"]
    __template__ = "---\\nstatus: ⸢rev•status⸥\\ndepends_on: ⸢rev•depends_on⸥\\n---\\n\\n# ⸢rev•title⸥"
    title: str = Field(description="Title.")
    status: str = Field(default="", description="Status.")
    depends_on: str = Field(default="", description="Referenced document.")


class Sub(X):
    pass


class State(StructuredNLDoc):
    __template__ = "# ⸢rev•title⸥"
    title: str = Field(description="Title.")
'''
RULE = {"title": "closed", "subject": "model <= X", "condition": 'status = "closed"', "severity": "error", "moment": "on_check"}


class World:
    def __init__(self, base: Path) -> None:
        self.root, self.py = base / "world", str(base)
        self.root.mkdir()
        self.store = api.init_store(self.root).store_path
        for ref in (f"{MODULE}:X", f"{MODULE}:Sub", f"{MODULE}:State", "sldb.models.rule_doc:RuleDoc"):
            api.add_model(self.store, ref, self.py)
        api.init_relations(self.store, self.py)
        for name in ("x1", "x2"):
            self.doc("X", name, {"title": name, "status": "open"})

    def doc(self, model: str, name: str, payload: dict) -> None:
        api.create_document(self.store, model, self.root / f"{name}.md", payload, name, self.py)

    def rule(self, name: str, **fields) -> None:
        api.create_document(self.store, "RuleDoc", self.root / "rules" / f"{name}.md", {**RULE, "title": name, **fields}, name, self.py)

    def save(self, model: str, name: str, payload: dict) -> None:
        api.save_document_payload(self.store, model, name, payload, self.py)

    def envelope(self, capsys, *argv: str, pythonpath: bool = True) -> dict:
        main(["--envelope", *argv, "--store", str(self.store)] + (["--pythonpath", self.py] if pythonpath else []))
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


@pytest.fixture
def recomputed(monkeypatch) -> list[str]:
    """Every recalculation (p8): one call of `recompute` per rule-document pair."""
    calls: list[str] = []
    real = on_check_module.recompute

    def counted(graph, rule, node):
        calls.append(f"{rule['name']}@{node}")
        return real(graph, rule, node)

    monkeypatch.setattr(on_check_module, "recompute", counted)
    return calls


def _codes(findings) -> list[tuple[str, str, str]]:
    return [(f.level, f.code, f.subject) for f in findings]


def test_an_error_rule_refuses_the_write_and_nothing_is_persisted(world: World, capsys) -> None:
    world.rule("closed", moment="on_write")
    before = (world.root / "x1.md").read_text(encoding="utf-8")
    with pytest.raises(SLDBRuleViolationError) as refused:
        world.save("X", "x1", {"title": "x1", "status": "review"})
    assert str(refused.value) == 'rules/closed: status = "closed" (seen: {"status":"review"})'
    assert (world.root / "x1.md").read_text(encoding="utf-8") == before
    assert api.edge_node(world.store, "X:x1").payload["status"] == "open"
    envelope = world.envelope(capsys, "fields", "update", "docs/X/x1/status", "review")
    assert (envelope["ok"], envelope["exit"], envelope["error"]["type"]) == (False, 1, "rules/violation")
    assert 'rules/closed: status = "closed" (seen: {"status":"review"})' in envelope["error"]["message"]
    assert (world.root / "x1.md").read_text(encoding="utf-8") == before


def test_two_error_rules_are_both_in_the_envelope_ordered_by_rule(world: World, capsys) -> None:
    world.rule("b-titled", moment="on_write", condition='title = "other"')
    world.rule("a-closed", moment="on_write")
    envelope = world.envelope(capsys, "fields", "update", "docs/X/x1/status", "review")
    lines = envelope["error"]["message"].splitlines()
    assert [line.split(":", 1)[0] for line in lines] == ["rules/a-closed", "rules/b-titled"]
    assert envelope["error"]["type"] == "rules/violation"


def test_an_alert_rule_lets_the_write_pass_and_reports_it_in_warnings(world: World, capsys) -> None:
    world.rule("closed", moment="on_write", severity="alert")
    envelope = world.envelope(capsys, "fields", "update", "docs/X/x1/status", "review")
    assert (envelope["ok"], [w["code"] for w in envelope["warnings"]]) == (True, ["rules/closed"])
    assert envelope["warnings"][0]["subject"] == "X:x1" and "review" in envelope["warnings"][0]["what"]
    assert api.edge_node(world.store, "X:x1").payload["status"] == "review"


def test_a_document_not_yet_indexed_is_refused_by_a_rule_on_its_base_family(world: World) -> None:
    from sldb.store.layout import edges_shard_path

    world.rule("closed", moment="on_write")
    world.doc("Sub", "s1", {"title": "s1", "status": "closed"})
    edges_shard_path(world.store, "Sub", "s1").unlink()
    assert api.edge_node(world.store, "Sub:s1") is None
    before = (world.root / "s1.md").read_text(encoding="utf-8")
    with pytest.raises(SLDBRuleViolationError, match="rules/closed"):
        world.save("Sub", "s1", {"title": "s1", "status": "open"})
    assert (world.root / "s1.md").read_text(encoding="utf-8") == before


def test_a_store_without_on_write_rules_writes_as_before(world: World) -> None:
    world.rule("closed")
    world.save("X", "x1", {"title": "x1", "status": "review"})
    assert api.edge_node(world.store, "X:x1").payload["status"] == "review"


def _machine(world: World) -> None:
    for state in ("open", "done"):
        world.doc("State", state, {"title": state})
    world.doc("RelationTypeDoc", "rt-moves", {"title": "moves", "name": "moves_to", "source_types": ["State"], "target_types": ["State"], "description": "A transition."})
    payload = {"title": "finish", "source_id": "State:open", "target_id": "State:done", "relation_type": "moves_to", "attributes": {"sets": {"status": "done"}}}
    world.doc("RelationDoc", "e-finish", payload)


def test_edges_holding_carries_the_alerts_and_an_error_moves_the_edge_to_edges_blocked(world: World) -> None:
    _machine(world)
    subject = {"title": "x1", "status": "open"}
    world.rule("titled", moment="on_transition", severity="alert", condition='title = "x9"')
    [edge] = api.edges_holding(world.store, "State:open", subject, "moves_to", document="X:x1")
    assert edge.effects == {"sets": {"status": "done"}, "terminal": False}
    assert _codes(edge.findings) == [("alert", "rules/titled", "X:x1")]
    assert api.edges_blocked(world.store, "State:open", subject, "moves_to", document="X:x1") == []
    world.rule("closed", moment="on_transition")
    assert api.edges_holding(world.store, "State:open", subject, "moves_to", document="X:x1") == []
    [blocked] = api.edges_blocked(world.store, "State:open", subject, "moves_to", document="X:x1")
    assert blocked.target == "sldb://document/State:done" and blocked.effects == edge.effects
    assert _codes(blocked.findings) == [("error", "rules/closed", "X:x1"), ("alert", "rules/titled", "X:x1")]
    assert "findings" not in api.edges_holding(world.store, "State:open", subject, "moves_to")[0].model_dump()


def test_stores_check_reports_on_check_rules_and_doc_anchors_and_fails_only_on_error(world: World, capsys, monkeypatch) -> None:
    from sldb.core.finding import alert

    anchor = alert("anchors/doc_changed", "X:x2", "subject: doc:X:x1 is changed")
    monkeypatch.setattr(on_check_module, "check_doc_anchors", lambda store, pythonpath=None: [anchor])
    world.rule("closed", severity="alert")
    envelope = world.envelope(capsys, "stores", "check", "--format", "json")
    assert (envelope["ok"], sorted(w["code"] for w in envelope["warnings"])) == (True, ["anchors/doc_changed", "rules/closed", "rules/closed"])
    world.rule("titled", condition='title = "x1"')
    envelope = world.envelope(capsys, "stores", "check", "--format", "json")
    assert (envelope["ok"], envelope["exit"]) == (False, 1)
    assert [(e["code"], e["subject"]) for e in envelope["data"]["errors"]] == [("rules/titled", "X:x2")]


def test_a_second_check_recomputes_nothing_and_a_changed_rule_recomputes_its_family(world: World, recomputed: list[str]) -> None:
    world.rule("closed")
    first = _codes(api.rules_on_check(world.store))
    assert first == [("error", "rules/closed", "X:x1"), ("error", "rules/closed", "X:x2")] and len(recomputed) == 2
    recomputed.clear()
    assert _codes(api.rules_on_check(world.store)) == first and recomputed == []
    world.save("RuleDoc", "closed", {**RULE, "condition": 'status = "open"'})
    assert api.rules_on_check(world.store) == [] and sorted(recomputed) == ["closed@X:x1", "closed@X:x2"]


def test_a_write_dirties_the_document_and_its_neighbours_only(world: World, recomputed: list[str]) -> None:
    world.doc("X", "x3", {"title": "x3", "status": "open"})
    world.rule("closed")
    api.rules_on_check(world.store)
    recomputed.clear()
    world.save("X", "x1", {"title": "x1", "status": "closed", "depends_on": "X:x2"})
    dirty = json.loads((cache_dir(world.store) / "rules" / "dirty.json").read_text(encoding="utf-8"))["dirty"]
    assert dirty == ["X:x1"]
    assert _codes(api.rules_on_check(world.store)) == [("error", "rules/closed", "X:x2"), ("error", "rules/closed", "X:x3")]
    assert sorted(recomputed) == ["closed@X:x1", "closed@X:x2"]


def test_without_the_cache_the_findings_are_the_same(world: World, recomputed: list[str]) -> None:
    world.rule("closed")
    first = _codes(api.rules_on_check(world.store))
    shutil.rmtree(cache_dir(world.store) / "rules")
    recomputed.clear()
    assert _codes(api.rules_on_check(world.store)) == first == _codes(api.rules_check(world.store))
    assert len(recomputed) == 2


def test_a_closure_over_a_cycle_terminates_and_names_the_open_document(world: World) -> None:
    for name, target in (("a", "b"), ("b", "c"), ("c", "a")):
        world.doc("X", name, {"title": name, "status": "closed", "depends_on": f"X:{target}"})
    api.rebuild_edges(world.store, world.py)
    world.save("X", "c", {"title": "c", "status": "open", "depends_on": "X:a"})
    world.rule("deps", where='title = "a"', condition='all(depends_on+: status = "closed")')
    [found] = api.rules_on_check(world.store)
    assert (found.code, found.subject) == ("rules/deps", "X:a") and found.what.endswith("(witness: X:c {\"status\":\"open\"})")
    world.save("X", "c", {"title": "c", "status": "closed", "depends_on": "X:a"})
    assert api.rules_on_check(world.store) == []


def test_edges_check_fails_on_a_condition_that_does_not_parse(world: World, capsys) -> None:
    _machine(world)
    assert api.check_edges(world.store).ok
    payload = {"title": "bad", "source_id": "State:done", "target_id": "State:open", "relation_type": "moves_to", "condition": 'status = = "x"'}
    world.doc("RelationDoc", "e-bad", payload)
    [error] = api.check_edges(world.store).errors
    assert "State:done -[moves_to]-> sldb://document/State:open: condition does not parse" in error
    envelope = world.envelope(capsys, "edges", "check", pythonpath=False)
    assert (envelope["ok"], envelope["exit"]) == (False, 1)
