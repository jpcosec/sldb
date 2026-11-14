"""GD27: tag namespaces declared in `store.yaml` (docs/architecture/tags.md).

A store that declares `tag_namespaces` refuses, on write, a tag of an undeclared namespace and a
hierarchical tag without an anchor for each of its prefixes (the full value included); the
family `builtin:tag_namespace:<name>` reports its findings where the RuleDocs do (`rules check`,
`rules explain`, `stores check`) and through `sldb tags check`; `tag_tree` nests a namespace;
`tag_folder` is pure. A store without the key behaves as before.
"""

from __future__ import annotations

import hashlib
import json
import sys
from pathlib import Path

import pytest
from pydantic import ValidationError

from sldb import api
from sldb.api.rules import explain_exit
from sldb.api.stores.declare_store import declare_store
from sldb.api.stores.store_declaration import StoreDeclaration, load_declaration, save_declaration
from sldb.cli import main
from sldb.core.exceptions import SLDBDocumentTargetError, SLDBRuleViolationError, SLDBStoreError

MODULE = "sldb_gd27_tag_models"
MODELS = '''from pydantic import Field
from sldb import StructuredNLDoc


class Anchor(StructuredNLDoc):
    __template__ = "---\\ntag: ⸢rev•tag⸥\\n---\\n\\n# ⸢rev•title⸥"
    title: str = Field(description="Title.")
    tag: str = Field(description="The tag this document anchors.")


class Note(StructuredNLDoc):
    __template__ = "---\\ntags: ⸢rev•tags⸥\\n---\\n\\n# ⸢rev•title⸥"
    title: str = Field(description="Title.")
    tags: list[str] = Field(default_factory=list, description="Tags.")
'''
AREA = {"name": "area", "hierarchical": True, "anchored_by": {"model": "Anchor", "field": "tag"}}
FLAT = {"name": "flat", "hierarchical": False, "folder_axis": True, "anchored_by": {"model": "Anchor", "field": "tag"}}
FREE = {"name": "free", "hierarchical": True}


class World:
    def __init__(self, base: Path) -> None:
        self.root, self.py = base / "world", str(base)
        self.root.mkdir()
        self.store = api.init_store(self.root).store_path
        for model in ("Anchor", "Note"):
            api.add_model(self.store, f"{MODULE}:{model}", self.py)
        api.init_relations(self.store, self.py)
        self.note("n1", ["plain"])
        save_declaration(self.store, declare_store(self.store, self.root))

    def declare(self, *namespaces: dict) -> None:
        declaration = load_declaration(self.store)
        declaration.tag_namespaces = [api.TagNamespace(**namespace) for namespace in namespaces]
        save_declaration(self.store, declaration)

    def note(self, name: str, tags: list[str]) -> None:
        api.create_document(self.store, "Note", self.root / f"{name}.md", {"title": name, "tags": tags}, name, self.py)

    def orphan(self, name: str, tags: list[str]) -> None:
        """A note whose tags break the family, created while no namespace is declared: `create_document` evaluates `on_write` (H4), so it cannot enter any other way."""
        declared = load_declaration(self.store)
        self.declare()
        self.note(name, tags)
        save_declaration(self.store, declared)

    def anchor(self, name: str, tag: str) -> None:
        api.create_document(self.store, "Anchor", self.root / "anchors" / f"{name}.md", {"title": name, "tag": tag}, name, self.py)

    def save(self, name: str, tags: list[str]) -> None:
        api.save_document_payload(self.store, "Note", name, {"title": name, "tags": tags}, self.py)

    def digest(self, name: str) -> str:
        return hashlib.sha256((self.root / f"{name}.md").read_bytes()).hexdigest()

    def cli(self, capsys, *argv: str) -> tuple[int, dict]:
        code = main(["--envelope", *argv, "--store", str(self.store), "--pythonpath", self.py, "--format", "json"])
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


@pytest.fixture
def placed(world: World) -> World:
    """The acceptance fixture: `area` declared, anchors `area:a` and `area:a.b`, n1 under `area:a.b`."""
    world.declare(AREA, FLAT, FREE)
    world.anchor("a", "area:a")
    world.anchor("ab", "area:a.b")
    world.save("n1", ["area:a.b"])
    return world


# --- the declaration ---------------------------------------------------------------------------


def test_the_declaration_reads_and_writes_tag_namespaces_and_drops_them_when_empty() -> None:
    declaration = StoreDeclaration.model_validate({"tag_namespaces": [AREA, {"name": "kind", "hierarchical": False}]})
    assert declaration.model_dump()["tag_namespaces"] == [{**AREA, "folder_axis": False}, {"name": "kind", "hierarchical": False, "folder_axis": False}]
    assert "tag_namespaces" not in StoreDeclaration().model_dump()
    assert api.TagNamespace(**AREA).required("area:a.b.c") == ["area:a", "area:a.b", "area:a.b.c"]
    assert api.TagNamespace(**FLAT).required("flat:a.b") == ["flat:a.b"]


@pytest.mark.parametrize("bad", [
    [{"name": "a:b"}], [{"name": " "}], [{"name": "a", "anchored_by": {"model": "X"}}], [{"name": "a", "anchored_by": {"model": "", "field": "f"}}],
    [{"name": "a", "unknown": 1}], [{"name": "a"}, {"name": "a"}],
])
def test_a_malformed_namespace_is_refused(bad: list[dict]) -> None:
    with pytest.raises(ValidationError):
        StoreDeclaration.model_validate({"tag_namespaces": bad})


# --- on_write ----------------------------------------------------------------------------------


def test_a_hierarchical_tag_without_its_anchors_is_refused_naming_each_missing_prefix_top_down(world: World) -> None:
    world.declare(AREA)
    before = world.digest("n1")
    with pytest.raises(SLDBRuleViolationError) as refused:
        world.save("n1", ["area:a.b"])
    assert str(refused.value) == 'rules/builtin:tag_namespace:area: each prefix anchored by Anchor.tag (seen: {"missing":["area:a","area:a.b"],"namespace":"area","tags":["area:a.b"]})'
    assert world.digest("n1") == before
    assert api.edge_node(world.store, "Note:n1").payload["tags"] == ["plain"]


def test_with_the_anchor_of_a_b_alone_the_write_still_names_area_a(world: World) -> None:
    world.declare(AREA)
    world.anchor("ab", "area:a.b")
    with pytest.raises(SLDBRuleViolationError) as refused:
        world.save("n1", ["area:a.b"])
    assert refused.value.findings[0].what.endswith('(seen: {"missing":["area:a"],"namespace":"area","tags":["area:a.b"]})')


def test_with_both_anchors_the_write_passes_and_a_tag_without_namespace_is_not_checked(placed: World) -> None:
    placed.save("n1", ["area:a.b", "plain", "x.y.z"])
    assert api.edge_node(placed.store, "Note:n1").payload["tags"] == ["area:a.b", "plain", "x.y.z"]


def test_a_tag_of_an_undeclared_namespace_is_refused(placed: World) -> None:
    with pytest.raises(SLDBRuleViolationError) as refused:
        placed.save("n1", ["area:a.b", "otro:x"])
    assert str(refused.value) == 'rules/builtin:tag_namespace:otro: namespace declared (seen: {"declared":["area","flat","free"],"namespace":"otro","tags":["otro:x"]})'


def test_the_namespace_is_cut_at_the_first_colon_and_an_unanchored_namespace_only_needs_declaring(placed: World) -> None:
    placed.save("n1", ["free:a.b:c"])
    with pytest.raises(SLDBRuleViolationError) as refused:
        placed.save("n1", ["free:x", "a.b:c:d"])
    assert refused.value.findings[0].code == "rules/builtin:tag_namespace:a.b"


def test_a_non_hierarchical_namespace_needs_an_anchor_for_the_whole_value_only(placed: World) -> None:
    with pytest.raises(SLDBRuleViolationError) as refused:
        placed.save("n1", ["flat:a.b"])
    assert refused.value.findings[0].what.endswith('(seen: {"missing":["flat:a.b"],"namespace":"flat","tags":["flat:a.b"]})')
    placed.anchor("fab", "flat:a.b")
    placed.save("n1", ["flat:a.b"])


def test_an_anchor_document_anchors_the_tag_it_carries_itself(world: World) -> None:
    """The anchor of `area:a` may itself be tagged `area:a` (deskops' crossroads are)."""
    world.declare(AREA)
    world.anchor("a", "area:a")
    api.save_document_payload(world.store, "Anchor", "a", {"title": "a", "tag": "area:a"}, world.py)


def test_a_refused_write_inside_a_transaction_is_rolled_back_with_the_rest(placed: World) -> None:
    before = placed.digest("n1")
    with pytest.raises(SLDBRuleViolationError):
        with api.transaction(placed.store, placed.py) as tx:
            tx.create("Note", "n9", {"title": "n9", "tags": []}, placed.root / "n9.md")
            tx.update("n1", {"title": "n1", "tags": ["otro:x"]})
    assert placed.digest("n1") == before
    assert not (placed.root / "n9.md").exists()
    assert not api.doc_exists(placed.store, "n9")


def test_a_store_without_tag_namespaces_writes_as_before_and_has_no_builtin_rule(world: World) -> None:
    world.save("n1", ["otro:x", "area:a.b"])
    assert api.rules_check(world.store) == [] and api.tag_check(world.store) == [] and api.tag_namespaces(world.store) == []
    assert api.on_check_findings(world.store, world.py) == []
    with pytest.raises(SLDBDocumentTargetError):
        api.rules_explain(world.store, "builtin:tag_namespace:area", "Note:n1", world.py)


# --- check, explain, stores check, tags check ----------------------------------------------------


def test_tags_check_finds_a_document_created_without_its_anchor(placed: World, capsys) -> None:
    """A document that entered before the namespace was declared (`create_document` now runs `on_write`, H4): `tags check`, `rules check`
    and `stores check` report the orphan, with the same finding."""
    placed.orphan("n2", ["area:c"])
    [found] = api.tag_check(placed.store)
    assert found.as_dict() == {"level": "error", "code": "rules/builtin:tag_namespace:area", "subject": "Note:n2", "fix": "", "document": "n2.md",
                               "what": 'each prefix anchored by Anchor.tag (seen: {"missing":["area:c"],"namespace":"area","tags":["area:c"]})'}
    assert api.rules_check(placed.store) == [found] == api.rules_check(placed.store, "Note:n2", placed.py)
    assert [f.code for f in api.on_check_findings(placed.store, placed.py)] == ["rules/builtin:tag_namespace:area"]
    code, envelope = placed.cli(capsys, "tags", "check")
    assert (code, envelope["error"]["type"], envelope["data"]["findings"]) == (1, "tags/failed", [found.as_dict()])
    assert placed.cli(capsys, "rules", "check")[1]["data"] == {"findings": [found.as_dict()]}
    assert main(["tags", "check", "--store", str(placed.store)]) == 1
    assert capsys.readouterr().out.splitlines()[-1] == "tags check: 1 error(es)"


def test_tags_check_gives_the_evaluation_as_data_beside_the_findings(placed: World, capsys) -> None:
    """H6: the evaluation of each document and namespace, held or not, without parsing a finding's text."""
    placed.orphan("n2", ["area:c"])
    code, envelope = placed.cli(capsys, "tags", "check")
    wanted = [{"document": "Note:n1", "namespace": "area", "rule": "builtin:tag_namespace:area", "holds": True, "clause": "each prefix anchored by Anchor.tag", "tags": ["area:a.b"], "missing": []},
              {"document": "Note:n2", "namespace": "area", "rule": "builtin:tag_namespace:area", "holds": False, "clause": "each prefix anchored by Anchor.tag", "tags": ["area:c"], "missing": ["area:c"]}]
    assert (code, envelope["data"]["evaluations"]) == (1, wanted)
    assert api.tag_evaluations(placed.store) == wanted
    assert [e["document"] for e in envelope["data"]["evaluations"] if not e["holds"]] == [f["subject"] for f in envelope["data"]["findings"]]


def test_tag_evaluations_are_empty_without_namespaces(world: World) -> None:
    assert api.tag_evaluations(world.store) == []


def test_tags_check_passes_a_placed_store(placed: World, capsys) -> None:
    code, envelope = placed.cli(capsys, "tags", "check")
    assert (code, envelope["ok"], envelope["data"]["findings"]) == (0, True, [])
    assert main(["tags", "check", "--store", str(placed.store)]) == 0


def test_rules_explain_answers_a_builtin_rule_with_its_eval_finding(placed: World, capsys) -> None:
    placed.orphan("n2", ["area:c"])
    answer = api.rules_explain(placed.store, "builtin:tag_namespace:area", "Note:n2", placed.py)
    assert answer == {"rule": "builtin:tag_namespace:area", "subject": "Note:n2", "finding": {"node": "Note:n2", "holds": "false", "clause": "each prefix anchored by Anchor.tag", "seen": {"namespace": "area", "tags": ["area:c"], "missing": ["area:c"]}}}
    assert explain_exit(answer) == 1
    held = api.rules_explain(placed.store, "builtin:tag_namespace:area", "Note:n1", placed.py)
    assert (held["finding"]["holds"], held["finding"]["seen"]["missing"]) == ("true", [])
    assert api.rules_explain(placed.store, "builtin:tag_namespace:otro", "Note:n1", placed.py)["finding"]["holds"] == "true"
    code, envelope = placed.cli(capsys, "rules", "explain", "builtin:tag_namespace:area", "Note:n2")
    assert (code, envelope["data"]) == (1, answer)


def test_tags_namespaces_lists_the_declaration(placed: World, capsys) -> None:
    assert api.tag_namespaces(placed.store) == [{**AREA, "folder_axis": False}, FLAT, {**FREE, "folder_axis": False}]
    code, envelope = placed.cli(capsys, "tags", "namespaces")
    assert (code, envelope["data"]) == (0, {"namespaces": api.tag_namespaces(placed.store)})


# --- tag_tree and tag_folder -----------------------------------------------------------------------


def test_tag_tree_nests_the_anchors_and_lists_the_orphan_and_the_unplaced(placed: World, capsys) -> None:
    placed.orphan("n2", ["area:c"])
    placed.anchor("ax", "area:a.x")
    tree = api.tag_tree(placed.store, "area")
    assert tree == {"namespace": "area",
                    "roots": [{"tag": "area:a", "document": "Anchor:a", "children": [{"tag": "area:a.b", "document": "Anchor:ab", "children": []}, {"tag": "area:a.x", "document": "Anchor:ax", "children": []}]}],
                    "orphans": [{"tag": "area:c", "used_by": ["Note:n2"]}],
                    "unplaced": [{"tag": "area:a.x", "document": "Anchor:ax"}]}
    code, envelope = placed.cli(capsys, "tags", "tree", "area")
    assert (code, envelope["data"]) == (0, tree)
    assert main(["tags", "tree", "area", "--store", str(placed.store), "--format", "json"]) == 0
    assert json.loads(capsys.readouterr().out) == tree


def test_tag_tree_fills_a_missing_intermediate_prefix_with_a_null_document(world: World) -> None:
    world.declare(AREA)
    world.anchor("abc", "area:a.b.c")
    assert api.tag_tree(world.store, "area")["roots"] == [{"tag": "area:a", "document": None, "children": [{"tag": "area:a.b", "document": None, "children": [{"tag": "area:a.b.c", "document": "Anchor:abc", "children": []}]}]}]


def test_tag_tree_of_a_flat_or_unanchored_namespace_and_of_an_undeclared_one(placed: World) -> None:
    placed.anchor("fab", "flat:a.b")
    placed.save("n1", ["flat:a.b", "free:x.y"])
    assert api.tag_tree(placed.store, "flat") == {"namespace": "flat", "roots": [{"tag": "flat:a.b", "document": "Anchor:fab", "children": []}], "orphans": [], "unplaced": []}
    assert api.tag_tree(placed.store, "free") == {"namespace": "free", "roots": [{"tag": "free:x", "document": None, "children": [{"tag": "free:x.y", "document": None, "children": []}]}], "orphans": [], "unplaced": []}
    with pytest.raises(SLDBStoreError, match="'nope' is not declared"):
        api.tag_tree(placed.store, "nope")


@pytest.mark.parametrize("tag, folder", [("a.b", "a/b"), ("area:a.b", "a/b"), ("a", "a"), ("area:a.b.c", "a/b/c")])
def test_tag_folder_maps_dots_to_segments(tag: str, folder: str) -> None:
    assert api.tag_folder(tag) == folder


@pytest.mark.parametrize("bad", ["", "area:", "a..b", ".a", "a.", "a/b.c"])
def test_tag_folder_refuses_a_value_that_is_not_a_path(bad: str) -> None:
    with pytest.raises(ValueError, match="does not name a folder"):
        api.tag_folder(bad)


def test_sldb_api_reexports_the_semantic_dag_functions() -> None:
    from sldb.api import semantic

    assert (api.add_semantic_parent, api.remove_semantic_parent, api.add_semantic_equivalence, api.semantic_tag) == (semantic.add_semantic_parent, semantic.remove_semantic_parent, semantic.add_semantic_equivalence, semantic.semantic_tag)
