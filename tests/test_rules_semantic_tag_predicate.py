"""`model_tag("T")`: the document's model declares tag T or one that descends from T in the
semantic DAG (an equivalent of either counts). Asking the parent matches the children, not the
reverse. A tag the DAG does not know is refused when the RuleDoc is written."""

from __future__ import annotations

import sys
from pathlib import Path

import pytest

from sldb import api
from sldb.core.exceptions import SLDBStoreError
from sldb.store.graph.language.predicate_parser import parse_predicate
from sldb.store.graph.language.predicate_view import graph_view
from sldb.store.graph.language.predicate_api import findings
from sldb.store.exceptions import WherePredicateError

MODULE = "sldb_semantic_tag_models"
MODELS = '''from pydantic import Field
from sldb import StructuredNLDoc


class BaseConcept(StructuredNLDoc):
    __template__ = "# ⸢rev•title⸥"
    title: str = Field(description="Title.")


class Parent(BaseConcept):
    __semantics__ = {"concept": ["base"]}


class Child(BaseConcept):
    __semantics__ = {"concept": ["base", "child"]}


class Twin(BaseConcept):
    __semantics__ = {"other": ["same"]}


class Alien(BaseConcept):
    __semantics__ = {"zzz": ["q"]}
'''


@pytest.fixture
def world(tmp_path: Path):
    (tmp_path / f"{MODULE}.py").write_text(MODELS, encoding="utf-8")
    sys.path.insert(0, str(tmp_path))
    root = tmp_path / "w"
    root.mkdir()
    try:
        store = api.init_store(root).store_path
        for name in ("BaseConcept", "Parent", "Child", "Twin", "Alien"):
            api.add_model(store, f"{MODULE}:{name}", str(tmp_path))
        api.add_model(store, "sldb.models.rule_doc:RuleDoc", str(tmp_path))
        api.init_relations(store, str(tmp_path))
        for model in ("Parent", "Child", "Twin", "Alien"):
            api.create_document(store, model, root / f"{model.lower()}.md", {"title": model}, model.lower(), str(tmp_path))
        api.add_semantic_equivalence(store, "other.same", "concept.base")
        yield store, root, str(tmp_path)
    finally:
        sys.path.remove(str(tmp_path))
        sys.modules.pop(MODULE, None)


def _rule(world, name: str, condition: str):
    store, root, py = world
    payload = {"title": name, "subject": "model <= BaseConcept", "condition": condition, "severity": "error", "moment": "on_check"}
    api.create_document(store, "RuleDoc", root / "rules" / f"{name}.md", payload, name, py)


def _failing(world) -> set[str]:
    return {f.subject.split(":")[-1] for f in api.rules_check(world[0])}


def test_the_parent_tag_matches_its_own_model_its_child_and_an_equivalent_but_not_the_unrelated(world) -> None:
    _rule(world, "asks-parent", 'not model_tag("concept.base")')
    assert _failing(world) == {"parent", "child", "twin"}


def test_a_child_tag_does_not_match_the_parent_model(world) -> None:
    _rule(world, "asks-child", 'not model_tag("concept.base.child")')
    assert _failing(world) == {"child"}


def test_an_unknown_tag_is_refused_when_the_rule_is_written_naming_the_tag(world) -> None:
    with pytest.raises(SLDBStoreError, match="concept.nope"):
        _rule(world, "bad", 'model_tag("concept.nope")')


def test_the_predicate_is_pure_over_a_test_graph() -> None:
    graph = {
        "nodes": {"M:a": {"model": "M", "payload": {}}, "N:b": {"model": "N", "payload": {}}},
        "semantic": {"model_tags": {"M": ["x.y"], "N": ["z"]}, "parents": {"x.y": ["x"]}},
    }
    view = graph_view(graph)
    held = {f["node"]: f["holds"] for f in findings(parse_predicate('model_tag("x")'), view)}
    assert held == {"M:a": "true", "N:b": "false"}


def test_the_argument_must_be_a_quoted_tag() -> None:
    with pytest.raises(WherePredicateError):
        parse_predicate("model_tag(x)")
