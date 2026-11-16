"""`apply_batch` holds the store lock from prevalidation to the last write: with two real
processes carrying the same `expected_source_hash`, one wins and the other gets `ConflictError`
and writes nothing, not even the other change of its batch."""

from __future__ import annotations

import hashlib
import subprocess
import sys
import time
from pathlib import Path

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
def marked(*args, **kwargs):
    plan = real(*args, **kwargs)
    (marks / ("ready" if hold == "1" else "entered")).write_text("x")
    while hold == "1" and not (marks / "go").exists():
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


def _spawn(api_store, tmp_path, hold, title, source_hash):
    args = [sys.executable, "-c", CHILD, str(api_store.store), api_store.pythonpath, hold, str(tmp_path), title, source_hash]
    return subprocess.Popen(args, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)


def _wait_for(path: Path) -> None:
    for _ in range(500):
        if path.exists():
            return
        time.sleep(0.02)


def _shard(api_store, name: str):
    return load_document_shard(documents_shard_path(api_store.store, "TicketDoc", name))


def test_second_process_with_the_same_guard_conflicts_and_leaves_no_partial_write(api_store, tmp_path):
    source_hash = _shard(api_store, "login").source_hash
    first = _spawn(api_store, tmp_path, "1", "Winner", source_hash)
    _wait_for(tmp_path / "ready")
    assert (tmp_path / "ready").exists(), first.communicate()
    second = _spawn(api_store, tmp_path, "0", "Loser", source_hash)
    _wait_for(tmp_path / "started")
    assert (tmp_path / "started").exists(), second.communicate()
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


def test_store_lock_is_reentrant_in_process_and_keeps_excluding_others(api_store):
    other = [sys.executable, "-c", "import sys\nfrom pathlib import Path\nfrom sldb.store.io import store_lock\nfrom sldb.store.exceptions import SLDBStoreError\ntry:\n    with store_lock(Path(sys.argv[1])): print('GOT')\nexcept SLDBStoreError: print('BUSY')", str(api_store.store)]
    with store_lock(api_store.store, wait=True):
        with store_lock(api_store.store):
            pass
        assert subprocess.run(other, capture_output=True, text=True, timeout=60).stdout.strip() == "BUSY"  # the inner release did not drop the outer lock
    assert subprocess.run(other, capture_output=True, text=True, timeout=60).stdout.strip() == "GOT"

