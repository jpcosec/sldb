"""SEGURIDAD (resto, after live_stale): no store command opens a tracked document whose path is a
symlink or resolves outside the project root. Each command names it with the finding `stores
check` gives it (`store/path-outside-root`, `store/symlink-not-read`) and goes on; `docs track` and
`docs update` refuse it before opening (or writing) anything.

Every command runs as the CLI in a fresh process with an audit hook on `open`, as the
coordinator's reproduction did, so no per-process cache can hide a read.
"""

from __future__ import annotations

import json
import os
import subprocess
import sys
from pathlib import Path

import pytest

MODULE = "sldb_tracked_reads_guarded_models"
_MODELS = '''from pydantic import Field
from sldb import StructuredNLDoc


class Memo(StructuredNLDoc):
    __references__ = ["title"]
    __template__ = """---
status: ⸢rev•status⸥
---

# ⸢rev•title⸥
"""
    title: str = Field(description="Title.")
    status: str = Field(description="Status.")
'''

_SETUP = f"""
from pathlib import Path
from sldb import api
root = Path.cwd()
sp = api.init_store(root).store_path
api.add_model(sp, "{MODULE}:Memo", str(root.parent))
for n in ("a", "b"):
    api.create_document(sp, "Memo", root / f"{{n}}.md", {{"title": n, "status": "open"}}, n, str(root.parent))
"""

_AUDITED = r"""
import json, os, runpy, sys
opened = []
def hook(event, args):
    if event == "open" and isinstance(args[0], str) and args[0].endswith(".md"):
        opened.append(os.path.realpath(args[0]))
sys.addaudithook(hook)
sys.argv = ["sldb"] + sys.argv[1:]
code, message = 0, ""
try:
    runpy.run_module("sldb", run_name="__main__")
except SystemExit as exc:  # the CLI exits with its error message as the code
    code, message = (exc.code or 0, "") if isinstance(exc.code, (int, type(None))) else (1, str(exc.code))
with open(os.environ["AUDIT_OUT"], "w") as out:
    json.dump({"opened": opened, "code": code, "message": message}, out)
"""

_SRC = Path(__file__).resolve().parents[2] / "src"
_SECRET = "---\nstatus: secret\n---\n\n# outside secret\n"


def _run(world: Path, *args: str) -> dict:
    """`sldb <args> --store .sldb` in a new process: its exit, its output and every `.md` it opened."""
    out = world.parent / "audit.json"
    env = {**os.environ, "PYTHONPATH": os.pathsep.join([str(_SRC), str(world.parent)]), "AUDIT_OUT": str(out)}
    done = subprocess.run([sys.executable, "-c", _AUDITED, *args, "--store", ".sldb"], capture_output=True, text=True, env=env, cwd=world)
    ran = json.loads(out.read_text(encoding="utf-8"))
    return {**ran, "output": done.stdout + done.stderr + ran["message"]}


@pytest.fixture
def world(tmp_path):
    """A declared, committed store with `a.md` and `b.md`, and a secret outside its root."""
    (tmp_path / f"{MODULE}.py").write_text(_MODELS, encoding="utf-8")
    root = tmp_path / "world"
    root.mkdir()
    env = {**os.environ, "PYTHONPATH": os.pathsep.join([str(_SRC), str(tmp_path)])}
    subprocess.run([sys.executable, "-c", _SETUP], cwd=root, env=env, check=True)
    subprocess.run([sys.executable, "-m", "sldb", "stores", "declare", "--write", "--store", ".sldb"], cwd=root, env=env, check=True, capture_output=True)
    for git in (["init", "-q"], ["add", "."], ["-c", "user.name=t", "-c", "user.email=t@t", "commit", "-qm", "init"]):
        subprocess.run(["git", *git], cwd=root, check=True)
    (tmp_path / "outside").mkdir()
    secret = tmp_path / "outside" / "secret.md"
    secret.write_text(_SECRET, encoding="utf-8")
    return root, secret


def _escape(root: Path, secret: Path) -> None:
    """`b.md`, tracked and declared, becomes a symlink to the secret outside the root."""
    (root / "b.md").unlink()
    (root / "b.md").symlink_to(secret)


@pytest.mark.parametrize("command", [["stores", "check"], ["stores", "update"], ["stores", "build"], ["stores", "build", "--check"]])
def test_a_store_command_does_not_open_a_tracked_symlink_out_of_the_root_and_names_it(world, command):
    root, secret = world
    _escape(root, secret)
    ran = _run(root, *command, *(["--pythonpath", str(root.parent)] if command[-1] in ("check", "update") else []))
    assert str(secret.resolve()) not in ran["opened"]
    assert "store/path-outside-root" in ran["output"]
    assert "Unexpected" not in ran["output"] and "Traceback" not in ran["output"]


def test_docs_update_of_another_document_does_not_open_it(world):
    root, secret = world
    _escape(root, secret)
    ran = _run(root, "docs", "update", "a", "{title: a, status: closed}", "--pythonpath", str(root.parent))
    assert ran["code"] == 0 and str(secret.resolve()) not in ran["opened"]


def test_docs_update_of_the_symlink_is_refused_and_writes_nothing_outside(world):
    root, secret = world
    _escape(root, secret)
    ran = _run(root, "docs", "update", "b", "{title: b, status: pwned}", "--pythonpath", str(root.parent))
    assert ran["code"] != 0 and "resolves outside the project root" in ran["output"]
    assert str(secret.resolve()) not in ran["opened"]
    assert secret.read_text(encoding="utf-8") == _SECRET


def test_docs_track_of_a_symlink_out_of_the_root_is_refused_without_opening_it(world):
    root, secret = world
    (root / "new.md").symlink_to(Path("..") / "outside" / "secret.md")
    ran = _run(root, "docs", "track", "new.md", "--model", "Memo", "--pythonpath", str(root.parent))
    assert ran["code"] != 0 and "resolves outside the project root" in ran["output"]
    assert str(secret.resolve()) not in ran["opened"]


def test_docs_track_of_a_symlink_inside_the_root_is_refused_too(world):
    root, _ = world
    (root / "real.md").write_text((root / "a.md").read_text(encoding="utf-8"), encoding="utf-8")
    (root / "new.md").symlink_to(root / "real.md")
    ran = _run(root, "docs", "track", "new.md", "--model", "Memo", "--name", "new", "--pythonpath", str(root.parent))
    assert ran["code"] != 0 and "is a symlink" in ran["output"]
    assert str((root / "real.md").resolve()) not in ran["opened"]


def test_stores_update_names_a_tracked_symlink_inside_the_root_and_goes_on(world):
    root, _ = world
    (root / "b.md").rename(root / "real-b.md")
    (root / "b.md").symlink_to(root / "real-b.md")
    ran = _run(root, "stores", "update", "--pythonpath", str(root.parent))
    assert "store/symlink-not-read" in ran["output"] and "Updated store" in ran["output"]
    assert str((root / "real-b.md").resolve()) not in ran["opened"]
