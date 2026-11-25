"""propose_changes / apply_changes refuse a batch whose relations violate their relation type
(classes, cardinality, condition) before writing, and `apply_batch(dry_run=True)` says the same."""

from __future__ import annotations

import importlib.util
import sys
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).parent / "mcp"))
pytest.importorskip("mcp", reason="the `mcp` extra is not installed")
_spec = importlib.util.spec_from_file_location("mcp_fixtures_conftest", Path(__file__).parent / "mcp" / "conftest.py")
_fixtures = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(_fixtures)
built_world, store_copy, write_copy, writer = _fixtures.built_world, _fixtures.store_copy, _fixtures.write_copy, _fixtures.writer

import sldb.api as api  # noqa: E402
from mcp_helpers import an_item, files, tracked, valid_edge  # noqa: E402
from mcp_world import front_matter  # noqa: E402
from mcp_session import tree_digest  # noqa: E402


def store_hash(root: Path) -> str:
    return api.store_fingerprint(root / ".sldb").store_hash


def type_doc(session, root: Path, name: str, **fields) -> dict:
    base = tracked(session, root, files(root, "relationtypedoc")[0])
    return {"action": "create", "model": "RelationTypeDoc", "name": f"type-{name}", "path": f"relationtypedoc/type-{name}.md", "payload": {**base["payload"], "name": name, "title": name, **fields}}


def refused(session, root: Path, changes, code: str, count: int = 1) -> dict:
    before, digest = store_hash(root), tree_digest(root)
    answer = session.call("propose_changes", changes=changes)
    if True:
        assert answer["applied"] is False and answer["rejected"] == "edges" and answer["written"] is False, answer
        codes = [f["code"] for f in answer["findings"]]
        assert codes.count(code) == count, answer["findings"]
        for finding in answer["findings"]:
            assert set(finding["relation"]) == {"source", "type", "target"} and finding["relation_doc"]
    assert store_hash(root) == before and tree_digest(root) == digest
    return answer


def test_a_relation_between_models_its_type_does_not_admit_is_refused(writer, write_copy: Path) -> None:
    item = an_item(writer, write_copy)
    wrong = {**valid_edge(write_copy, "edge-wrong-source"), "source": item["export_id"]}
    answer = refused(writer, write_copy, [wrong], "types")
    assert answer["findings"][0]["relation"]["source"] == item["export_id"]
    assert not (write_copy / wrong["path"]).exists()


def test_a_relation_over_the_cardinality_is_refused(writer, write_copy: Path) -> None:
    declared = type_doc(writer, write_copy, "one_to_one", cardinality="one_to_one", target_types=[])
    assert writer.call("apply_changes", proposal=writer.call("propose_changes", changes=[declared])["proposal"])["applied"] is True
    try:
        first, second = valid_edge(write_copy, "card-1"), valid_edge(write_copy, "card-2")
        edges = [{**first, "relation_type": "one_to_one"}, {**second, "relation_type": "one_to_one", "target": "Stage:review"}]
        refused(writer, write_copy, edges, "cardinality", count=2)
    finally:
        delete = {"action": "delete", "model": "RelationTypeDoc", "name": "type-one_to_one"}
        answer = writer.call("propose_changes", changes=[delete])
        assert "proposal" in answer, answer
        assert writer.call("apply_changes", proposal=answer["proposal"])["applied"] is True


def test_a_relation_that_breaks_the_condition_is_refused(writer, write_copy: Path) -> None:
    bad = {**valid_edge(write_copy, "edge-bad-condition"), "condition": "status = "}
    refused(writer, write_copy, [bad], "condition")


def test_a_valid_relation_and_an_invalid_one_are_refused_together(writer, write_copy: Path) -> None:
    item = an_item(writer, write_copy)
    good = valid_edge(write_copy, "edge-good")
    wrong = {**valid_edge(write_copy, "edge-wrong"), "source": item["export_id"], "target": "Stage:review"}
    answer = refused(writer, write_copy, [good, wrong], "types")
    assert {f["relation_doc"] for f in answer["findings"]} == {"edge-wrong"}
    assert not (write_copy / good["path"]).exists()


def test_a_valid_batch_is_proposed_and_applied_as_before(writer, write_copy: Path) -> None:
    edge = valid_edge(write_copy, "edge-fine")
    proposal = writer.call("propose_changes", changes=[edge])
    assert proposal["dry_run"] is True and not any("edge_validation" in p["what"] or "edge checked" in p["what"] for p in proposal["pending"])
    answer = writer.call("apply_changes", proposal=proposal["proposal"])
    try:
        assert answer["applied"] is True and answer["edge_findings"] == []
    finally:
        writer.call("apply_changes", proposal=writer.call("propose_changes", changes=[{"action": "retract_edge", "name": edge["name"]}])["proposal"])


def test_a_relation_may_lean_on_another_of_the_same_batch(writer, write_copy: Path) -> None:
    declared = type_doc(writer, write_copy, "batch_type", cardinality="many_to_many")
    edge = {**valid_edge(write_copy, "edge-in-batch"), "relation_type": "batch_type"}
    answer = writer.call("propose_changes", changes=[declared, edge])
    assert answer.get("dry_run") is True, answer


def test_apply_batch_dry_run_reports_the_same_rejections(writer, write_copy: Path) -> None:
    item = an_item(writer, write_copy)
    wrong = {**valid_edge(write_copy, "edge-dry"), "source": item["export_id"]}
    answer = writer.call("propose_changes", changes=[wrong])
    before = store_hash(write_copy)
    batch = [{"id": "edge-dry", "action": "create", "model": "RelationDoc", "path": wrong["path"], "payload": {"title": "t", "source_id": wrong["source"], "target_id": wrong["target"], "relation_type": wrong["relation_type"], "notes": "n"}}]
    report = api.apply_batch(write_copy / ".sldb", batch, dry_run=True)
    assert report.applied is False and store_hash(write_copy) == before
    assert [(r["code"], r["relation"]) for r in report.rejections] == [(f["code"], f["relation"]) for f in answer["findings"]]
