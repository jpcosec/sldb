"""`undo_changes` works from another server process: the write journal is the store's, not the session's."""

from __future__ import annotations

import sys
from pathlib import Path
from typing import Any

import pytest

pytest.importorskip("mcp", reason="the `mcp` extra is not installed")

sys.path.insert(0, str(Path(__file__).parent / "mcp"))

import sldb.api as api  # noqa: E402
from mcp_helpers import an_item  # noqa: E402
from mcp_session import WRITER, copy_of, served, tree_digest  # noqa: E402
from mcp_world import build  # noqa: E402


@pytest.fixture(scope="module")
def world(tmp_path_factory: pytest.TempPathFactory) -> Path:
    return copy_of(build(tmp_path_factory.mktemp("undo-world") / "world"), tmp_path_factory, "undo-sessions")


def retitle(item: dict[str, Any], title: str) -> list[dict[str, Any]]:
    return [{"action": "update", "model": item["model"], "name": item["name"], "fields": {"title": title}}]


def apply(root: Path, changes: list[dict[str, Any]]) -> None:
    """Apply in a server of its own, which ends when this returns."""
    with served(root, "--level", "2", "--actor", WRITER) as session:
        proposal = session.call("propose_changes", changes=changes)["proposal"]
        assert session.call("apply_changes", proposal=proposal)["applied"] is True


def undo(root: Path, **arguments: Any) -> dict[str, Any]:
    with served(root, "--level", "2", "--actor", WRITER) as session:
        return session.call("undo_changes", **arguments)


def store_hash(root: Path) -> str:
    return api.store_fingerprint(root / ".sldb").store_hash


def title(root: Path, item: dict[str, Any]) -> str:
    """Read by a server of its own: this process caches what it read before."""
    with served(root, "--level", "2") as session:
        return session.call("read_document", ref=item["export_id"], field="title")["value"]


def test_a_new_process_undoes_what_another_applied_in_reverse_order(world: Path) -> None:
    with served(world, "--level", "2") as session:
        item = an_item(session, world)
    original, h0 = title(world, item), store_hash(world)
    apply(world, retitle(item, "first"))
    h1 = store_hash(world)
    apply(world, retitle(item, "second"))
    assert h0 != h1 != store_hash(world)
    two = undo(world)
    assert two["applied"] is True and two["undone"] == 1 and two["remaining"] == 1, two
    assert (title(world, item), store_hash(world)) == ("first", h1)
    one = undo(world)
    assert one["applied"] is True and one["remaining"] == 0, one
    assert (title(world, item), store_hash(world)) == (original, h0)
    nothing = undo(world)
    assert nothing["applied"] is False and nothing["rejected"] == "nothing_to_undo" and nothing["written"] is False, nothing


def test_an_id_is_accepted_only_for_the_last_not_reverted_batch(world: Path) -> None:
    with served(world, "--level", "2") as session:
        item = an_item(session, world)
    apply(world, retitle(item, "older"))
    apply(world, retitle(item, "newer"))
    from sldb.store import write_journal

    older, newer = write_journal.unreverted(world / ".sldb")[-2:]
    before = tree_digest(world)
    refused = undo(world, batch_id=older["batch_id"])
    assert refused["applied"] is False and refused["rejected"] == "nothing_to_undo" and older["batch_id"] in refused["explanation"], refused
    assert tree_digest(world) == before
    assert undo(world, batch_id=newer["batch_id"])["applied"] is True
    assert undo(world, batch_id=older["batch_id"])["applied"] is True


def test_a_batch_whose_document_changed_afterwards_is_refused_and_nothing_is_written(world: Path) -> None:
    with served(world, "--level", "2") as session:
        item = an_item(session, world)
    apply(world, retitle(item, "mine"))
    api.save_document_payload(world / ".sldb", item["model"], item["name"], {**item["payload"], "title": "edited by hand"}, pythonpath=str(world), actor="human:x")
    before = tree_digest(world)
    answer = undo(world)
    assert answer["applied"] is False and answer["rejected"] == "stale" and answer["written"] is False and answer["document"] == item["name"], answer
    assert tree_digest(world) == before
