"""GD27: `sldb.api.replace_text` and `sldb docs replace` (docs/architecture/transactions.md).

Exactly `count` literal occurrences, else nothing is written; a tracked document is validated
under its model and its `on_write` rules, rewritten and tracked again with the same model and
name; a plain file under the root is rewritten in the transaction; a path outside it is refused.
"""

from __future__ import annotations

import hashlib
import json
import sys
from pathlib import Path

import pytest

from sldb import api
from sldb.api.stores.declare_store import declare_store
from sldb.api.stores.store_declaration import load_declaration, save_declaration
from sldb.cli import main
from sldb.core.exceptions import SLDBDocumentTargetError, SLDBRuleViolationError, SLDBStoreError, SLDBValidationError

MODULE = "sldb_gd27_replace_models"
MODELS = '''from pydantic import Field, model_validator
from sldb import StructuredNLDoc


class Note(StructuredNLDoc):
    __template__ = "---\\ntags: ⸢rev•tags⸥\\n---\\n\\n# ⸢rev•title⸥\\n\\n⸢rev•body⸥"
    title: str = Field(description="Title.")
    tags: list[str] = Field(default_factory=list, description="Tags.")
    body: str = Field(default="", description="Body.")

    @model_validator(mode="after")
    def _no_forbidden_body(self):
        if "FORBIDDEN" in self.body:
            raise ValueError("the body must not say FORBIDDEN")
        return self
'''


class World:
    def __init__(self, base: Path) -> None:
        self.root, self.py = base / "world", str(base)
        self.root.mkdir()
        self.store = api.init_store(self.root).store_path
        api.add_model(self.store, f"{MODULE}:Note", self.py)
        api.init_relations(self.store, self.py)
        api.create_document(self.store, "Note", self.root / "docs" / "n1.md", {"title": "n1", "tags": ["kind:x"], "body": "alpha beta alpha"}, "n1", self.py)
        (self.root / "notes.txt").write_bytes(b"foo\r\nfoo bar\n")

    def digest(self, relative: str) -> str:
        return hashlib.sha256((self.root / relative).read_bytes()).hexdigest()

    def payload(self) -> dict:
        return api.edge_node(self.store, "Note:n1").payload

    def replace(self, ref: str, old: str, new: str, **kwargs) -> dict:
        return api.replace_text(self.store, ref, old, new, pythonpath=self.py, **kwargs)

    def cli(self, capsys, *argv: str) -> tuple[int, dict]:
        code = main(["--envelope", "docs", "replace", *argv, "--store", str(self.store), "--pythonpath", self.py, "--format", "json"])
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


def test_two_occurrences_with_count_one_fail_and_nothing_is_written(world: World) -> None:
    before, entry = world.digest("docs/n1.md"), api.edge_node(world.store, "Note:n1").source_hash
    with pytest.raises(SLDBValidationError, match="'alpha' occurs 2 time\\(s\\), not 1; nothing written") as refused:
        world.replace("n1", "alpha", "omega")
    assert refused.value.details == {"seen": 2, "expected": 1}
    assert world.digest("docs/n1.md") == before and api.edge_node(world.store, "Note:n1").source_hash == entry


def test_one_occurrence_is_rewritten_and_the_document_is_tracked_again_with_the_same_model_and_name(world: World) -> None:
    before, text = world.payload(), (world.root / "docs" / "n1.md").read_text(encoding="utf-8")
    result = world.replace("n1", "beta", "gamma")
    assert result == {"ref": "n1", "path": "docs/n1.md", "tracked": True, "model": "Note", "name": "n1", "count": 1}
    assert (world.root / "docs" / "n1.md").read_text(encoding="utf-8") == text.replace("beta", "gamma")
    assert world.payload() == {**before, "body": "alpha gamma alpha"}
    assert api.doc_status(world.store, "n1").model_dump(include={"model", "name", "path"}) == {"model": "Note", "name": "n1", "path": "docs/n1.md"}
    assert api.edge_node(world.store, "Note:n1").source_hash == hashlib.sha256((world.root / "docs" / "n1.md").read_bytes()).hexdigest()


def test_a_replacement_that_breaks_the_model_fails_and_leaves_the_file_and_the_index_as_they_were(world: World) -> None:
    before, payload = world.digest("docs/n1.md"), world.payload()
    with pytest.raises(SLDBValidationError, match="does not validate under Note"):
        world.replace("n1", "beta", "FORBIDDEN")
    with pytest.raises(SLDBValidationError, match="does not (validate|round-trip) under Note"):
        world.replace("n1", "# n1", "n1")
    assert world.digest("docs/n1.md") == before and world.payload() == payload


def test_a_replacement_an_on_write_rule_refuses_fails_with_the_rule_and_writes_nothing(world: World) -> None:
    declaration = declare_store(world.store, world.root)
    declaration.tag_namespaces = [api.TagNamespace(name="kind")]
    save_declaration(world.store, declaration)
    before = world.digest("docs/n1.md")
    with pytest.raises(SLDBRuleViolationError, match="rules/builtin:tag_namespace:otro"):
        world.replace("n1", "kind:x", "otro:x")
    assert world.digest("docs/n1.md") == before
    assert world.replace("n1", "kind:x", "kind:y")["count"] == 1 and world.payload()["tags"] == ["kind:y"]


def test_a_plain_file_under_the_root_is_rewritten_literally_and_counted_without_overlap(world: World) -> None:
    (world.root / "aaa.txt").write_text("aaaa", encoding="utf-8")
    assert world.replace("notes.txt", "foo", "quux", count=2) == {"ref": "notes.txt", "path": "notes.txt", "tracked": False, "model": None, "name": None, "count": 2}
    assert (world.root / "notes.txt").read_bytes() == b"quux\r\nquux bar\n"
    with pytest.raises(SLDBValidationError, match="'aa' occurs 2 time"):
        world.replace("aaa.txt", "aa", "b", count=3)
    assert world.replace("aaa.txt", "aa", "b", count=2)["count"] == 2 and (world.root / "aaa.txt").read_text() == "bb"


@pytest.mark.parametrize("ref, error, text", [
    ("../outside.txt", SLDBStoreError, "outside the project root"),
    ("nowhere.txt", SLDBDocumentTargetError, "Unknown document target: nowhere.txt"),
    ("docs", SLDBDocumentTargetError, "Unknown document target: docs"),
])
def test_a_path_outside_the_root_or_absent_is_refused(world: World, ref: str, error: type, text: str) -> None:
    (world.root.parent / "outside.txt").write_text("x", encoding="utf-8")
    with pytest.raises(error, match=text):
        world.replace(ref, "x", "y")


@pytest.mark.parametrize("old, count", [("", 1), ("x", 0), ("x", -1), ("x", "1")])
def test_an_empty_old_or_a_count_below_one_is_refused(world: World, old: str, count) -> None:
    with pytest.raises(SLDBValidationError, match="replace_text"):
        world.replace("notes.txt", old, "y", count=count)


def test_an_ambiguous_reference_is_refused(world: World) -> None:
    api.create_document(world.store, "Note", world.root / "other" / "n1.md", {"title": "n1", "tags": []}, "n1-other", world.py)
    api.add_model(world.store, "sldb.models.rule_doc:RuleDoc", world.py)
    api.create_document(world.store, "RuleDoc", world.root / "rules" / "n1.md", {"title": "n1", "subject": "model <= Note", "condition": "has(title)", "severity": "alert", "moment": "on_check"}, "n1", world.py)
    with pytest.raises(SLDBDocumentTargetError, match="Ambiguous document target: n1"):
        world.replace("n1", "alpha", "omega")


def test_replace_text_joins_the_transaction_it_receives_and_the_outermost_one_rolls_back(world: World) -> None:
    before = world.digest("docs/n1.md"), world.digest("notes.txt"), world.payload()
    with pytest.raises(RuntimeError, match="later"):
        with api.transaction(world.store, world.py) as tx:
            world.replace("n1", "beta", "gamma", transaction=tx)
            world.replace("notes.txt", "foo", "quux", count=2, transaction=tx)
            assert world.payload()["body"] == "alpha gamma alpha" and (world.root / "notes.txt").read_bytes() == b"quux\r\nquux bar\n"
            raise RuntimeError("later")
    assert (world.digest("docs/n1.md"), world.digest("notes.txt"), world.payload()) == before
    with api.transaction(world.store, world.py) as tx:
        world.replace("n1", "beta", "gamma", transaction=tx)
    assert world.payload()["body"] == "alpha gamma alpha"


def test_a_failed_replace_inside_a_transaction_undoes_the_earlier_writes(world: World) -> None:
    before = world.digest("notes.txt")
    with pytest.raises(SLDBValidationError):
        with api.transaction(world.store, world.py) as tx:
            tx.write_file("notes.txt", b"rewritten")
            world.replace("n1", "alpha", "omega", transaction=tx)
    assert world.digest("notes.txt") == before


def test_the_cli_answers_with_an_envelope_and_typed_errors(world: World, capsys) -> None:
    code, envelope = world.cli(capsys, "n1", "--old", "beta", "--new", "gamma")
    assert (code, envelope["ok"], envelope["data"]) == (0, True, {"ref": "n1", "path": "docs/n1.md", "tracked": True, "model": "Note", "name": "n1", "count": 1})
    code, envelope = world.cli(capsys, "n1", "--old", "alpha", "--new", "omega")
    assert (code, envelope["error"]["type"]) == (3, "validate/rejected") and "occurs 2 time(s), not 1" in envelope["error"]["message"]
    code, envelope = world.cli(capsys, "notes.txt", "--old", "foo", "--new", "bar", "--count", "2")
    assert (code, envelope["data"]["tracked"], envelope["data"]["count"]) == (0, False, 2)
    assert main(["docs", "replace", "notes.txt", "--old", "bar", "--new", "baz", "--count", "3", "--store", str(world.store)]) == 0
    assert capsys.readouterr().out.strip() == "replaced 3 occurrence(s) in notes.txt (notes.txt)"
