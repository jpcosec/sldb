"""Propose and apply, called by the real MCP client on the real server at write level 2 over its
own copy of a real store. Payloads start from documents the store tracks."""

from __future__ import annotations

from pathlib import Path
from typing import Any

import pytest

from mcp_helpers import an_item, files, page_items, tracked, valid_edge
from mcp_session import WRITER, served, tree_digest
from mcp_world import front_matter


def apply(session, changes: list[dict[str, Any]]) -> dict[str, Any]:
    """Propose `changes` and apply the proposal exactly as it came back."""
    return session.call("apply_changes", proposal=session.call("propose_changes", changes=changes)["proposal"])


def applied(session, changes: list[dict[str, Any]]) -> dict[str, Any]:
    answer = apply(session, changes)
    assert answer["applied"] is True, answer
    return answer


def signed_by_the_writer(answer: dict[str, Any], write_copy: Path, via: str) -> None:
    """Every document written carries who wrote it and through which operation, in the answer and on disk."""
    for document in answer["documents"]:
        assert document["provenance"]["by"] == WRITER and document["provenance"]["via"] == via, document
        on_disk = front_matter(write_copy / document["path"])["sldb"]
        assert on_disk["by"] == WRITER and on_disk["via"] == via, (document["path"], on_disk)


def test_cycle_on_a_document(writer, write_copy: Path) -> None:
    item = an_item(writer, write_copy)
    name = "item-cycle"
    payload = {**item["payload"], "title": "The cycle: propose, validate, apply", "depends_on": []}
    created = applied(writer, [{"action": "create", "model": item["model"], "name": name, "payload": payload, "path": f"item/{name}.md"}])
    export_id = f"{item['model']}:{name}"
    assert [d["export_id"] for d in created["documents"]] == [export_id]
    signed_by_the_writer(created, write_copy, "create_document")
    read = writer.call("read_document", ref=export_id)
    assert read["found"] and read["payload"] == payload

    updated = applied(writer, [{"action": "update", "model": item["model"], "name": name, "fields": {"title": payload["title"] + " (edited)"}}])
    signed_by_the_writer(updated, write_copy, "save_document_payload")
    assert writer.call("read_document", ref=export_id, field="title")["value"] == payload["title"] + " (edited)"

    deleted = applied(writer, [{"action": "delete", "model": item["model"], "name": name}])
    assert deleted["deleted"] == [read["address"]] and deleted["documents"] == []
    assert writer.call("read_document", ref=export_id)["found"] is False
    assert not (write_copy / read["path"]).exists()


def test_cycle_on_an_edge(writer, write_copy: Path) -> None:
    edge = valid_edge(write_copy, "cycle-edge")
    target = writer.call("read_document", ref=edge["target"])["address"]

    def targets() -> set[str]:
        return {e["target"] for e in page_items(writer, "neighbors", node=edge["source"], direction="outgoing", relation=edge["relation_type"])}

    assert target not in targets(), "the edge exists already; it would prove nothing"
    asserted = applied(writer, [edge])
    assert asserted["edge_findings"] == [], asserted["edge_findings"]
    signed_by_the_writer(asserted, write_copy, "create_document")
    assert target in targets()
    stored = writer.call("read_document", ref="RelationDoc:cycle-edge")["payload"]
    assert (stored["source_id"], stored["target_id"], stored["relation_type"]) == (edge["source"], edge["target"], edge["relation_type"])

    applied(writer, [{"action": "retract_edge", "name": "cycle-edge"}])
    assert target not in targets()
    assert not (write_copy / edge["path"]).exists()


def test_a_change_to_a_store_that_moved_since_the_proposal_is_rejected(writer, write_copy: Path) -> None:
    item = an_item(writer, write_copy)
    first = writer.call("propose_changes", changes=[{"action": "update", "model": item["model"], "name": item["name"], "fields": {"title": "first proposal"}}])
    second = writer.call("propose_changes", changes=[{"action": "update", "model": item["model"], "name": item["name"], "fields": {"title": "second proposal"}}])
    assert writer.call("apply_changes", proposal=second["proposal"])["applied"] is True
    stale = writer.call("apply_changes", proposal=first["proposal"])
    assert stale["applied"] is False and stale["rejected"] == "stale" and stale["document"] == item["name"]
    assert "changed" in stale["explanation"]
    assert "# second proposal" in (write_copy / item["path"]).read_text(encoding="utf-8")


def test_an_edited_proposal_is_refused(writer, write_copy: Path) -> None:
    item = an_item(writer, write_copy)
    proposal = writer.call("propose_changes", changes=[{"action": "update", "model": item["model"], "name": item["name"], "fields": {"title": "sealed"}}])["proposal"]
    proposal["changes"][0]["expected_source_hash"] = None
    assert "propose it again" in writer.error_of("apply_changes", proposal=proposal)


def a_rule(writer, root: Path, name: str, **fields: Any) -> dict[str, Any]:
    """A RuleDoc change: the world's first RuleDoc, under a new name with `fields`."""
    rule = tracked(writer, root, files(root, "ruledoc")[0])
    return {"action": "create", "model": "RuleDoc", "name": name, "payload": {**rule["payload"], **fields}, "path": f"ruledoc/{name}.md"}


def test_an_error_rule_refuses_the_change_and_is_named(writer, write_copy: Path) -> None:
    rule = a_rule(writer, write_copy, "rule-edges-explain-themselves", title="An authored edge explains itself", subject="model <= RelationDoc", where="", condition="nonempty(notes)", severity="error", moment="on_write", message="An authored edge explains itself in its notes.")
    applied(writer, [rule])
    try:
        silent = {**valid_edge(write_copy, "edge-without-notes"), "notes": ""}
        refused = apply(writer, [silent])
        assert refused["applied"] is False and refused["rejected"] == "rules"
        assert refused["rules"] == [f"rules/{rule['name']}"] and rule["name"] in refused["explanation"]
        assert refused["findings"][0]["level"] == "error" and refused["findings"][0]["subject"] == "RelationDoc:edge-without-notes"
        assert not (write_copy / silent["path"]).exists()
    finally:
        applied(writer, [{"action": "delete", "model": "RuleDoc", "name": rule["name"]}])


def test_an_alert_rule_is_reported_by_name(writer, write_copy: Path) -> None:
    rules = [p for p in files(write_copy, "ruledoc") if front_matter(p)["moment"] == "on_write" and front_matter(p)["severity"] == "alert"]
    assert rules, "the world declares no on_write alert"
    item = tracked(writer, write_copy, next(p for p in files(write_copy, "item") if not front_matter(p)["owner"]))
    answer = applied(writer, [{"action": "update", "model": item["model"], "name": item["name"], "fields": {"title": item["payload"]["title"] + " (touched)"}}])
    codes = {a["code"] for a in answer["alerts"] if a["subject"] == item["export_id"]}
    assert {f"rules/{tracked(writer, write_copy, p)['name']}" for p in rules} <= codes, answer["alerts"]


def test_an_edge_against_its_relation_type_is_refused_before_writing(writer, write_copy: Path) -> None:
    edge = valid_edge(write_copy, "edge-refused")
    item = an_item(writer, write_copy)
    wrong = {**edge, "source": item["export_id"]}
    answer = writer.call("propose_changes", changes=[wrong])
    assert answer["applied"] is False and answer["rejected"] == "edges" and not (write_copy / wrong["path"]).exists()
    assert answer["findings"][0]["code"] == "types" and item["export_id"] in answer["findings"][0]["message"]


def retitled(item: dict[str, Any], title: str) -> list[dict[str, Any]]:
    """The change that sets an item's title."""
    return [{"action": "update", "model": item["model"], "name": item["name"], "fields": {"title": title}}]


def two_items(session, root: Path) -> tuple[dict[str, Any], dict[str, Any]]:
    """Two different items of the world, read."""
    return an_item(session, root), an_item(session, root, with_dependency=False)


def written_by_someone_else(root: Path, changes: list[dict[str, Any]]) -> None:
    """Apply `changes` from another server process, the way another client would."""
    with served(root, "--level", "2", "--actor", WRITER) as other:
        applied(other, changes)


def test_undo_changes_is_served_and_puts_the_store_back(write_copy: Path) -> None:
    with served(write_copy, "--level", "2", "--actor", WRITER) as session:
        assert "undo_changes" in {t.name for t in session.list_tools()}
        item, other = two_items(session, write_copy)
        export_ids = {r["export_id"] for r in page_items(session, "select_documents", model=item["model"])}
        name = "item-undone"
        applied(session, [{"action": "create", "model": item["model"], "name": name, "payload": {**item["payload"], "title": "To be undone", "depends_on": []}, "path": f"item/{name}.md"}])
        applied(session, retitled(item, "undone title"))
        applied(session, retitled(other, "undone too"))
        one = session.call("undo_changes")
        assert one["applied"] is True and one["undone"] == 1 and one["remaining"] == 2, one
        assert session.call("read_document", ref=other["export_id"])["payload"] == other["payload"]
        two = session.call("undo_changes", steps=2)
        assert two["applied"] is True and two["undone"] == 2 and two["remaining"] == 0, two
        assert session.call("read_document", ref=item["export_id"])["payload"] == item["payload"]
        assert {r["export_id"] for r in page_items(session, "select_documents", model=item["model"])} == export_ids
        assert not (write_copy / f"item/{name}.md").exists()


def test_undo_after_someone_else_wrote_is_a_conflict_and_writes_nothing(write_copy: Path) -> None:
    with served(write_copy, "--level", "2", "--actor", WRITER) as session:
        item = an_item(session, write_copy)
        applied(session, retitled(item, "mine"))
        written_by_someone_else(write_copy, retitled(item, "someone else's"))
        before = tree_digest(write_copy)
        stale = session.call("undo_changes")
        assert stale["applied"] is False and stale["rejected"] == "stale" and stale["written"] is False, stale
        assert stale["undone"] == 0 and stale["remaining"] == 1 and stale["document"] == item["name"], stale
        assert tree_digest(write_copy) == before, "a refused undo changed a file"
        assert session.call("read_document", ref=item["export_id"], field="title")["value"] == "someone else's"


def test_undo_of_a_document_that_went_back_to_the_content_the_batch_left_is_not_stale(write_copy: Path) -> None:
    with served(write_copy, "--level", "2", "--actor", WRITER) as session:
        item = an_item(session, write_copy)
        applied(session, retitled(item, "mine"))
        written_by_someone_else(write_copy, retitled(item, "someone else's"))
        written_by_someone_else(write_copy, retitled(item, "mine"))  # same content, new provenance
        answer = session.call("undo_changes")
        assert answer["applied"] is True and answer["undone"] == 1 and answer["remaining"] == 0, answer
        assert session.call("read_document", ref=item["export_id"])["payload"] == item["payload"]


def test_undo_of_several_is_whole_or_nothing(write_copy: Path) -> None:
    with served(write_copy, "--level", "2", "--actor", WRITER) as session:
        item, other = two_items(session, write_copy)
        applied(session, retitled(item, "first") + retitled(other, "first too"))
        applied(session, retitled(item, "second"))  # the newer batch edits a document of the older one
        written_by_someone_else(write_copy, retitled(other, "overwritten"))  # the older one is now stale
        before = tree_digest(write_copy)
        answer = session.call("undo_changes", steps=2)
        assert answer["applied"] is False and answer["rejected"] == "stale" and answer["document"] == other["name"], answer
        assert answer["written"] is False and answer["undone"] == 0 and answer["remaining"] == 2, answer
        assert tree_digest(write_copy) == before, "a refused chain changed a file"
        assert session.call("read_document", ref=item["export_id"], field="title")["value"] == "second"
        assert session.call("undo_changes")["applied"] is True, "the stack was left intact"


def test_undo_of_a_chain_over_the_same_document_applies_step_by_step(write_copy: Path) -> None:
    with served(write_copy, "--level", "2", "--actor", WRITER) as session:
        item = an_item(session, write_copy)
        applied(session, retitled(item, "one"))
        applied(session, retitled(item, "two"))
        answer = session.call("undo_changes", steps=2)
        assert answer["applied"] is True and answer["undone"] == 2 and answer["remaining"] == 0, answer
        assert session.call("read_document", ref=item["export_id"])["payload"] == item["payload"]


def test_undo_with_nothing_to_undo_is_a_clear_refusal(write_copy: Path) -> None:
    with served(write_copy, "--level", "2", "--actor", WRITER) as session:
        before = tree_digest(write_copy)
        answer = session.call("undo_changes")
        assert answer["applied"] is False and answer["rejected"] == "nothing_to_undo" and answer["written"] is False, answer
        assert answer["remaining"] == 0 and "0 applied batch(es)" in answer["explanation"], answer
        assert tree_digest(write_copy) == before
