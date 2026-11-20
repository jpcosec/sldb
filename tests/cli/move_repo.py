"""A throwaway git repo holding a store with `FileDoc` documents whose fields name repo paths."""

from __future__ import annotations

import subprocess
import sys
from pathlib import Path

from sldb import api

MODULE = "sldb_move_test_models"
MODELS = '''from pydantic import Field
from sldb import StructuredNLDoc


class FileDoc(StructuredNLDoc):
    __template__ = """# ⸢rev•title⸥

Target: ⸢rev•target⸥

## Files

- ⸢rev,list•files⸥
""".strip()
    title: str = Field(description="Title.")
    target: str = Field(description="A repo path.")
    files: list[str] = Field(description="Repo paths.")
'''


def git(root: Path, *args: str) -> str:
    return subprocess.run(["git", *args], cwd=root, capture_output=True, text=True, check=True).stdout


def build_repo(tmp_path: Path) -> tuple[Path, str]:
    """`(root, pythonpath)`: a git repo with a store, `FileDoc` registered, and one commit."""
    sys.modules.pop(MODULE, None)
    (tmp_path / f"{MODULE}.py").write_text(MODELS, encoding="utf-8")
    root = tmp_path / "repo"
    root.mkdir()
    git(root, "init", "-q")
    git(root, "config", "user.email", "t@example.com")
    git(root, "config", "user.name", "t")
    api.init_store(root)
    api.add_model(root / ".sldb", f"{MODULE}:FileDoc", str(tmp_path))
    return root, str(tmp_path)


def commit_all(root: Path) -> None:
    git(root, "add", "-A")
    git(root, "commit", "-q", "-m", "base")


def write(root: Path, rel: str, text: str) -> Path:
    path = root / rel
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8")
    return path


def track(root: Path, pythonpath: str, name: str, rel: str, target: str, files: list[str] | None = None) -> None:
    """Create the tracked document `name` at `rel`."""
    payload = {"title": name, "target": target, "files": files or ["none"]}
    api.create_document(root / ".sldb", "FileDoc", root / rel, payload, name, pythonpath)


def snapshot(root: Path) -> dict[str, bytes]:
    """Every file under `root` but `.git` and the cache, by relative path."""
    skip = (".git", ".sldb_cache")
    return {p.relative_to(root).as_posix(): p.read_bytes() for p in root.rglob("*") if p.is_file() and not any(s in p.relative_to(root).parts for s in skip)}


def field(root: Path, pythonpath: str, name: str) -> dict:
    doc = next(d for d in api.load_runtime_documents(root / ".sldb", pythonpath) if d.name == name)
    return doc.payload
