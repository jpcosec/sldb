"""The desk copies the benchmark works on, and the cache purge that makes a run cold."""

from __future__ import annotations

import json
import shutil
import subprocess
import sys
from pathlib import Path


MARKER = ".sldb-bench"


def claim_workdir(workdir: Path) -> None:
    """Refuse a non-empty directory the benchmark did not create: cleanup deletes inside it."""
    if workdir.is_dir() and any(workdir.iterdir()) and not (workdir / MARKER).exists():
        raise ValueError(f"--workdir {workdir} is not empty and is not a bench workdir")
    workdir.mkdir(parents=True, exist_ok=True)
    (workdir / MARKER).touch()


def release_workdir(workdir: Path, names: list[str]) -> None:
    """Delete only what the benchmark made: the copies, the XDG cache and the marker."""
    for name in [*names, "xdg"]:
        shutil.rmtree(workdir / name, ignore_errors=True)
    (workdir / MARKER).unlink(missing_ok=True)
    if not any(workdir.iterdir()):
        workdir.rmdir()


def copy_desk(source: Path, workdir: Path, name: str) -> Path:
    """Copy the working tree of `source` into `workdir/name`, without its `.sldb_cache`.

    The working tree and not a clone: generated documents (the sldb store's
    `knowledge/symbols/`, about 3300 files) are ignored by git and a clone would measure
    a store with them missing. The source is only read.
    """
    target = workdir / name
    if target.exists():
        shutil.rmtree(target)
    shutil.copytree(source, target, symlinks=True, ignore=shutil.ignore_patterns(".sldb_cache"))
    return target


def purge_caches(copy: Path | None, xdg: Path) -> None:
    """Cold start: no `.sldb_cache` in the copy and an empty XDG cache for sldb."""
    if copy is not None:
        shutil.rmtree(copy / ".sldb_cache", ignore_errors=True)
    shutil.rmtree(xdg, ignore_errors=True)
    xdg.mkdir(parents=True)


def pick_document(copy: Path, env: dict[str, str]) -> Path | None:
    """The first tracked Markdown document of the copy, per `sldb docs list`."""
    argv = [sys.executable, "-m", "sldb", "docs", "list", "--format", "json"]
    out = subprocess.run(argv, cwd=copy, env=env, capture_output=True, text=True).stdout
    docs = json.loads(out or "{}").get("documents", [])
    paths = (copy / d.get("path", "") for d in docs if str(d.get("path", "")).endswith(".md"))
    return next((p for p in paths if p.is_file()), None)


def touch_document(path: Path) -> None:
    """The one-document change: a newline appended at the end."""
    with path.open("a", encoding="utf-8") as handle:
        handle.write("\n")
