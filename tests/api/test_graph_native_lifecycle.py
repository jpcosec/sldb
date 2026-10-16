"""The graph as a state machine (what deskops asked for): states are documents, transitions are
RelationDocs whose condition is a `--where` read on the subject moving through them.

Covers: `where_matches` on a plain payload, loud on an unparseable part; `and` joins
predicates, never inside a literal; `nonempty` rejects [] and {} where `has` does not;
`{field}` fills from the subject; `edges_holding` keeps the transitions whose condition holds,
also from the CLI; a self-loop is a valid terminal transition.
"""

from __future__ import annotations

import json
import sys
from pathlib import Path

import pytest

from sldb import api
from sldb.cli import main as cli_main

MODULE = "sldb_lifecycle_test_models"
MODELS = '''from pydantic import Field
from sldb import StructuredNLDoc


class Ritual(StructuredNLDoc):
    __template__ = "# ⸢rev•title⸥"
    title: str = Field(description="Title.")


class Task(StructuredNLDoc):
    __template__ = "---\\nimpl: ⸢rev•impl⸥\\nvalidation: ⸢rev,list•validation⸥\\n---\\n\\n# ⸢rev•title⸥"
    title: str = Field(description="Title.")
    impl: str = Field(default="", description="Implementation path.")
    validation: list[str] = Field(default_factory=list, description="Checks.")
'''
GATE = "has(impl) and nonempty(validation)"


@pytest.fixture
def desk(tmp_path: Path) -> tuple[Path, str]:
    sys.modules.pop(MODULE, None)
    (tmp_path / f"{MODULE}.py").write_text(MODELS, encoding="utf-8")
    root, py = tmp_path / "desk", str(tmp_path)
    root.mkdir()
    store = api.init_store(root).store_path
    for model in ("Ritual", "Task"):
        api.add_model(store, f"{MODULE}:{model}", py)
    api.init_relations(store, py)

    def create(model: str, name: str, payload: dict) -> None:
        api.create_document(store, model, root / f"{name}.md", payload, name, py)

    for ritual in ("execution", "closeout"):
        create("Ritual", ritual, {"title": ritual})
    for verb, condition in (("hands_to_closeout", GATE), ("completes", "")):
        create("RelationTypeDoc", f"rt-{verb}", {"title": verb, "name": verb, "source_types": ["Ritual"], "target_types": ["Ritual"], "condition": condition, "description": f"{verb}."})
    create("RelationDoc", "e-handoff", {"title": "handoff", "source_id": "Ritual:execution", "target_id": "Ritual:closeout", "relation_type": "hands_to_closeout"})
    create("RelationDoc", "e-complete", {"title": "complete", "source_id": "Ritual:closeout", "target_id": "Ritual:closeout", "relation_type": "completes"})
    create("Task", "task-ready", {"title": "ready", "impl": "src/x.py", "validation": ["pytest"]})
    create("Task", "task-unchecked", {"title": "unchecked", "impl": "src/x.py", "validation": []})
    return store, py


@pytest.mark.parametrize(
    "expression,payload,expected",
    [
        (GATE, {"impl": "a", "validation": ["t"]}, True),
        (GATE, {"impl": "a", "validation": []}, False),
        (GATE, {"impl": "", "validation": ["t"]}, False),
        ("has(v)", {"v": []}, True),
        ("nonempty(v)", {"v": []}, False),
        ("nonempty(v)", {"v": {}}, False),
        ("nonempty(v)", {"v": 0}, True),
        ("nonempty(v)", {}, False),
        ('title = "a and b"', {"title": "a and b"}, True),
        ('"x" in tags and n >= 2', {"tags": ["x"], "n": 2}, True),
        ("", {}, True),
    ],
)
def test_where_matches_a_plain_payload(expression, payload, expected):
    assert api.where_matches(expression, payload) is expected


def test_braces_fill_from_the_subject():
    assert api.where_matches("capacity >= {party_size}", {"capacity": 6}, {"party_size": 6})
    assert not api.where_matches("capacity >= {party_size}", {"capacity": 6}, {"party_size": 8})
    assert not api.where_matches("capacity >= {party_size}", {"capacity": 6}, {})
    assert api.where_matches('owner = {who} and title = "{who}"', {"owner": 'J "P"', "title": "{who}"}, {"who": 'J "P"'})


def test_an_unparseable_part_is_loud():
    with pytest.raises(api.WherePredicateError, match="bogus"):
        api.where_matches("has(a) and bogus", {"a": 1})


def test_edges_holding_keeps_the_transitions_the_subject_may_take(desk):
    store, py = desk
    ready = api.extract_document_payload(store, py, "task-ready")
    unchecked = api.extract_document_payload(store, py, "task-unchecked")
    assert [e.target for e in api.edges_holding(store, "Ritual:execution", ready, "hands_to_closeout")] == ["sldb://document/Ritual:closeout"]
    assert api.edges_holding(store, "Ritual:execution", unchecked, "hands_to_closeout") == []


def test_a_self_loop_is_a_valid_terminal_transition(desk):
    store, _ = desk
    [edge] = api.edges_holding(store, "Ritual:closeout", {}, "completes")
    assert edge.source == edge.target == "sldb://document/Ritual:closeout"
    assert api.check_edges(store).ok


def test_edges_show_holds_for(desk, capsys):
    store, py = desk
    args = ["edges", "show", "Ritual:execution", "--relation", "hands_to_closeout", "--store", str(store), "--pythonpath", py, "--holds-for"]
    assert cli_main(args + ["task-ready"]) == 0
    assert [e["relation"] for e in json.loads(capsys.readouterr().out)] == ["hands_to_closeout"]
    assert cli_main(args + ["Task/task-unchecked"]) == 0
    assert json.loads(capsys.readouterr().out) == []
