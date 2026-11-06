"""`ViewDoc` as GD25 types it: `params` as `{name, required, default}` entries, `sections`
as typed `Section`s, and the invariants of one document checked by its validators."""

from __future__ import annotations

import pytest
from pydantic import ValidationError

from sldb.api import ViewDoc
from sldb.models.notation.view_param import ViewParam
from sldb.models.notation.view_section import ViewSection

SECTION = {"key": "cards", "select": {"model": "Item", "where": "owner = {owner}"}}


def _view(**fields) -> ViewDoc:
    return ViewDoc(**{"id": "v", "name": "v", "title": "V", "params": [{"name": "owner"}], "sections": [SECTION], **fields})


def test_params_and_sections_are_typed_and_default_to_empty() -> None:
    view = _view()
    assert view.params == [ViewParam(name="owner")] and view.params[0].model_dump() == {"name": "owner", "required": False, "default": None}
    [section] = view.sections
    assert isinstance(section, ViewSection) and (section.fields, section.edges, section.group_by, section.group_order, section.rules, section.transitions) == (["*"], [], "", [], [], None)
    for empty in (None, {}, []):
        assert ViewDoc(id="p", name="p", title="P", params=empty, sections=empty).params == []
    assert ViewDoc(id="p", name="p", title="P").sections == []


def test_a_section_dumps_as_it_was_declared() -> None:
    declared = {**SECTION, "edges": [{"relation": "depends_on", "direction": "in", "as": "blocked_by"}, {"relation": "rel", "direction": "out"}], "transitions": {"from_field": "stage", "relation": "moves_to"}}
    [section] = _view(sections=[declared]).sections
    assert section.model_dump()["edges"] == [{"relation": "depends_on", "direction": "in", "as": "blocked_by"}, {"relation": "rel", "direction": "out", "as": ""}]
    assert [edge.row_key() for edge in section.edges] == ["blocked_by", "out:rel"]
    assert section.transitions == {"from_field": "stage", "relation": "moves_to"}


@pytest.mark.parametrize("fields, message", [
    ({"name": "projection", "id": "projection"}, "reserved"),
    ({"params": [{"name": "owner"}, {"name": "owner"}]}, "declared more than once"),
    ({"params": [{"name": "not an id"}]}, "must be an identifier"),
    ({"params": [{"name": "owner", "required": True, "default": "x"}]}, "cannot be required and have a default"),
    ({"params": [{"name": "owner", "colour": "red"}]}, "colour"),
    ({"sections": [SECTION, SECTION]}, "section keys declared more than once"),
    ({"sections": [{**SECTION, "key": " "}]}, "needs a key"),
    ({"sections": [{"key": "k", "select": {}}]}, "non-empty selector mapping"),
    ({"sections": [{"key": "k", "select": {"colour": "red"}}]}, "unknown selector keys"),
    ({"sections": [{"key": "k", "select": {"model": " "}}]}, "non-blank string"),
    ({"sections": [{"key": "k", "select": {"include_linked": "yes"}}]}, "include_linked must be a boolean"),
    ({"sections": [{"key": "k", "select": {"model": "Item", "where": "owner = = 1"}}]}, "where"),
    ({"sections": [{"key": "k", "select": {"model": "Item", "where": "owner = {who}"}}]}, "undeclared params"),
    ({"sections": [{"key": "k", "select": {"prefix": "{who}-"}}]}, "undeclared params"),
    ({"sections": [{**SECTION, "edges": [{"relation": "r", "direction": "both"}]}]}, "must be out or in"),
    ({"sections": [{**SECTION, "edges": [{"relation": " ", "direction": "in"}]}]}, "needs a relation"),
    ({"sections": [{**SECTION, "transitions": {"from_field": "stage"}}]}, "exactly"),
    ({"sections": [{**SECTION, "transitions": {"from_field": "", "relation": "r"}}]}, "cannot be blank"),
    ({"sections": [{**SECTION, "rules": ["owned", 3]}]}, "rules must be a list of non-blank strings"),
    ({"sections": [{**SECTION, "extra": 1}]}, "extra"),
])
def test_an_invariant_of_the_document_is_rejected_on_validation(fields: dict, message: str) -> None:
    with pytest.raises(ValidationError, match=message):
        _view(**fields)
