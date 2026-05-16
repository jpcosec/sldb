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
    cli_main(["store", "init", "--path", str(root)])
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
            "model",
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
            "doc",
            "add",
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
        ["store", "update", "--store", str(store_path), "--pythonpath", str(root)]
    )

    assert exit_code == 1
    captured = capsys.readouterr()
    assert "Skipped missing documents: doc" in captured.out
    assert "Updated store at" in captured.out


_LOCK_HOLDER_SCRIPT = """\
import sys
sys.path.insert(0, sys.argv[1])
from pathlib import Path
from sldb.store.io import store_lock
import time
sp = Path(sys.argv[2])
duration = float(sys.argv[3])
with store_lock(sp):
    time.sleep(duration)
"""


def test_store_lock_fails_fast_when_busy(tmp_path):
    """A subprocess holding the store lock causes parallel write to fail fast."""
    root = tmp_path / "root"
    root.mkdir()
    store_path, _doc_path = _setup_store(root)

    lock_holder = subprocess.Popen(
        [sys.executable, "-c", _LOCK_HOLDER_SCRIPT, _SRC, str(store_path), "5.0"],
        env={**os.environ, "PYTHONDONTWRITEBYTECODE": "1"},
    )

    time.sleep(0.5)

    with pytest.raises(SystemExit) as exc:
        cli_main(
            ["store", "update", "--store", str(store_path), "--pythonpath", str(root)]
        )

    lock_holder.terminate()
    lock_holder.wait()
    assert "busy" in str(exc.value.code).lower() or exc.value.code != 0


def test_store_lock_wait_blocks_until_released(tmp_path):
    """The --wait flag blocks until the lock is released, then succeeds."""
    root = tmp_path / "root"
    root.mkdir()
    store_path, _doc_path = _setup_store(root)

    lock_holder = subprocess.Popen(
        [sys.executable, "-c", _LOCK_HOLDER_SCRIPT, _SRC, str(store_path), "1.5"],
        env={**os.environ, "PYTHONDONTWRITEBYTECODE": "1"},
    )

    time.sleep(0.3)

    exit_code = cli_main(
        [
            "store",
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
    from sldb.store.io import _atomic_write

    target = tmp_path / "test.yaml"
    _atomic_write(target, "hello: world\n")
    assert target.exists()
    assert target.read_text() == "hello: world\n"
    leftover = list(tmp_path.glob("*.tmp"))
    assert leftover == []


def test_atomic_write_creates_parent_dirs(tmp_path):
    """_atomic_write creates intermediate directories."""
    from sldb.store.io import _atomic_write

    target = tmp_path / "a" / "b" / "c.yaml"
    _atomic_write(target, "key: val\n")
    assert target.exists()
    assert target.read_text() == "key: val\n"
