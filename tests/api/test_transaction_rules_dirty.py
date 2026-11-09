"""The rollback of `sldb.api.transaction` restores the rules dirty set (GO08,
`<.sldb_cache>/rules/dirty.json`): every `on_write` of the transaction rewrites it, so a failed
transaction re-raises its own error (or `ConflictError`), not `RollbackError`, and leaves the
set and the documents as they were; a commit leaves the set as the writes left it; an absent
set stays absent (hallazgo de deskops CC32).
"""

from __future__ import annotations

from pathlib import Path

import pytest

from sldb import api
from sldb.core.exceptions import ConflictError
from sldb.store.layout import cache_dir
from tests.api.test_rules_evaluation import World, world  # noqa: F401 - the fixture


class Boom(RuntimeError):
    pass


def _dirty(world: World) -> Path:
    return cache_dir(world.store) / "rules" / "dirty.json"


def _dirty_world(world: World) -> bytes:
    world.rule("closed")
    api.rules_on_check(world.store)
    return _dirty(world).read_bytes()


def test_an_own_error_is_raised_and_the_dirty_set_and_document_are_restored(world: World) -> None:
    before, doc = _dirty_world(world), (world.root / "x1.md").read_bytes()
    with pytest.raises(Boom), api.transaction(world.store, world.py) as tx:
        tx.update("x1", {"title": "x1", "status": "closed"})
        assert _dirty(world).read_bytes() != before
        raise Boom("boom")
    assert _dirty(world).read_bytes() == before
    assert (world.root / "x1.md").read_bytes() == doc


def test_a_stale_source_hash_after_a_write_is_a_conflict_not_a_rollback_error(world: World) -> None:
    before, doc = _dirty_world(world), (world.root / "x1.md").read_bytes()
    with pytest.raises(ConflictError), api.transaction(world.store, world.py) as tx:
        tx.update("x1", {"title": "x1", "status": "closed"})
        tx.update("x2", {"title": "x2", "status": "closed"}, expected_source_hash="stale")
    assert _dirty(world).read_bytes() == before
    assert (world.root / "x1.md").read_bytes() == doc


def test_a_commit_leaves_the_dirty_set_as_the_writes_left_it(world: World) -> None:
    before = _dirty_world(world)
    with api.transaction(world.store, world.py) as tx:
        tx.update("x1", {"title": "x1", "status": "closed"})
    assert _dirty(world).read_bytes() != before
    assert '"X:x1"' in _dirty(world).read_text(encoding="utf-8")


def test_an_absent_dirty_set_stays_absent_after_a_failed_transaction(world: World) -> None:
    world.rule("closed")
    assert not _dirty(world).exists()
    with pytest.raises(Boom), api.transaction(world.store, world.py) as tx:
        tx.update("x1", {"title": "x1", "status": "closed"})
        raise Boom("boom")
    assert not _dirty(world).exists()
