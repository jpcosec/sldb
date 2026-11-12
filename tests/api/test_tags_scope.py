"""GD27 for deskops (CC35d H1-H3): `anchored_by.value: bare` and `tag_models` (docs/architecture/tags.md).

With `value: bare` the anchor's field holds the tag's value without its namespace (deskops'
`CrossroadDoc.path` is `a.b`, the tag `domain:a.b`); a field already carrying `domain:` anchors
nothing. With `tag_models` the family `builtin:tag_namespace` checks only the documents of those
models or of their descendants; the anchors are never filtered. Without either, nothing changes
(`tests/api/test_tags.py`).
"""

from __future__ import annotations

import sys
from pathlib import Path

import pytest
from pydantic import ValidationError

from sldb import api
from sldb.api.stores.declare_store import declare_store
from sldb.api.stores.store_declaration import StoreDeclaration, load_declaration, save_declaration
from sldb.core.exceptions import SLDBRuleViolationError

MODULE = "sldb_gd27b_scope_models"
MODELS = '''from pydantic import Field
from sldb import StructuredNLDoc


class CrossroadDoc(StructuredNLDoc):
    __template__ = "---\\npath: ⸢rev•path⸥\\n---\\n\\n# ⸢rev•title⸥"
    title: str = Field(description="Title.")
    path: str = Field(description="The domain value, without namespace.")


class AtomDoc(StructuredNLDoc):
    __template__ = "---\\ntags: ⸢rev•tags⸥\\n---\\n\\n# ⸢rev•title⸥"
    title: str = Field(description="Title.")
    tags: list[str] = Field(default_factory=list, description="Tags.")


class SubAtomDoc(AtomDoc):
    __template__ = "---\\ntags: ⸢rev•tags⸥\\n---\\n\\n# ⸢rev•title⸥"


class TaskDoc(StructuredNLDoc):
    __template__ = "---\\ntags: ⸢rev•tags⸥\\n---\\n\\n# ⸢rev•title⸥"
    title: str = Field(description="Title.")
    tags: list[str] = Field(default_factory=list, description="Tags.")
'''
DOMAIN = {"name": "domain", "anchored_by": {"model": "CrossroadDoc", "field": "path", "value": "bare"}}


class Desk:
    def __init__(self, base: Path) -> None:
        self.root, self.py = base / "desk", str(base)
        self.root.mkdir()
        self.store = api.init_store(self.root).store_path
        for model in ("CrossroadDoc", "AtomDoc", "SubAtomDoc", "TaskDoc"):
            api.add_model(self.store, f"{MODULE}:{model}", self.py)
        api.init_relations(self.store, self.py)
        save_declaration(self.store, declare_store(self.store, self.root))

    def declare(self, *namespaces: dict, models: list[str] | None = None) -> None:
        declaration = load_declaration(self.store)
        declaration.tag_namespaces = [api.TagNamespace(**namespace) for namespace in namespaces]
        declaration.tag_models = models or []
        save_declaration(self.store, declaration)

    def create(self, model: str, name: str, payload: dict) -> None:
        api.create_document(self.store, model, self.root / model / f"{name}.md", {"title": name, **payload}, name, self.py)


@pytest.fixture
def desk(tmp_path: Path):
    (tmp_path / f"{MODULE}.py").write_text(MODELS, encoding="utf-8")
    sys.path.insert(0, str(tmp_path))
    try:
        yield Desk(tmp_path)
    finally:
        sys.path.remove(str(tmp_path))
        sys.modules.pop(MODULE, None)


# --- g1: anchored_by.value ----------------------------------------------------------------------


def test_value_is_optional_tag_or_bare_and_dumps_as_written() -> None:
    declaration = StoreDeclaration.model_validate({"tag_namespaces": [DOMAIN, {"name": "area", "anchored_by": {"model": "A", "field": "tag"}}]})
    assert [n["anchored_by"] for n in declaration.model_dump()["tag_namespaces"]] == [DOMAIN["anchored_by"], {"model": "A", "field": "tag"}]
    assert api.TagNamespace(**DOMAIN).anchor_tag("a.b") == "domain:a.b"
    assert [api.TagNamespace(**DOMAIN).anchor_tag(v) for v in ("domain:a.b", "", " ", None, ["a"])] == [None] * 5
    assert api.TagNamespace(name="area", anchored_by={"model": "A", "field": "tag", "value": "tag"}).anchor_tag("area:a") == "area:a"


@pytest.mark.parametrize("anchored_by", [{"model": "A", "field": "f", "value": "full"}, {"model": "A", "value": "bare"}, {"model": "A", "field": "f", "other": "x"}, {}])
def test_a_malformed_anchored_by_is_refused(anchored_by: dict) -> None:
    with pytest.raises(ValidationError):
        api.TagNamespace(name="domain", anchored_by=anchored_by)


def test_a_bare_path_anchors_its_tag_the_tree_has_the_root_and_check_is_clean(desk: Desk) -> None:
    """CC35d B1: `CrossroadDoc.path` `a.b` anchors `domain:a` and `domain:a.b`."""
    desk.declare(DOMAIN)
    desk.create("CrossroadDoc", "a", {"path": "a"})
    desk.create("CrossroadDoc", "ab", {"path": "a.b"})
    desk.create("AtomDoc", "atom", {"tags": ["domain:a.b"]})
    assert api.tag_check(desk.store) == []
    assert api.tag_tree(desk.store, "domain") == {"namespace": "domain", "orphans": [], "unplaced": [],
        "roots": [{"tag": "domain:a", "document": "CrossroadDoc:a", "children": [{"tag": "domain:a.b", "document": "CrossroadDoc:ab", "children": []}]}]}


def test_with_bare_a_path_carrying_the_namespace_anchors_nothing(desk: Desk) -> None:
    desk.declare(DOMAIN)
    desk.create("CrossroadDoc", "a", {"path": "domain:a"})
    desk.create("AtomDoc", "atom", {"tags": []})
    with pytest.raises(SLDBRuleViolationError, match='"missing":\\["domain:a"\\]'):
        api.save_document_payload(desk.store, "AtomDoc", "atom", {"title": "atom", "tags": ["domain:a"]}, desk.py)
    assert api.tag_tree(desk.store, "domain")["roots"] == []


# --- g2: tag_models -----------------------------------------------------------------------------


def test_tag_models_checks_only_their_documents_and_descendants(desk: Desk) -> None:
    """CC35d B2: tasks with undeclared `workspace:x` are out of scope; atoms are checked."""
    desk.create("CrossroadDoc", "a", {"path": "a"})
    desk.create("TaskDoc", "t1", {"tags": ["workspace:x", "domain:zz"]})
    desk.create("AtomDoc", "atom", {"tags": ["domain:a", "kind:x"]})
    desk.create("SubAtomDoc", "sub", {"tags": ["pill-type:y"]})
    desk.declare(DOMAIN, models=["AtomDoc"])
    assert [(f.subject, f.code) for f in api.tag_check(desk.store)] == [("AtomDoc:atom", "rules/builtin:tag_namespace:kind"), ("SubAtomDoc:sub", "rules/builtin:tag_namespace:pill-type")]
    assert [f.subject for f in api.rules_check(desk.store)] == ["AtomDoc:atom", "SubAtomDoc:sub"]
    assert [f.subject for f in api.on_check_findings(desk.store, desk.py)] == ["AtomDoc:atom", "SubAtomDoc:sub"]
    api.save_document_payload(desk.store, "TaskDoc", "t1", {"title": "t1", "tags": ["workspace:y"]}, desk.py)
    with pytest.raises(SLDBRuleViolationError):
        api.save_document_payload(desk.store, "AtomDoc", "atom", {"title": "atom", "tags": ["workspace:y"]}, desk.py)


def test_explain_of_a_document_out_of_scope_holds_naming_the_scope(desk: Desk) -> None:
    desk.declare(DOMAIN, models=["AtomDoc"])
    desk.create("TaskDoc", "t1", {"tags": ["workspace:x"]})
    answer = api.rules_explain(desk.store, "builtin:tag_namespace:workspace", "TaskDoc:t1", desk.py)
    assert answer["finding"] == {"node": "TaskDoc:t1", "holds": "true", "clause": "model in tag_models", "seen": {"model": "TaskDoc", "tag_models": ["AtomDoc"]}}


def test_tag_tree_with_tag_models_uses_only_documents_in_scope_and_every_anchor(desk: Desk) -> None:
    desk.create("CrossroadDoc", "a", {"path": "a"})
    desk.create("CrossroadDoc", "b", {"path": "b"})
    desk.create("TaskDoc", "t1", {"tags": ["domain:b", "domain:c"]})
    desk.create("AtomDoc", "atom", {"tags": ["domain:a", "domain:d"]})
    desk.declare(DOMAIN, models=["AtomDoc"])
    tree = api.tag_tree(desk.store, "domain")
    assert [root["tag"] for root in tree["roots"]] == ["domain:a", "domain:b"]
    assert tree["orphans"] == [{"tag": "domain:d", "used_by": ["AtomDoc:atom"]}]
    assert tree["unplaced"] == [{"tag": "domain:b", "document": "CrossroadDoc:b"}]


def test_without_tag_models_the_declaration_dumps_as_before_and_every_document_is_checked(desk: Desk) -> None:
    assert "tag_models" not in StoreDeclaration().model_dump()
    assert StoreDeclaration(tag_models=["AtomDoc"]).model_dump()["tag_models"] == ["AtomDoc"]
    desk.create("TaskDoc", "t1", {"tags": ["workspace:x"]})
    desk.declare(DOMAIN)
    assert [f.subject for f in api.tag_check(desk.store)] == ["TaskDoc:t1"]
