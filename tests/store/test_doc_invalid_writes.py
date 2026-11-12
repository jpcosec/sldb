"""H2 and H3 of inbox 3895e9f7: with two documents their model rejects, untracking one of the
model's documents and a transactional write of a valid one succeed and touch nothing else; a
transaction that fails leaves the tree as it was. Each write runs in a fresh process, as a CLI
does, with the caches kept (warm) or gone as in a clean clone (cold): only a cold cache rebuilds
every document's edges, which is where an invalid neighbour used to stop the write (H2) and
leave its shards rewritten (H3)."""

from __future__ import annotations

import os
import shutil
import subprocess
import sys
from pathlib import Path

import pytest

from sldb.store.layout import documents_shard_path

from tests.store.invalid_memo_store import store_with_invalid  # noqa: F401 - the fixture

_SRC = Path(__file__).resolve().parents[2] / "src"
_TX = "with api.transaction(sp, py) as tx:\n    api.replace_text(sp, 'c', '# c', '# c2', transaction=tx, pythonpath=py)\n"


def _tree(root: Path, cache: bool = False) -> dict[str, bytes]:
    """Every file under the project; the regenerable cache only with `cache`."""
    return {p.relative_to(root).as_posix(): p.read_bytes() for p in sorted(root.rglob("*")) if p.is_file() and (cache or ".sldb_cache" not in p.parts)}


def _changed(before: dict[str, bytes], after: dict[str, bytes]) -> set[str]:
    return {p for p in before.keys() | after.keys() if before.get(p) != after.get(p)}


def _run(store, cache: str, code: str) -> subprocess.CompletedProcess:
    """`code` in a new process over the store (`api`, `sp`, `py` bound); `cold` drops every cache first."""
    root, sp, py = store
    if cache == "cold":
        shutil.rmtree(root / ".sldb_cache", ignore_errors=True)
        shutil.rmtree(os.environ["XDG_CACHE_HOME"], ignore_errors=True)
    prelude = f"import sys\nsys.path[:0] = [{str(_SRC)!r}, {py!r}]\nfrom sldb import api\nsp, py = {str(sp)!r}, {py!r}\n"
    return subprocess.run([sys.executable, "-c", prelude + code], capture_output=True, text=True, cwd=root, timeout=300)


def _shards(root: Path, sp: Path, *names: str) -> set[str]:
    return {documents_shard_path(sp, "Memo", n).relative_to(root).as_posix() for n in names}


@pytest.mark.parametrize("cache", ["warm", "cold"])
@pytest.mark.parametrize("name", ["a", "c"])
def test_untracking_beside_invalid_documents_touches_only_that_one(store_with_invalid, cache, name):
    root, sp, _py = store_with_invalid
    before = _tree(root)
    done = _run(store_with_invalid, cache, f"api.untrack_document(sp, {name!r}, py)")
    assert done.returncode == 0, done.stderr
    changed = _changed(before, _tree(root))
    assert _shards(root, sp, name) <= changed
    assert not ({"a.md", "b.md", "c.md"} | _shards(root, sp, *({"a", "b", "c"} - {name}))) & changed


@pytest.mark.parametrize("cache", ["warm", "cold"])
def test_a_transactional_write_of_a_valid_document_touches_only_it(store_with_invalid, cache):
    root, sp, _py = store_with_invalid
    before = _tree(root)
    done = _run(store_with_invalid, cache, _TX)
    assert done.returncode == 0, done.stderr
    changed = _changed(before, _tree(root))
    assert "c.md" in changed
    assert not ({"a.md", "b.md"} | _shards(root, sp, "a", "b")) & changed


@pytest.mark.parametrize("cache", ["warm", "cold"])
def test_a_failed_transaction_leaves_the_tree_as_it_was(store_with_invalid, cache):
    """Derived shards included: what the rebuilds wrote in the cache is put back or removed."""
    root, _sp, _py = store_with_invalid
    if cache == "cold":
        _run(store_with_invalid, cache, "")  # drops the caches; the snapshot below is taken cold
    before = _tree(root, cache=True)
    done = _run(store_with_invalid, "warm", _TX.replace("pythonpath=py)\n", "pythonpath=py)\n    raise RuntimeError('on purpose')\n"))
    assert done.returncode != 0 and "RuntimeError: on purpose" in done.stderr
    assert "RollbackError" not in done.stderr
    assert _changed(before, _tree(root, cache=True)) == set()
