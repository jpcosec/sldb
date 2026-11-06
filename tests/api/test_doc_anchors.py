"""GO07: document anchors pinned with the target's contract hash (docs/architecture/anchoring.md §6).

A Review's `subject` (in `__doc_anchors__`) anchors a TaskDoc whose `__contract__` is title and
status; `notes` is outside it. The save pins, the composed index derives `subject__anchor_state`
(never written to a shard), `anchors check` reports what moved as alerts, and the rules
language reads it through `^subject`. A malformed form or model definition is refused.
"""

from __future__ import annotations

import json
import sys
from pathlib import Path

import pytest
from pydantic import Field, ValidationError

from sldb import StructuredNLDoc, api
from sldb.api.rules.rule_graph import rule_graph
from sldb.cli import main
from sldb.core.exceptions import SLDBModelError
from sldb.models.provenance import Provenance
from sldb.models.provenance_block import attach_block, read_block
from sldb.store.edge_index.doc_anchor_states import field_states
from sldb.store.edge_index.node_ids import EDGE_INDEX_VERSION
from sldb.store.graph.language.contract_hash import contract_hash
from sldb.store.layout import edges_shard_path

MODULE = "sldb_go07_doc_anchor_models"
MODELS = '''from pydantic import Field
from sldb import StructuredNLDoc


class TaskDoc(StructuredNLDoc):
    __contract__ = ["title", "status"]
    __template__ = "---\\nstatus: ⸢rev•status⸥\\nnotes: ⸢rev•notes⸥\\n---\\n\\n# ⸢rev•title⸥"
    title: str = Field(description="Title.")
    status: str = Field(default="", description="Status.")
    notes: str = Field(default="", description="Free notes, outside the contract.")


class Review(StructuredNLDoc):
    __doc_anchors__ = ["subject"]
    __template__ = "---\\nsubject: ⸢rev•subject⸥\\nverdict: ⸢rev•verdict⸥\\n---\\n\\n# ⸢rev•title⸥"
    title: str = Field(description="Title.")
    subject: str = Field(default="", description="The reviewed document.")
    verdict: str = Field(default="", description="accepted or rejected.")


class Bundle(StructuredNLDoc):
    __doc_anchors__ = ["subjects"]
    __template__ = "---\\nsubjects: ⸢rev•subjects⸥\\n---\\n\\n# ⸢rev•title⸥"
    title: str = Field(description="Title.")
    subjects: list[str] = Field(default_factory=list, description="Anchored documents.")


class Note(StructuredNLDoc):
    __template__ = "# ⸢rev•title⸥"
    title: str = Field(description="Title.")
'''
ACCEPTED = 'any(^subject: anchor_state = "intact" and verdict = "accepted")'
TASK = {"title": "b", "status": "open", "notes": ""}


class World:
    def __init__(self, base: Path) -> None:
        self.root, self.py = base / "world", str(base)
        self.root.mkdir()
        self.store = api.init_store(self.root).store_path
        for model in ("TaskDoc", "Review", "Bundle", "Note"):
            api.add_model(self.store, f"{MODULE}:{model}", self.py)
        api.create_document(self.store, "TaskDoc", self.root / "b.md", TASK, "b", self.py)

    def create(self, model: str, name: str, payload: dict) -> None:
        api.create_document(self.store, model, self.root / f"{name}.md", payload, name, self.py)

    def save(self, model: str, name: str, payload: dict) -> None:
        api.save_document_payload(self.store, model, name, payload, self.py)

    def payload(self, export_id: str) -> dict:
        return api.edge_node(self.store, export_id).payload

    def b_hash(self) -> str:
        return contract_hash(sys.modules[MODULE].TaskDoc, api.edge_node(self.store, "TaskDoc:b").field_hashes)

    def review(self, name: str = "a", subject: str = "doc:TaskDoc:b", verdict: str = "accepted") -> None:
        payload = {"title": name, "subject": subject, "verdict": verdict}
        self.create("Review", name, payload)
        self.save("Review", name, payload)

    def codes(self) -> list[tuple[str, str, str]]:
        return [(f.level, f.code, f.subject) for f in api.check_doc_anchors(self.store, self.py)]

    def holds(self, predicate: str = ACCEPTED, node: str = "TaskDoc:b") -> str:
        return rule_graph(self.store).holds(predicate, node)["holds"]


@pytest.fixture
def world(tmp_path: Path):
    (tmp_path / f"{MODULE}.py").write_text(MODELS, encoding="utf-8")
    sys.path.insert(0, str(tmp_path))
    try:
        yield World(tmp_path)
    finally:
        sys.path.remove(str(tmp_path))
        sys.modules.pop(MODULE, None)


def test_a_saved_anchor_is_pinned_with_the_target_contract_hash(world: World) -> None:
    world.review()
    assert world.payload("Review:a")["subject"] == f"doc:TaskDoc:b@sha256:{world.b_hash()}"
    assert world.payload("Review:a")["subject__anchor_state"] == "intact"
    assert world.codes() == []


def test_the_anchor_follows_the_target_contract_and_anchors_check_alerts(world: World, capsys) -> None:
    world.review()
    world.save("TaskDoc", "b", {**TASK, "notes": "outside the contract"})
    assert world.payload("Review:a")["subject__anchor_state"] == "intact"
    world.save("TaskDoc", "b", {**TASK, "status": "closed"})
    assert world.payload("Review:a")["subject__anchor_state"] == "changed"
    assert world.codes() == [("alert", "anchors/doc_changed", "Review:a")]
    found = api.check_doc_anchors(world.store, world.py)[0]
    assert found.document == "a.md" and "subject" in found.what and "TaskDoc:b" in found.what and "changed" in found.what and found.fix == ""
    assert main(["--envelope", "anchors", "check", "--store", str(world.store), "--pythonpath", world.py, "--format", "json"]) == 0
    envelope = json.loads(capsys.readouterr().out)
    assert [w["code"] for w in envelope["warnings"]] == ["anchors/doc_changed"]
    api.delete_document(world.store, "b", world.py)
    assert world.payload("Review:a")["subject__anchor_state"] == "lost"
    assert world.codes() == [("alert", "anchors/doc_lost", "Review:a")]


def test_an_anchor_to_a_missing_target_is_saved_without_hash_and_pinned_by_a_later_write(world: World) -> None:
    world.review(subject="doc:TaskDoc:later")
    assert world.payload("Review:a")["subject"] == "doc:TaskDoc:later"
    world.create("TaskDoc", "later", {**TASK, "title": "later"})
    assert world.payload("Review:a")["subject__anchor_state"] == "lost"
    world.save("Review", "a", {"title": "a", "subject": "doc:TaskDoc:later", "verdict": "accepted"})
    assert world.payload("Review:a")["subject"].startswith("doc:TaskDoc:later@sha256:")
    assert world.payload("Review:a")["subject__anchor_state"] == "intact"


def test_the_subject_anchor_is_an_edge_and_the_derived_state_never_reaches_the_shard(world: World) -> None:
    world.review()
    edges = api.edges_from(world.store, "Review:a", "references")
    assert [(e.target, e.metadata["field"]) for e in edges] == [("sldb://document/TaskDoc:b", "subject")]
    shard = edges_shard_path(world.store, "Review", "a").read_text(encoding="utf-8")
    assert "__anchor_state" not in shard and EDGE_INDEX_VERSION == "5"


def test_the_rule_reads_anchor_state_through_the_inverse_subject(world: World) -> None:
    assert world.holds() == "false"
    world.review("r1", verdict="rejected")
    assert world.holds() == "false"
    world.review("r2", verdict="accepted")
    assert world.holds() == "true"
    world.save("TaskDoc", "b", {**TASK, "status": "closed"})
    assert world.holds() == "false"


def test_a_list_field_has_one_state_and_one_edge_per_anchor(world: World) -> None:
    payload = {"title": "set", "subjects": ["doc:TaskDoc:b", "doc:TaskDoc:ghost"]}
    world.create("Bundle", "set", payload)
    world.save("Bundle", "set", payload)
    assert world.payload("Bundle:set")["subjects__anchor_state"] == ["intact", "lost"]
    assert [e.target for e in api.edges_from(world.store, "Bundle:set", "references")] == ["sldb://document/TaskDoc:b"]
    assert world.codes() == [("alert", "anchors/doc_lost", "Bundle:set")]
    assert field_states(["doc:A:x", "", "  "], lambda _: (True, None)) == ["lost", None, None]


def test_a_provenance_from_anchor_is_pinned_and_alerts_when_the_target_contract_moves(world: World) -> None:
    world.create("Note", "c", {"title": "c"})
    path = world.root / "c.md"
    text = path.read_text(encoding="utf-8")
    path.write_text(attach_block(text, {**(read_block(text) or {}), "from": ["code:src/x.py::f", "doc:TaskDoc:b"]}), encoding="utf-8")
    world.save("Note", "c", {"title": "c"})
    assert read_block(path.read_text(encoding="utf-8"))["from"] == ["code:src/x.py::f", f"doc:TaskDoc:b@sha256:{world.b_hash()}"]
    assert world.codes() == []
    world.save("TaskDoc", "b", {**TASK, "status": "closed"})
    assert world.codes() == [("alert", "anchors/provenance_changed", "Note:c")]
    api.delete_document(world.store, "b", world.py)
    assert world.codes() == [("alert", "anchors/provenance_lost", "Note:c")]


def test_a_value_that_is_not_an_anchor_is_refused_when_written(world: World) -> None:
    with pytest.raises(Exception, match="subject.*not a document anchor"):
        world.create("Review", "bad", {"title": "bad", "subject": "TaskDoc:b", "verdict": ""})
    world.review()
    with pytest.raises(Exception, match="subject.*not a document anchor"):
        world.save("Review", "a", {"title": "a", "subject": "see TaskDoc:b", "verdict": ""})


@pytest.mark.parametrize("value", ["TaskDoc:b", "doc:TaskDoc", "doc:TaskDoc:b@sha256:", "doc:TaskDoc:b@sha256:abc", "doc:TaskDoc:b@sha256:" + "g" * 64, "doc:TaskDoc:b@md5:" + "a" * 64])
def test_a_malformed_anchor_form_is_rejected_in_a_field_and_in_from(world: World, value: str) -> None:
    review = sys.modules[MODULE].Review
    with pytest.raises(ValidationError, match="subject"):
        review(title="x", subject=value)
    if value.startswith("doc:"):
        with pytest.raises(ValidationError, match="from"):
            Provenance(from_=[value])


def test_the_accepted_forms_and_from_items_that_are_not_doc_anchors(world: World) -> None:
    review = sys.modules[MODULE].Review
    assert review(title="x", subject="").subject == ""
    assert review(title="x", subject="doc:TaskDoc:b@sha256:" + "a" * 64).subject.endswith("a" * 64)
    assert Provenance(from_=["code:src/x.py::f", "whatever"]).from_ == ["code:src/x.py::f", "whatever"]


@pytest.mark.parametrize(
    ("body", "reason"),
    [
        ('__doc_anchors__ = ["count"]\n    count: int = Field(default=0, description="A number.")', "count"),
        ('__doc_anchors__ = ["ghost"]\n    title: str = Field(description="Title.")', "ghost"),
        ('__doc_anchors__ = ["meta"]\n    meta: dict = Field(default_factory=dict, description="Nested.")', "meta"),
        ('subject__anchor_state: str = Field(default="", description="Reserved.")', "reserved suffix"),
    ],
)
def test_an_invalid_model_definition_is_refused_when_loaded(tmp_path: Path, body: str, reason: str) -> None:
    module = "sldb_go07_bad_definition"
    (tmp_path / f"{module}.py").write_text(f"from pydantic import Field\nfrom sldb import StructuredNLDoc\n\n\nclass Bad(StructuredNLDoc):\n    {body}\n", encoding="utf-8")
    try:
        with pytest.raises(SLDBModelError, match=f"Bad.*{reason}"):
            api.resolve_model_ref(f"{module}:Bad", str(tmp_path))
    finally:
        sys.modules.pop(module, None)


def test_optional_str_and_list_fields_are_valid_anchor_fields() -> None:
    class Fine(StructuredNLDoc):
        __doc_anchors__ = ["one", "many"]
        one: str | None = Field(default=None, description="One.")
        many: list[str] = Field(default_factory=list, description="Many.")

    from sldb.store.model_contract import doc_anchor_fields

    assert doc_anchor_fields(Fine) == ["one", "many"]
