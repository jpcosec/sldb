"""Transitions as edge data (GO09): a RelationDoc's `attributes.sets/terminal` travel with the edge.

Covers: the convention validated on RelationDoc (one rejection per rule, through the existing
write path); `edges_holding` returns each holding edge with `effects` resolved (`{field}` of a
boolean written as true, absent attributes as `{sets: {}, terminal: false}`, extra keys left
out, an unfillable `{field}` makes the edge not hold); `apply_effects` builds the new payload
and rejects an invalid one; `effects` never shows in a dump while unset.
"""

from __future__ import annotations

import sys
from pathlib import Path

import pytest
from pydantic import ValidationError

from sldb import api

MODULE = "sldb_edge_effects_test_models"
MODELS = '''from pydantic import Field
from sldb import StructuredNLDoc


class State(StructuredNLDoc):
    __template__ = "# ⸢rev•title⸥"
    title: str = Field(description="Title.")


class Item(StructuredNLDoc):
    __template__ = "---\\nstatus: ⸢rev•status⸥\\ndone: ⸢rev•done⸥\\nclosed: ⸢rev•closed⸥\\n---\\n\\n# ⸢rev•title⸥"
    title: str = Field(description="Title.")
    status: str = Field(description="Where the item is.")
    done: bool = Field(default=False, description="Whether the work is done.")
    closed: str = Field(default="", description="Closing mark.")
'''
SUBMIT = {"sets": {"status": "review", "closed": "{done}"}, "terminal": False}
CLOSE = {"sets": {"status": "closed"}, "terminal": True, "owner": "ops"}


@pytest.fixture
def machine(tmp_path: Path):
    sys.modules.pop(MODULE, None)
    (tmp_path / f"{MODULE}.py").write_text(MODELS, encoding="utf-8")
    root, py = tmp_path / "desk", str(tmp_path)
    root.mkdir()
    store = api.init_store(root).store_path
    for model in ("State", "Item"):
        api.add_model(store, f"{MODULE}:{model}", py)
    api.init_relations(store, py)

    def create(model: str, name: str, payload: dict) -> None:
        api.create_document(store, model, root / f"{name}.md", payload, name, py)

    for state in ("open", "review", "closed"):
        create("State", state, {"title": state})
    create("RelationTypeDoc", "rt-moves", {"title": "moves", "name": "moves_to", "source_types": ["State"], "target_types": ["State"], "description": "A transition."})
    for name, source, target, condition, attributes in (
        ("e-submit", "open", "review", 'status = "open"', SUBMIT),
        ("e-abandon", "open", "closed", 'status = "abandoned"', None),
        ("e-close", "review", "closed", "nonempty(status)", CLOSE),
    ):
        payload = {"title": name, "source_id": f"State:{source}", "target_id": f"State:{target}", "relation_type": "moves_to", "condition": condition}
        create("RelationDoc", name, payload | ({"attributes": attributes} if attributes else {}))
    return store, py, create


def _relation(attributes: object) -> dict:
    return {"title": "bad", "source_id": "State:open", "target_id": "State:review", "relation_type": "moves_to", "attributes": attributes}


def test_the_holding_transition_carries_its_resolved_effects(machine):
    store, _, _ = machine
    [edge] = api.edges_holding(store, "State:open", {"title": "i", "status": "open", "done": True}, "moves_to")
    assert edge.target == "sldb://document/State:review"
    assert edge.effects == {"sets": {"status": "review", "closed": "true"}, "terminal": False}


def test_an_edge_without_attributes_has_empty_effects(machine):
    store, _, _ = machine
    [edge] = api.edges_holding(store, "State:open", {"status": "abandoned", "done": False}, "moves_to")
    assert edge.target == "sldb://document/State:closed"
    assert edge.effects == {"sets": {}, "terminal": False}


def test_an_extra_attribute_stays_out_of_effects(machine):
    store, _, _ = machine
    [edge] = api.edges_holding(store, "State:review", {"status": "review"}, "moves_to")
    assert edge.effects == {"sets": {"status": "closed"}, "terminal": True}
    assert edge.metadata["attributes"]["owner"] == "ops"


@pytest.mark.parametrize("done", [None, {"a": 1}, "absent"])
def test_an_unfillable_field_makes_the_edge_not_hold(machine, done):
    store, _, _ = machine
    subject = {"status": "open"} | ({} if done == "absent" else {"done": done})
    assert api.edges_holding(store, "State:open", subject, "moves_to") == []


def _item(store, py):
    return api.load_registered_model(store, "Item", py).model_type


def test_apply_effects_builds_the_new_payload(machine):
    store, py, _ = machine
    subject = {"title": "i", "status": "open", "done": True, "closed": ""}
    [edge] = api.edges_holding(store, "State:open", subject, "moves_to")
    new = api.apply_effects(subject, edge.effects, _item(store, py))
    assert new == {"title": "i", "status": "review", "done": True, "closed": "true"}
    assert subject["status"] == "open"
    assert api.apply_effects({"title": "i", "status": "open"}, {"sets": {"extra_list": ["a"]}, "terminal": False}, _item(store, py))["extra_list"] == ["a"]


def test_apply_effects_rejects_a_value_invalid_for_the_model(machine):
    store, py, _ = machine
    with pytest.raises(ValidationError, match="done"):
        api.apply_effects({"title": "i", "status": "open"}, {"sets": {"done": "maybe"}, "terminal": False}, _item(store, py))
    with pytest.raises(ValidationError, match="status"):
        api.apply_effects({"title": "i", "status": "open"}, {"sets": {"status": None}, "terminal": False}, _item(store, py))


@pytest.mark.parametrize("value,kind", [({"a": 1}, "a map"), ([["a"]], "a nested list")])
def test_apply_effects_rejects_a_value_that_is_not_scalar(machine, value, kind):
    store, py, _ = machine
    with pytest.raises(ValueError, match=f"attributes.sets.status.*{kind}"):
        api.apply_effects({"title": "i", "status": "open"}, {"sets": {"status": value}}, _item(store, py))


@pytest.mark.parametrize(
    "attributes,reason",
    [
        (["sets"], "valid dictionary"),
        ({"sets": "status=closed"}, "attributes.sets must be a map"),
        ({"terminal": "yes"}, "attributes.terminal must be a boolean"),
        ({"sets": {"status": {"to": "closed"}}}, "attributes.sets.status .*a map"),
        ({"sets": {"tags": [["a"]]}}, "attributes.sets.tags .*a nested list"),
    ],
    ids=["attributes-not-map", "sets-not-map", "terminal-not-bool", "sets-value-map", "sets-value-nested-list"],
)
def test_the_convention_is_rejected_when_writing_the_relation_doc(machine, attributes, reason):
    _, _, create = machine
    with pytest.raises(ValidationError, match=f"(?s)attributes.*{reason}"):
        create("RelationDoc", "e-bad", _relation(attributes))


@pytest.mark.parametrize("attributes", [None, {}, {"sets": None, "terminal": None}, {"sets": {"x": None, "tags": ["a", 1, True, None]}, "terminal": True, "role": {"free": [1]}}])
def test_the_convention_accepts_its_defaults_and_free_keys(attributes):
    from sldb.models.relation_doc import RelationDoc

    assert RelationDoc(**_relation(attributes)).attributes == (attributes or {})


def test_effects_fill_strings_with_yaml_scalars_and_keep_null():
    subject = {"done": False, "n": 3, "x": 1.5, "big": 1e20, "who": 'J "P"'}
    sets = {"a": "{done}", "b": "n={n} x={x}", "c": "{big}", "d": "{who}", "e": None, "f": ["{n}", 2, "{done}"], "g": "{{who}}"}
    effects = api.effects_of({"sets": sets}, subject)
    assert effects == {"sets": {"a": "false", "b": "n=3 x=1.5", "c": "1.0e+20", "d": 'J "P"', "e": None, "f": ["3", 2, "false"], "g": '{J "P"}'}, "terminal": False}
    assert api.effects_of({"sets": {"f": ["ok", "{missing}"]}}, subject) is None


def test_effects_stay_out_of_every_dump_while_unset(machine):
    store, _, _ = machine
    record = api.EdgeRecord(source="a", target="b", relation="r")
    assert "effects" not in record.model_dump() and "effects" not in record.model_dump_json()
    assert all("effects" not in e for e in api.serialize_edge_records(api.edges_from(store, "State:open")))
    [held] = api.edges_holding(store, "State:review", {"status": "review"}, "moves_to")
    assert api.serialize_edge_record(held)["effects"] == {"sets": {"status": "closed"}, "terminal": True}
