"""The rules read a linked store only when they may (`rule_reach`, task rule_graph sin federación).

The world store links `other` (both register Base, X < Base); a rule whose path crosses into the
linked store still sees the linked document, and a store whose rules stay local is evaluated
over its own index without composing the federation.
"""

from __future__ import annotations

import sys
from pathlib import Path

import pytest

from sldb import api
from sldb.api.rules.rule_graph import rule_graph

MODULE = "sldb_rule_reach_models"
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
'''
CROSSING = {"title": "deps", "subject": "model <= X", "condition": 'all(depends_on: status = "closed")', "severity": "error", "moment": "on_check"}
LOCAL = {"title": "closed", "subject": "model <= X", "condition": 'status = "closed"', "severity": "error", "moment": "on_check"}


class Federation:
    def __init__(self, base: Path) -> None:
        self.py = str(base)
        self.other = self._store(base / "other")
        self.store = self._store(base / "world")
        api.add_model(self.store, "sldb.models.rule_doc:RuleDoc", self.py)
        api.link_store(self.store, self.other, "other")
        self.doc(self.other, "X", "o1", {"title": "o1", "status": "open"})
        self.doc(self.store, "X", "x1", {"title": "x1", "status": "closed", "depends_on": "other:X:o1"})

    def _store(self, root: Path) -> Path:
        root.mkdir()
        store = api.init_store(root).store_path
        for model in ("Base", "X"):
            api.add_model(store, f"{MODULE}:{model}", self.py)
        return store

    def doc(self, store: Path, model: str, name: str, payload: dict) -> None:
        api.create_document(store, model, store.parent / f"{name}.md", payload, name, self.py)

    def rule(self, fields: dict) -> None:
        api.create_document(self.store, "RuleDoc", self.store.parent / "rules" / f"{fields['title']}.md", fields, fields["title"], self.py)


@pytest.fixture
def federation(tmp_path: Path):
    (tmp_path / f"{MODULE}.py").write_text(MODELS, encoding="utf-8")
    sys.path.insert(0, str(tmp_path))
    try:
        yield Federation(tmp_path)
    finally:
        sys.path.remove(str(tmp_path))
        sys.modules.pop(MODULE, None)


def _codes(findings) -> list[tuple[str, str, str]]:
    return [(f.level, f.code, f.subject) for f in findings]


def test_a_rule_whose_path_crosses_into_a_linked_store_still_sees_the_linked_document(federation: Federation) -> None:
    federation.rule(CROSSING)
    assert rule_graph(federation.store, None).linked
    found = api.rules_check(federation.store, pythonpath=federation.py)
    assert _codes(found) == [("error", "rules/deps", "X:x1")]
    assert "other:X:o1" in found[0].what
    explained = api.rules_explain(federation.store, "deps", "X:x1", federation.py)
    assert explained["finding"]["holds"] == "false"


def test_local_rules_read_the_store_alone_with_the_same_findings(federation: Federation) -> None:
    federation.rule(LOCAL)
    federation.doc(federation.store, "X", "x2", {"title": "x2", "status": "open"})
    graph = rule_graph(federation.store, None)
    assert not graph.linked
    assert all(":" not in node.split(":", 1)[1] for node in graph.index_documents)
    assert _codes(api.rules_check(federation.store, pythonpath=federation.py)) == [("error", "rules/closed", "X:x2")]
    assert rule_graph(federation.store).linked


def test_a_subject_in_the_linked_store_is_read_from_the_composed_index(federation: Federation) -> None:
    federation.rule(LOCAL)
    explained = api.rules_explain(federation.store, "closed", "other:X:o1", federation.py)
    assert explained["subject"] == "other:X:o1"
    assert explained["finding"]["holds"] == "false"
    assert _codes(api.rules_check(federation.store, "other:X:o1", federation.py)) == [("error", "rules/closed", "other:X:o1")]


def test_an_anchor_to_a_local_document_is_not_a_linked_one() -> None:
    from sldb.api.rules.rule_reach import qualified

    assert not qualified("doc:X:x1") and not qualified("X:x1") and not qualified("x1")
    assert qualified("other:X:o1") and qualified("doc:other:X:o1@sha256:" + "0" * 64)
