"""Propose and apply, called by the real MCP client on the real server at write level 2 over its
own copy of a real store. Payloads start from documents the store tracks."""

from __future__ import annotations

from pathlib import Path
from typing import Any

import pytest

from mcp_helpers import an_item, files, page_items, tracked, valid_edge
from mcp_session import WRITER
from mcp_world import front_matter

EDGE_PENDING = "edge_validation_before_write"


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


def test_an_edge_against_its_relation_type_is_reported(writer, write_copy: Path) -> None:
    edge = valid_edge(write_copy, "edge-wrong-source")
    allowed = front_matter(files(write_copy, "relationtypedoc")[0])["source_types"]
    item = an_item(writer, write_copy)
    assert item["model"] not in allowed
    wrong = {**edge, "source": item["export_id"]}
    proposal = writer.call("propose_changes", changes=[wrong])
    assert any(p["note"].startswith("sldb:") for p in proposal["pending"] if EDGE_PENDING in p["what"] or "RelationTypeDoc" in p["what"])
    answer = writer.call("apply_changes", proposal=proposal["proposal"])
    try:
        assert answer["applied"] is True
        assert any("source_types" in f and item["export_id"] in f for f in answer["edge_findings"]), answer["edge_findings"]
    finally:
        applied(writer, [{"action": "retract_edge", "name": wrong["name"]}])


def test_cardinality_and_condition_of_a_declared_type_are_reported(writer, write_copy: Path) -> None:
    base = tracked(writer, write_copy, files(write_copy, "relationtypedoc")[0])
    name = "one_to_one"
    declared = {"action": "create", "model": "RelationTypeDoc", "name": f"type-{name}", "path": f"relationtypedoc/type-{name}.md", "payload": {**base["payload"], "name": name, "title": "One to one", "cardinality": "one_to_one", "target_types": []}}
    applied(writer, [declared])
    first, second = valid_edge(write_copy, "card-1"), valid_edge(write_copy, "card-2")
    # Two targets for one source under a one_to_one type, the second with a condition that does not parse.
    edges = [{**first, "relation_type": name}, {**second, "relation_type": name, "target": "Stage:review", "condition": "status = "}]
    try:
        findings = applied(writer, edges)["edge_findings"]
        assert any(f"has 2 '{name}' targets but cardinality is one_to_one" in f for f in findings), findings
        assert any("condition does not parse" in f for f in findings), findings
    finally:
        applied(writer, [{"action": "retract_edge", "name": e["name"]} for e in edges] + [{"action": "delete", "model": "RelationTypeDoc", "name": f"type-{name}"}])


@pytest.mark.xfail(strict=True, reason="SLDB checks an edge against its RelationTypeDoc only after the write (check_edges); asked by note, see PENDING['edge_validation_before_write']")
def test_an_edge_against_its_relation_type_is_refused_before_writing(writer, write_copy: Path) -> None:
    edge = valid_edge(write_copy, "edge-refused")
    item = an_item(writer, write_copy)
    wrong = {**edge, "source": item["export_id"]}
    answer = apply(writer, [wrong])
    try:
        assert answer["applied"] is False and not (write_copy / wrong["path"]).exists()
    finally:
        if answer["applied"]:
            applied(writer, [{"action": "retract_edge", "name": wrong["name"]}])
