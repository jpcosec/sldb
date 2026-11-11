"""SEGURIDAD resto 2: a store with tracked Memo documents and a secret outside its root, and a way
to run the CLI (or a snippet of the API) in a fresh process with an audit hook on `open`, as the
coordinator's reproduction did (no per-process cache can hide a read).

`escape(world, "b")` turns the tracked `b.md` into a symlink to the secret; every test then checks
that the secret is never opened (not even an `O_NOFOLLOW` attempt: the audit event fires before
the syscall) and that the surface names the finding (`store/path-outside-root`)."""

from __future__ import annotations

import json
import os
import subprocess
import sys
from dataclasses import dataclass
from pathlib import Path

MODULE = "sldb_secrest2_models"
MODELS = '''from pydantic import Field
from sldb import StructuredNLDoc


class Memo(StructuredNLDoc):
    __template__ = """---
status: ⸢rev•status⸥
---

# ⸢rev•title⸥

⸢rev•body⸥
"""
    title: str = Field(description="Title.")
    status: str = Field(description="Status.")
    body: str = Field(default="", description="Body.")
'''
SETUP = f"""
from pathlib import Path
from sldb import api
root = Path.cwd()
sp = api.init_store(root).store_path
api.add_model(sp, "{MODULE}:Memo", str(root.parent))
for n, body in (("a", "See [[b]] and [[c]].\\n\\n![[b]]"), ("b", "B body."), ("c", "C body.")):
    api.create_document(sp, "Memo", root / "memos" / f"{{n}}.md", {{"title": n, "status": "open", "body": body}}, n, str(root.parent))
"""
SECRET = "---\nstatus: secret\n---\n\n# outside secret\n\nSECRET-BODY\n"
SRC = Path(__file__).resolve().parents[2] / "src"

_HOOK = r"""
import json, os, sys
opened = []
def hook(event, args):
    if event == "open" and isinstance(args[0], (str, bytes, os.PathLike)) and str(args[0]).endswith(".md"):
        opened.append(os.path.realpath(args[0]))
sys.addaudithook(hook)
"""
_CLI = _HOOK + r"""
import runpy
sys.argv = ["sldb"] + sys.argv[1:]
code, message = 0, ""
try:
    runpy.run_module("sldb", run_name="__main__")
except SystemExit as exc:
    code, message = (exc.code or 0, "") if isinstance(exc.code, (int, type(None))) else (1, str(exc.code))
with open(os.environ["AUDIT_OUT"], "w") as out:
    json.dump({"opened": opened, "code": code, "message": message}, out)
"""
_API = _HOOK + r"""
result, error = None, ""
try:
    exec(os.environ["AUDIT_CODE"])
except Exception as exc:
    error = f"{type(exc).__name__}: {exc}"
with open(os.environ["AUDIT_OUT"], "w") as out:
    json.dump({"opened": opened, "result": result, "error": error}, out, default=str)
"""


@dataclass
class World:
    root: Path
    secret: Path

    @property
    def py(self) -> str:
        return str(self.root.parent)

    def env(self, **extra: str) -> dict[str, str]:
        return {**os.environ, "PYTHONPATH": os.pathsep.join([str(SRC), self.py]), **extra}

    def cli(self, *args: str) -> dict:
        """`sldb <args>` in a new process: exit code, output and every `.md` it opened."""
        out = self.root.parent / "audit.json"
        done = subprocess.run([sys.executable, "-c", _CLI, *args], capture_output=True, text=True, env=self.env(AUDIT_OUT=str(out)), cwd=self.root)
        ran = json.loads(out.read_text(encoding="utf-8"))
        return {**ran, "output": done.stdout + done.stderr + ran["message"]}

    def api(self, code: str) -> dict:
        """`code` (it may set `result`) in a new process, with `root`, `sp` and `py` bound."""
        out = self.root.parent / "audit.json"
        prelude = f"from pathlib import Path\nroot = Path({str(self.root)!r})\nsp = root / '.sldb'\npy = {self.py!r}\n"
        done = subprocess.run([sys.executable, "-c", _API], capture_output=True, text=True, env=self.env(AUDIT_OUT=str(out), AUDIT_CODE=prelude + code), cwd=self.root)
        ran = json.loads(out.read_text(encoding="utf-8"))
        return {**ran, "output": done.stdout + done.stderr + ran["error"]}

    def outside_opened(self, ran: dict) -> bool:
        return str(self.secret.resolve()) in ran["opened"]


def make_world(tmp_path: Path) -> World:
    """A store with `memos/a.md` (linking and including `b`), `b.md`, `c.md`, and a secret outside it."""
    (tmp_path / f"{MODULE}.py").write_text(MODELS, encoding="utf-8")
    root = tmp_path / "world"
    root.mkdir()
    world = World(root, tmp_path / "outside" / "secret.md")
    subprocess.run([sys.executable, "-c", SETUP], cwd=root, env=world.env(), check=True)
    world.secret.parent.mkdir()
    world.secret.write_text(SECRET, encoding="utf-8")
    return world


def escape(world: World, name: str = "b") -> None:
    """The tracked `memos/<name>.md` becomes a symlink to the secret outside the root."""
    (world.root / "memos" / f"{name}.md").unlink()
    (world.root / "memos" / f"{name}.md").symlink_to(world.secret)
