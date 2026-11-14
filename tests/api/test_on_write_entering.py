"""H4: `create_document` and `track_document_file` evaluate the `on_write` rules as a save does
(rules.md §9.1). An error refuses the document and nothing is written or tracked; `apply_batch`
and `transaction` inherit the refusal and restore the tree; `stores build` does not evaluate."""

from __future__ import annotations

import pytest

from sldb import api
from sldb.core.exceptions import SLDBRuleViolationError
from sldb.runtime.validation import render_model_markdown
from tests.api.test_rules_evaluation import MODULE, World, world  # noqa: F401 - the fixture

OPEN, CLOSED = {"title": "x3", "status": "open"}, {"title": "x3", "status": "closed"}


def _tracked(world: World, name: str) -> bool:
    return api.edge_node(world.store, f"X:{name}") is not None


def _hand_written(world: World, name: str, payload: dict):
    model_type = api.resolve_model_ref(f"{MODULE}:X", world.py)
    path = world.root / f"{name}.md"
    path.write_text(render_model_markdown(model_type, payload) + "\n", encoding="utf-8")
    return path


def test_a_created_document_that_breaks_an_on_write_rule_is_refused_and_nothing_is_written(world: World) -> None:
    world.rule("closed", moment="on_write")
    with pytest.raises(SLDBRuleViolationError, match="rules/closed"):
        world.doc("X", "x3", OPEN)
    assert not (world.root / "x3.md").exists() and not _tracked(world, "x3")


def test_a_created_document_that_passes_is_written_and_tracked(world: World) -> None:
    world.rule("closed", moment="on_write")
    world.doc("X", "x3", CLOSED)
    assert (world.root / "x3.md").exists() and _tracked(world, "x3")


def test_a_tracked_file_that_breaks_an_on_write_rule_is_refused_and_not_tracked(world: World) -> None:
    world.rule("closed", moment="on_write")
    path = _hand_written(world, "x3", OPEN)
    with pytest.raises(SLDBRuleViolationError, match="rules/closed"):
        api.track_document_file(world.store, "X", path, "x3", world.py)
    assert path.exists() and not _tracked(world, "x3")


def test_a_tracked_file_that_passes_is_tracked(world: World) -> None:
    world.rule("closed", moment="on_write")
    api.track_document_file(world.store, "X", _hand_written(world, "x3", CLOSED), "x3", world.py)
    assert _tracked(world, "x3")


def test_apply_batch_inherits_the_refusal_and_leaves_the_tree_as_it_was(world: World) -> None:
    world.rule("closed", moment="on_write")
    changes = [{"id": "x3", "action": "create", "model": "X", "payload": CLOSED}, {"id": "x4", "action": "create", "model": "X", "payload": {**OPEN, "title": "x4"}}]
    with pytest.raises(SLDBRuleViolationError):
        api.apply_batch(world.store, changes, world.py)
    assert not any((world.root / f"{name}.md").exists() or _tracked(world, name) for name in ("x3", "x4"))


def test_transaction_create_inherits_the_refusal_and_restores_the_tree(world: World) -> None:
    world.rule("closed", moment="on_write")
    with pytest.raises(SLDBRuleViolationError), api.transaction(world.store, world.py) as tx:
        tx.create("X", "x3", CLOSED, world.root / "x3.md")
        tx.create("X", "x4", {**OPEN, "title": "x4"}, world.root / "x4.md")
    assert not any((world.root / f"{name}.md").exists() or _tracked(world, name) for name in ("x3", "x4"))


def test_a_store_without_on_write_rules_creates_as_before(world: World) -> None:
    world.rule("closed")
    world.doc("X", "x3", OPEN)
    assert _tracked(world, "x3")
