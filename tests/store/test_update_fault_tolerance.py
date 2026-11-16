from __future__ import annotations

import os
import subprocess
import sys
import time

import pytest
from sldb.cli import main as cli_main
from pathlib import Path


_SRC = str(Path(__file__).resolve().parent.parent.parent / "src")


def _setup_store(root: Path) -> Path:
    """Create a minimal store with one model for testing."""
    cli_main(["stores", "init", "--path", str(root)])
    store_path = root / ".sldb"
    model_py = root / "models.py"
    model_py.write_text(
        "from pydantic import Field\nfrom sldb import StructuredNLDoc\n"
        "class MyDoc(StructuredNLDoc):\n"
        "    __template__ = '\u2e22rev\u2022title\u2e25'\n"
        "    title: str = Field(description='The title')"
    )
    cli_main(
        [
            "models",
            "add",
            "models:MyDoc",
            "--store",
            str(store_path),
            "--pythonpath",
            str(root),
        ]
    )
    doc_path = root / "doc.md"
    cli_main(
        [
            "docs",
            "create",
            "--model",
            "MyDoc",
            "-o",
            str(doc_path),
            '{"title": "Hello"}',
            "--store",
            str(store_path),
            "--pythonpath",
            str(root),
        ]
    )
    return store_path, doc_path


def test_store_update_skips_missing_doc(tmp_path, capsys):
    root = tmp_path / "root"
    root.mkdir()
    store_path, doc_path = _setup_store(root)

    doc_path.unlink()

    exit_code = cli_main(
        ["stores", "update", "--store", str(store_path), "--pythonpath", str(root)]
    )

    assert exit_code == 1
    captured = capsys.readouterr()
    assert "Skipped missing documents: doc" in captured.out
    assert "Updated store at" in captured.out


_LOCK_HOLDER_SCRIPT = """\
import os, sys, time
sys.path.insert(0, sys.argv[1])
from pathlib import Path
from sldb.store.io import store_lock
sp = Path(sys.argv[2])
ready_file = Path(sys.argv[4])
duration = float(sys.argv[3])
with store_lock(sp):
    ready_file.write_text("ready")
    time.sleep(duration)
"""


def test_store_lock_fails_fast_when_busy(tmp_path):
    """A subprocess holding the store lock causes parallel write to fail fast."""
    root = tmp_path / "root"
    root.mkdir()
    store_path, _doc_path = _setup_store(root)

    ready_file = tmp_path / "lock_ready"
    lock_holder = subprocess.Popen(
        [sys.executable, "-c", _LOCK_HOLDER_SCRIPT, _SRC, str(store_path), "5.0", str(ready_file)],
        env={**os.environ, "PYTHONDONTWRITEBYTECODE": "1"},
    )

    for _ in range(50):
        if ready_file.exists():
            break
        time.sleep(0.1)

    assert ready_file.exists(), "Subprocess never acquired the lock"

    with pytest.raises(SystemExit) as exc:
        cli_main(
            ["stores", "update", "--store", str(store_path), "--pythonpath", str(root)]
        )

    lock_holder.terminate()
    lock_holder.wait()
    assert "busy" in str(exc.value.code).lower() or exc.value.code != 0


def test_store_lock_wait_blocks_until_released(tmp_path):
    """The --wait flag blocks until the lock is released, then succeeds."""
    root = tmp_path / "root"
    root.mkdir()
    store_path, _doc_path = _setup_store(root)

    ready_file = tmp_path / "lock_ready_wait"
    lock_holder = subprocess.Popen(
        [sys.executable, "-c", _LOCK_HOLDER_SCRIPT, _SRC, str(store_path), "1.5", str(ready_file)],
        env={**os.environ, "PYTHONDONTWRITEBYTECODE": "1"},
    )

    for _ in range(30):
        if ready_file.exists():
            break
        time.sleep(0.1)

    assert ready_file.exists(), "Subprocess never acquired the lock"

    exit_code = cli_main(
        [
            "stores",
            "update",
            "--wait",
            "--store",
            str(store_path),
            "--pythonpath",
            str(root),
        ]
    )

    lock_holder.wait()
    assert exit_code == 0


def test_atomic_write_cleans_up_temp_file(tmp_path):
    """_atomic_write leaves no .tmp file behind after success."""
    from sldb.store.io.utils import StoreIOUtils
    _atomic_write = StoreIOUtils._atomic_write

    target = tmp_path / "test.yaml"
    _atomic_write(target, "hello: world\n")
    assert target.exists()
    assert target.read_text() == "hello: world\n"
    leftover = list(tmp_path.glob("*.tmp"))
    assert leftover == []


def test_atomic_write_creates_parent_dirs(tmp_path):
    """_atomic_write creates intermediate directories."""
    from sldb.store.io.utils import StoreIOUtils
    _atomic_write = StoreIOUtils._atomic_write

    target = tmp_path / "a" / "b" / "c.yaml"
    _atomic_write(target, "key: val\n")
    assert target.exists()
    assert target.read_text() == "key: val\n"


def _git(root: Path, *args: str) -> str:
    return subprocess.run(["git", "-c", "user.name=t", "-c", "user.email=t@t", *args], cwd=root, capture_output=True, text=True, check=True).stdout


def test_a_conflicted_derived_index_says_which_command_to_run(tmp_path):
    """The exact message, for the store index and for a model index, with markers or unparseable."""
    from sldb.core.exceptions import SLDBStoreError
    from sldb.store.io import invalidate_index_cache, load_models_index, load_store_index

    store_path, _ = _setup_store(tmp_path)
    index_file, model_file = store_path / "core" / "store_index.yaml", store_path / "core" / "models" / "MyDoc.yaml"
    index_file.write_text("<<<<<<< HEAD\nstore_hash: a\n=======\nstore_hash: b\n>>>>>>> other\n", encoding="utf-8")
    model_file.write_text("name: [unclosed\n", encoding="utf-8")
    invalidate_index_cache()
    for path, load in ((index_file, lambda: load_store_index(store_path)), (model_file, lambda: load_models_index(model_file))):
        with pytest.raises(SLDBStoreError) as raised:
            load()
        assert str(raised.value) == f"{path} is a derived index that git could not merge: run `sldb stores rebuild-index` (and `sldb stores merge-driver --install` once per clone)"


def test_merge_driver_install_is_idempotent(tmp_path):
    _git(tmp_path, "init", "-q")
    cli_main(["stores", "init", "--path", str(tmp_path)])
    for _ in range(2):
        assert cli_main(["stores", "merge-driver", "--install", "--store", str(tmp_path / ".sldb")]) == 0
    lines = (tmp_path / ".gitattributes").read_text(encoding="utf-8").splitlines()
    assert lines == [".sldb/core/store_index.yaml merge=sldb", ".sldb/core/models/*.yaml merge=sldb", ".sldb/store.yaml merge=sldb"]
    assert _git(tmp_path, "config", "--get", "merge.sldb.driver").strip() == "sldb stores merge-driver %O %A %B %P"
    assert _git(tmp_path, "config", "--get", "merge.sldb.name").strip()


def test_stores_init_alerts_when_another_branch_already_has_a_store(tmp_path, capsys):
    _git(tmp_path, "init", "-q", "-b", "main")
    cli_main(["stores", "init", "--path", str(tmp_path)])
    _git(tmp_path, "add", "-A")
    _git(tmp_path, "commit", "-qm", "store")
    _git(tmp_path, "checkout", "-q", "--orphan", "dev")
    _git(tmp_path, "rm", "-rq", "--cached", ".")
    import shutil
    shutil.rmtree(tmp_path / ".sldb")
    capsys.readouterr()
    assert cli_main(["stores", "init", "--path", str(tmp_path)]) == 0
    assert "alert: branch 'main' already has a store at .sldb/" in capsys.readouterr().err
