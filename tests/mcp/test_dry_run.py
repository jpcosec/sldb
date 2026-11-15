"""The dry run: `propose_changes` answers what would be written and changes no file."""

from __future__ import annotations

from pathlib import Path

from mcp_helpers import an_item, files, tracked, valid_edge
from mcp_session import tree_digest


def test_a_dry_run_answers_what_would_be_written_and_writes_nothing(writer, write_copy: Path) -> None:
    item = an_item(writer, write_copy)
    created = {**item["payload"], "title": "Dry run", "depends_on": []}
    retracted = tracked(writer, write_copy, files(write_copy, "relationdoc")[-1])
    edge = valid_edge(write_copy, "dry-run-edge")
    changes = [
        {"action": "create", "model": item["model"], "name": "dry-run", "payload": created, "path": "item/dry-run.md"},
        {"action": "update", "model": item["model"], "name": item["name"], "fields": {"title": item["payload"]["title"] + " (dry)"}},
        edge,
        {"action": "retract_edge", "name": retracted["name"]},
    ]
    before = tree_digest(write_copy)
    answer = writer.call("propose_changes", changes=changes)
    assert tree_digest(write_copy) == before, "the dry run changed a file"
    assert answer["dry_run"] is True and answer["written"] is False

    would = {w["export_id"]: w for w in answer["would_write"]}
    assert set(would) == {f"{item['model']}:dry-run", item["export_id"], "RelationDoc:dry-run-edge", retracted["export_id"]}
    assert would[f"{item['model']}:dry-run"]["payload"] == created
    update = would[item["export_id"]]
    assert update["action"] == "update" and update["changed_fields"] == ["title"] and update["path"] == item["path"]
    assert update["payload"] == {**item["payload"], "title": item["payload"]["title"] + " (dry)"}
    written_edge = would["RelationDoc:dry-run-edge"]["payload"]
    assert (written_edge["source_id"], written_edge["target_id"], written_edge["relation_type"]) == (edge["source"], edge["target"], edge["relation_type"])
    assert would[retracted["export_id"]]["action"] == "delete" and would[retracted["export_id"]]["path"] == retracted["path"]

    batch = {c["id"]: c for c in answer["proposal"]["changes"]}
    for name in (item["name"], retracted["name"]):
        assert batch[name]["expected_source_hash"], f"the server filled no guard for {name}"
    assert not (write_copy / "item/dry-run.md").exists() and not (write_copy / edge["path"]).exists()
    assert (write_copy / retracted["path"]).is_file()
    assert any(p["note"].startswith("sldb:") and "dry run" in p["what"] for p in answer["pending"]), "the missing SLDB dry run is not declared"
