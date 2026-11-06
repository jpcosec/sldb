"""GO06: RuleDoc, `sldb rules check` and `sldb rules explain` (docs/architecture/rules.md).

The store has Base, X < Base, Y < X and Z < Base. A malformed RuleDoc is refused when written,
one test per field; the rest is the acceptance of the node.
"""

from __future__ import annotations

import json
import sys
from pathlib import Path

import pytest
from pydantic import ValidationError

from sldb import api
from sldb.cli import main
from sldb.core.exceptions import SLDBDocumentTargetError, SLDBStoreError

MODULE = "sldb_go06_rule_models"
MODELS = '''from pydantic import Field
from sldb import StructuredNLDoc


class Base(StructuredNLDoc):
    __references__ = ["depends_on"]
    __template__ = "---\\nstatus: ⸢rev•status⸥\\ndepends_on: ⸢rev•depends_on⸥\\n---\\n\\n# ⸢rev•title⸥"
    title: str = Field(description="Title.")
    status: str = Field(default="", description="Status.")
    depends_on: str = Field(default="", description="Referenced document.")


class X(Base):
    pass


class Y(X):
    pass


class Z(Base):
    pass
'''
RULE = {"title": "closed", "subject": "model <= X", "condition": 'status = "closed"', "severity": "error", "moment": "on_check"}


class World:
    def __init__(self, base: Path) -> None:
        self.root, self.py = base / "world", str(base)
        self.root.mkdir()
        self.store = api.init_store(self.root).store_path
        for model in ("Base", "X", "Y", "Z"):
            api.add_model(self.store, f"{MODULE}:{model}", self.py)
        api.add_model(self.store, "sldb.models.rule_doc:RuleDoc", self.py)
        api.init_relations(self.store, self.py)
        for model, name in (("X", "x1"), ("Y", "y1"), ("Z", "z1")):
            self.doc(model, name, {"title": name, "status": "open"})

    def doc(self, model: str, name: str, payload: dict) -> None:
        api.create_document(self.store, model, self.root / f"{name}.md", payload, name, self.py)

    def rule(self, name: str, **fields) -> None:
        api.create_document(self.store, "RuleDoc", self.root / "rules" / f"{name}.md", {**RULE, "title": name, **fields}, name, self.py)

    def cli(self, capsys, *argv: str) -> tuple[int, dict]:
        code = main(["--envelope", "rules", *argv, "--store", str(self.store), "--pythonpath", self.py, "--format", "json"])
        return code, json.loads(capsys.readouterr().out)


@pytest.fixture
def world(tmp_path: Path):
    (tmp_path / f"{MODULE}.py").write_text(MODELS, encoding="utf-8")
    sys.path.insert(0, str(tmp_path))
    try:
        yield World(tmp_path)
    finally:
        sys.path.remove(str(tmp_path))
        sys.modules.pop(MODULE, None)


def _check(world: World, subject: str | None = None) -> list[tuple[str, str, str]]:
    return sorted((f.level, f.code, f.subject) for f in api.rules_check(world.store, subject, world.py))


def test_a_rule_about_x_applies_to_x_and_y_and_not_to_z(world: World) -> None:
    world.rule("closed")
    assert _check(world) == [("error", "rules/closed", "X:x1"), ("error", "rules/closed", "Y:y1")]
    assert _check(world, "Z:z1") == []


def test_check_reports_errors_and_alerts_with_clause_and_node_and_fails_only_on_error(world: World, capsys) -> None:
    world.rule("owner", severity="alert", subject="model <= Y", condition="has(depends_on)", message="sin dependencia")
    code, alert_only = world.cli(capsys, "check")
    assert (code, alert_only["ok"], alert_only["warnings"][0]["code"]) == (0, True, "rules/owner")
    world.rule("closed")
    code, envelope = world.cli(capsys, "check", "--subject", "Y:y1")
    found = {f["code"]: f for f in envelope["data"]["findings"]}
    assert (code, envelope["exit"], found["rules/owner"]["level"], found["rules/closed"]["level"]) == (1, 1, "alert", "error")
    assert found["rules/closed"]["subject"] == "Y:y1" and found["rules/closed"]["document"] == "y1.md"
    assert found["rules/closed"]["what"] == 'status = "closed" (seen: {"status":"open"})'
    assert found["rules/owner"]["what"] == "sin dependencia | has(depends_on) (seen: {\"depends_on\":\"\"})"


def test_check_without_subject_runs_only_on_check_rules(world: World) -> None:
    world.rule("later", moment="on_write")
    assert _check(world) == []
    assert _check(world, "X:x1") == [("error", "rules/later", "X:x1")]


def test_subject_accepts_model_name_and_path(world: World) -> None:
    world.rule("closed")
    assert _check(world, "Y:y1") == _check(world, "y1.md") == _check(world, str(world.root / "y1.md")) == [("error", "rules/closed", "Y:y1")]


def test_explain_returns_the_eval_finding_and_exits_by_its_value(world: World, capsys) -> None:
    world.rule("closed")
    world.rule("open", condition='status = "open"')
    world.rule("filtered", where='status = "closed"')
    code, holds = world.cli(capsys, "explain", "RuleDoc:open", "X:x1")
    assert (code, holds["data"]) == (0, {"rule": "RuleDoc:open", "subject": "X:x1", "finding": {"node": "X:x1", "holds": "true", "clause": 'status = "open"', "seen": {"status": "open"}}})
    code, fails = world.cli(capsys, "explain", "closed", "y1.md")
    assert (code, fails["data"]["finding"]["holds"]) == (1, "false")
    code, skipped = world.cli(capsys, "explain", str(world.root / "rules" / "filtered.md"), "X:x1")
    assert (code, skipped["data"]) == (3, {"rule": "RuleDoc:filtered", "subject": "X:x1", "applies": False, "reason": "where", "detail": 'status = "closed"'})
    assert api.rules_explain(world.store, "closed", "Z:z1", world.py)["reason"] == "subject"


def test_an_incomplete_result_is_an_alert_whatever_the_severity(world: World, capsys, monkeypatch) -> None:
    world.doc("X", "x2", {"title": "x2", "depends_on": "Z:z1"})
    api.rebuild_edges(world.store, world.py)
    world.rule("deps", condition='all(depends_on: status = "closed")')
    monkeypatch.setattr("sldb.api.rules.rule_graph.load_edge_index", _unavailable(api.load_edge_index))
    assert _check(world, "X:x2") == [("alert", "rules/deps/incomplete", "X:x2")]
    code, envelope = world.cli(capsys, "explain", "deps", "X:x2")
    assert (code, envelope["data"]["finding"]["holds"]) == (2, "incomplete")


def test_an_unknown_rule_or_subject_is_the_unknown_document_error(world: World, capsys) -> None:
    world.rule("closed")
    with pytest.raises(SLDBDocumentTargetError, match="Unknown document target: nope"):
        api.rules_explain(world.store, "nope", "X:x1", world.py)
    code, envelope = world.cli(capsys, "check", "--subject", "X:nope")
    assert (code, envelope["error"]["type"]) == (1, "docs/missing")


@pytest.mark.parametrize("field, value", [
    ("condition", "has("),
    ("where", 'status = "open" and'),
    ("severity", "warning"),
    ("moment", "nightly"),
    ("subject", 'model <= X or status = "open"'),
])
def test_a_malformed_rule_is_refused_when_written(world: World, field: str, value: str) -> None:
    with pytest.raises(ValidationError) as refused:
        world.rule("bad", **{field: value})
    assert [e["loc"] for e in refused.value.errors()] == [(field,)]
    assert not (world.root / "rules" / "bad.md").exists()


def test_a_rule_about_an_unregistered_model_is_refused_when_written(world: World) -> None:
    with pytest.raises(SLDBStoreError, match="Model 'Missing' not registered."):
        world.rule("bad", subject="model <= Missing")
    assert not (world.root / "rules" / "bad.md").exists()


def _unavailable(load):
    """`load_edge_index` whose `depends_on` edges reach an unavailable linked store (H4)."""

    def marked(index):
        class Index:
            def __getattr__(self, name):
                return getattr(index, name)

            def edges_from(self, export_id, relation=None):
                return [e.model_copy(update={"metadata": {**e.metadata, "unavailable": e.metadata.get("field") == "depends_on"}}) for e in index.edges_from(export_id, relation)]

        return Index()

    return lambda *args, **kwargs: marked(load(*args, **kwargs))
