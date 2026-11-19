"""`apply_batch(dry_run=True)` prevalidates under the lock and writes nothing; its verdict is the
one a real apply gives."""

from __future__ import annotations

import hashlib
from pathlib import Path

import pytest

from sldb import api
from sldb.core.exceptions import SLDBStoreError, SLDBValidationError
from tests.api.test_rules_evaluation import World, world  # noqa: F401 - the fixture

OK = {"title": "d1", "status": "open"}


def _snapshot(world: World) -> dict[str, str]:
    files: dict[str, str] = {}
    for base in {world.root, Path(world.store)}:
        for path in sorted(p for p in base.rglob("*") if p.is_file() and ".git" not in p.parts):
            files[str(path)] = hashlib.sha256(path.read_bytes()).hexdigest()
    return files


def test_a_valid_dry_run_reports_and_leaves_every_file_identical(world: World) -> None:
    changes = [{"id": "d2", "action": "create", "model": "X", "payload": {**OK, "title": "d2"}}, {"id": "d1", "action": "create", "model": "X", "payload": OK}]
    before = _snapshot(world)
    report = api.apply_batch(world.store, changes, world.py, dry_run=True)
    assert (report.applied, report.saved, report.inverse, report.planned) == (False, [], [], ["d2", "d1"])
    assert _snapshot(world) == before
    real = api.apply_batch(world.store, changes, world.py)
    assert real.applied and real.saved == ["d2", "d1"]


@pytest.mark.parametrize("changes, error", [
    ([{"id": "d1", "action": "create", "model": "X", "payload": {"title": 3}}], SLDBValidationError),
    ([{"id": "d1", "action": "update", "payload": OK}], SLDBStoreError),
    ("nope", SLDBValidationError),
])
def test_an_invalid_dry_run_raises_what_a_real_apply_raises_and_writes_nothing(world: World, changes, error) -> None:
    before = _snapshot(world)
    with pytest.raises(error) as dry:
        api.apply_batch(world.store, changes, world.py, dry_run=True)
    with pytest.raises(error) as real:
        api.apply_batch(world.store, changes, world.py)
    assert str(dry.value) == str(real.value)
    assert _snapshot(world) == before
