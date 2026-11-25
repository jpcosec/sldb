"""The read tools, called by the real MCP client on the real server over the isolated copy of a
real store. Expected values come from the copy's own files (front matter of its documents),
never from literals that restate the answer."""

from __future__ import annotations

from pathlib import Path
from typing import Any

import pytest
import yaml

from mcp_helpers import files, one_document, page_items
from mcp_world import ITEM_COUNT, front_matter

TOOLS = {
    "list_models", "describe_model", "list_relation_types", "describe_relation_type",
    "read_document", "select_documents", "neighbors", "neighborhood",
    "list_views", "resolve_view", "anchors_resolve", "check_integrity", "list_signals",
}


@pytest.fixture(scope="module")
def item(mcp, store_copy: Path) -> dict[str, Any]:
    """An item that depends on another, as the store selects it from its path."""
    path = next(p for p in files(store_copy, "item") if front_matter(p)["depends_on"])
    return one_document(mcp, str(path.relative_to(store_copy)))


def test_tools_are_the_read_surface_and_read_only(mcp) -> None:
    tools = {tool.name: tool for tool in mcp.list_tools()}
    assert set(tools) == TOOLS
    for tool in tools.values():
        assert tool.annotations.read_only_hint is True and tool.annotations.destructive_hint is False, tool.name
        assert tool.output_schema is not None, f"{tool.name} returns no structured JSON"


def test_list_models_is_the_store_registry(mcp, store_copy: Path) -> None:
    index = yaml.safe_load((store_copy / ".sldb" / "core" / "store_index.yaml").read_text(encoding="utf-8"))
    models = page_items(mcp, "list_models", limit=2)
    assert {m["name"] for m in index["models"]} == {m["name"] for m in models}
    assert all(m["address"] == f"sldb://model/{m['name']}" for m in models)
    described = mcp.call("describe_model", model="Item")
    assert described["found"] and described["address"] == "sldb://model/Item"
    fields = {f["name"] for f in described["fields"]}
    written = front_matter(files(store_copy, "item")[0])
    assert {"title", "status", "owner", "stage", "depends_on"} <= fields and set(written) - {"sldb"} <= fields
    assert described["documents"]["total"] == ITEM_COUNT == len(files(store_copy, "item"))


@pytest.mark.parametrize("model,folder", [("Item", "item"), ("RuleDoc", "ruledoc"), ("RelationDoc", "relationdoc")])
def test_documents_are_the_files_of_the_store(mcp, store_copy: Path, model: str, folder: str) -> None:
    rows = page_items(mcp, "select_documents", model=model)
    assert len(rows) == len(files(store_copy, folder)) > 0, f"no {model} selected"
    for row in rows:
        assert row["address"] == f"sldb://document/{row['export_id']}"
        original = store_copy / row["path"]
        assert original.is_file(), f"{row['export_id']} is not a file of the store: {row['path']}"
        document = mcp.call("read_document", ref=row["export_id"])
        assert document["found"] and document["address"] == row["address"]
        assert document["name"] == row["name"] and document["path"] == row["path"]
        written = front_matter(original)
        shared = (set(written) & set(document["payload"])) - {"sldb"}
        assert shared, f"{row['export_id']}: no field in common with {row['path']}"
        for key in shared:
            assert document["payload"][key] == written[key], f"{row['export_id']}.{key}"


def test_read_one_field(mcp, store_copy: Path, item: dict[str, Any]) -> None:
    written = front_matter(store_copy / item["path"])
    answer = mcp.call("read_document", ref=item["export_id"], field="depends_on")
    assert answer["found"] and answer["value"] == written["depends_on"] and answer["address"] == item["address"]


def test_largest_model_comes_paged(mcp, store_copy: Path) -> None:
    totals = {m["name"]: mcp.call("select_documents", model=m["name"], limit=1)["total"] for m in page_items(mcp, "list_models")}
    largest = max(totals, key=totals.get)
    total, size = totals[largest], 5
    assert total == len(files(store_copy, largest.lower())) > 3 * size, f"the largest model {largest} has only {total} documents"
    seen: list[str] = []
    offset: int | None = 0
    while offset is not None:
        answer = mcp.call("select_documents", model=largest, offset=offset, limit=size)
        assert answer["total"] == total and len(answer["items"]) <= size
        assert answer["truncated"] == (offset + size < total)
        seen += [row["export_id"] for row in answer["items"]]
        assert all((store_copy / row["path"]).is_file() for row in answer["items"])
        offset = answer["next_offset"]
    assert len(seen) == len(set(seen)) == total
    first = mcp.call("select_documents", model=largest, limit=1)
    assert first["truncated"] and first["next_offset"] == 1 and len(first["items"]) == 1


def test_select_by_predicate(mcp, store_copy: Path) -> None:
    done = page_items(mcp, "select_documents", model="Item", where='status = "done"')
    written = [p for p in files(store_copy, "item") if front_matter(p)["status"] == "done"]
    assert written and {row["path"] for row in done} == {str(p.relative_to(store_copy)) for p in written}
    assert "predicate" in mcp.error_of("select_documents", model="Item", where="status = ")


def test_neighbors_by_relation(mcp, store_copy: Path, item: dict[str, Any]) -> None:
    written = front_matter(store_copy / item["path"])
    edges = page_items(mcp, "neighbors", node=item["export_id"], direction="outgoing", relation="references")
    assert edges and all(e["relation"] == "references" and e["source"] == item["address"] for e in edges)
    dependencies = {f"sldb://document/{ref}" for ref in written["depends_on"]}
    assert dependencies <= {e["target"] for e in edges if e["metadata"].get("field") == "depends_on"}
    dependency = next(iter(dependencies))
    incoming = page_items(mcp, "neighbors", node=dependency, direction="incoming", relation="references")
    assert item["address"] in {e["source"] for e in incoming} and all(e["target"] == dependency for e in incoming)


def test_neighborhood_by_direction(mcp, item: dict[str, Any]) -> None:
    targets = {e["target"] for e in page_items(mcp, "neighbors", node=item["export_id"], direction="outgoing")}
    one_hop = set(page_items(mcp, "neighborhood", node=item["export_id"], direction="outgoing", depth=1))
    two_hops = set(page_items(mcp, "neighborhood", node=item["export_id"], direction="outgoing", depth=2))
    assert one_hop == targets - {item["address"]} and one_hop < two_hops
    sources = {e["source"] for e in page_items(mcp, "neighbors", node=item["export_id"], direction="incoming")}
    assert set(page_items(mcp, "neighborhood", node=item["export_id"], direction="incoming", depth=1)) == sources - {item["address"]}
    assert "direction" in mcp.error_of("neighborhood", node=item["export_id"], direction="sideways")


def test_relation_types(mcp, store_copy: Path) -> None:
    types = page_items(mcp, "list_relation_types", limit=3)
    assert all(t["address"] == f"sldb://relation_type/{t['name']}" for t in types)
    declared = [front_matter(p) for p in files(store_copy, "relationtypedoc")]
    assert declared and {d["name"] for d in declared} <= {t["name"] for t in types}
    for written in declared:
        described = mcp.call("describe_relation_type", name=written["name"])
        assert described["found"] and described["direction"] == written["direction"]


def test_undeclared_answers_empty_with_explanation(mcp, item: dict[str, Any]) -> None:
    for tool, arguments in [
        ("select_documents", {"model": "NoSuchModelDoc"}),
        ("select_documents", {"model": "Item", "where": 'status = "no-such-status"'}),
        ("neighbors", {"node": item["export_id"], "relation": "no_such_relation"}),
        ("neighbors", {"node": "Item:no-such-item"}),
        ("neighborhood", {"node": "Item:no-such-item", "direction": "both"}),
    ]:
        answer = mcp.call(tool, **arguments)
        assert answer["items"] == [] and answer["total"] == 0 and not answer["truncated"], (tool, arguments)
        assert answer["explanation"], (tool, arguments)
    for tool, arguments in [
        ("read_document", {"ref": "Item:no-such-item"}),
        ("read_document", {"ref": item["export_id"], "field": "no_such_field"}),
        ("describe_model", {"model": "NoSuchModelDoc"}),
        ("describe_relation_type", {"name": "no_such_relation"}),
        ("resolve_view", {"view": "no-such-view"}),
        ("resolve_view", {"view": item["export_id"]}),
    ]:
        answer = mcp.call(tool, **arguments)
        assert answer["found"] is False and answer["explanation"], (tool, arguments)


def test_composed_and_projection_views(mcp, store_copy: Path) -> None:
    listed = page_items(mcp, "list_views")
    board = next(v for v in listed if v["kind"] == "composed")
    written = front_matter(files(store_copy, "viewdoc")[0])
    assert board["view"] == written["name"] and set(board["sections"]) == {s["key"] for s in written["sections"]}
    answer = mcp.call("resolve_view", view=board["view"])
    assert answer["found"] and answer["kind"] == "composed"
    rows = [row for group in answer["result"]["sections"]["items"]["groups"] for row in group["rows"]]
    assert {r["name"] for r in rows} == {p.stem for p in files(store_copy, "item")}
    assert all(r["fields"]["status"] == front_matter(store_copy / r["path"])["status"] for r in rows)


def test_check_integrity(mcp) -> None:
    answer = mcp.call("check_integrity", limit=10)
    assert answer["ok"] is True and answer["store"]["errors"] == 0 and answer["edges"]["errors"] == 0
    assert answer["store"]["checked"] > 0
    findings = answer["findings"]
    assert findings["total"] == answer["store"]["errors"] + answer["store"]["alerts"] + answer["edges"]["errors"]
    assert len(findings["items"]) == min(10, findings["total"]) and findings["truncated"] == (findings["total"] > 10)
