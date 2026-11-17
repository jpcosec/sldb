"""`apply_batch` holds the store lock from prevalidation to the last write: with two real
processes carrying the same `expected_source_hash`, one wins and the other gets `ConflictError`
and writes nothing, not even the other change of its batch."""

from __future__ import annotations

import hashlib
import subprocess
import sys
import time
from contextlib import contextmanager
from pathlib import Path

import pytest

from sldb.api.stores.store_check import check_store
from sldb.store.io import store_lock
from sldb.store.io.shards import load_document_shard
from sldb.store.layout import documents_shard_path

CHILD = r'''
import sys, time
from pathlib import Path
import sldb.api as api
import sldb.api.documents.apply_batch as ab
from sldb.core.exceptions import ConflictError

store, pythonpath, hold, marks, title, source_hash = sys.argv[1:7]
marks = Path(marks)
real = ab.prevalidate_changes
HOLD_LIMIT = float(sys.argv[7])             # an orphan never waits for marks/go forever
def marked(*args, **kwargs):
    plan = real(*args, **kwargs)
    (marks / ("ready" if hold == "1" else "entered")).write_text("x")
    deadline = time.monotonic() + HOLD_LIMIT
    while hold == "1" and not (marks / "go").exists():
        if time.monotonic() > deadline:
            sys.exit(3)                     # nonzero, and the lock is released on the way out
        time.sleep(0.02)                    # the first holds here, after prevalidating
    return plan
ab.prevalidate_changes = marked
payload = {"title": title, "status": "open", "tags": ["auth"]}
changes = [
    {"id": "login", "action": "update", "payload": payload, "expected_source_hash": source_hash},
    {"id": "extra-" + title.lower(), "action": "create", "model": "TicketDoc", "payload": payload, "path": "extra-" + title.lower() + ".md"},
]
(marks / ("started" if hold == "0" else "_")).write_text("x")
try:
    api.apply_batch(store, changes, pythonpath)
    print("OK")
except ConflictError:
    print("CONFLICT")
'''


@contextmanager
def _processes(api_store, tmp_path):
    """Yields a launcher that registers every child; on exit, passing or failing, kills and waits for the live ones."""
    children: list[subprocess.Popen] = []

    def spawn(hold, title, source_hash, hold_limit="120"):
        args = [sys.executable, "-c", CHILD, str(api_store.store), api_store.pythonpath, hold, str(tmp_path), title, source_hash, hold_limit]
        children.append(subprocess.Popen(args, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True))
        return children[-1]

    spawn.children = children
    try:
        yield spawn
    finally:
        for child in children:
            if child.poll() is None:
                child.kill()
            child.communicate(timeout=30)


@pytest.fixture
def spawn(api_store, tmp_path):
    with _processes(api_store, tmp_path) as launcher:
        yield launcher


def _alive(pid: int) -> bool:
    try:
        state = Path(f"/proc/{pid}/stat").read_text().rsplit(")", 1)[1].split()[0]
    except FileNotFoundError:
        return False
    return state != "Z"


def _wait_for(path: Path) -> None:
    for _ in range(500):
        if path.exists():
            return
        time.sleep(0.02)


def _shard(api_store, name: str):
    return load_document_shard(documents_shard_path(api_store.store, "TicketDoc", name))


def test_second_process_with_the_same_guard_conflicts_and_leaves_no_partial_write(api_store, tmp_path, spawn):
    source_hash = _shard(api_store, "login").source_hash
    first = spawn("1", "Winner", source_hash)
    _wait_for(tmp_path / "ready")
    assert (tmp_path / "ready").exists(), first.communicate(timeout=60)
    second = spawn("0", "Loser", source_hash)
    _wait_for(tmp_path / "started")
    assert (tmp_path / "started").exists(), second.communicate(timeout=60)
    time.sleep(1.0)
    assert not (tmp_path / "entered").exists()  # the second waits on the lock before prevalidating
    (tmp_path / "go").write_text("x")
    out1, err1 = first.communicate(timeout=60)
    out2, err2 = second.communicate(timeout=60)
    assert (out1.strip(), out2.strip()) == ("OK", "CONFLICT"), (err1, err2)
    login = (api_store.root / "login.md").read_bytes()
    assert b"Winner" in login and b"Loser" not in login
    assert _shard(api_store, "login").source_hash.removeprefix("sha256:") == hashlib.sha256(login).hexdigest() != source_hash
    assert (api_store.root / "extra-winner.md").exists()
    assert not (api_store.root / "extra-loser.md").exists()  # the loser's create was not written
    assert not documents_shard_path(api_store.store, "TicketDoc", "extra-loser").exists()
    assert check_store(api_store.store, api_store.root, api_store.pythonpath)["ok"]


def _flow_that_fails_while_the_lock_is_held(api_store, tmp_path, spawn):
    source_hash = _shard(api_store, "login").source_hash
    spawn("1", "Winner", source_hash)
    _wait_for(tmp_path / "ready")
    spawn("0", "Loser", source_hash)
    _wait_for(tmp_path / "started")
    raise RuntimeError("simulated failure of the test, before marks/go")


def test_a_failing_test_leaves_no_child_alive(api_store, tmp_path):
    with pytest.raises(RuntimeError, match="simulated failure"):
        with _processes(api_store, tmp_path) as spawn:
            children = spawn.children
            _flow_that_fails_while_the_lock_is_held(api_store, tmp_path, spawn)
    assert len(children) == 2 and (tmp_path / "ready").exists()
    assert [child.pid for child in children if _alive(child.pid)] == []
    assert all(child.returncode is not None for child in children)


def test_the_held_child_gives_up_on_marks_go_after_its_limit_and_exits_nonzero(api_store, tmp_path, spawn):
    held = spawn("1", "Winner", _shard(api_store, "login").source_hash, hold_limit="0.5")
    out, err = held.communicate(timeout=60)
    assert (tmp_path / "ready").exists() and held.returncode == 3, (out, err)
    assert b"Winner" not in (api_store.root / "login.md").read_bytes()


def test_store_lock_is_reentrant_in_process_and_keeps_excluding_others(api_store):
    other = [sys.executable, "-c", "import sys\nfrom pathlib import Path\nfrom sldb.store.io import store_lock\nfrom sldb.store.exceptions import SLDBStoreError\ntry:\n    with store_lock(Path(sys.argv[1])): print('GOT')\nexcept SLDBStoreError: print('BUSY')", str(api_store.store)]
    with store_lock(api_store.store, wait=True):
        with store_lock(api_store.store):
            pass
        assert subprocess.run(other, capture_output=True, text=True, timeout=60).stdout.strip() == "BUSY"  # the inner release did not drop the outer lock
    assert subprocess.run(other, capture_output=True, text=True, timeout=60).stdout.strip() == "GOT"

