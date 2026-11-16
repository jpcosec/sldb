"""Other local branches of the same repository that already have a store at this path: the
alert `sldb stores init` gives before a second store is born on a branch (one store per repo:
two stores in two branches only meet again in a merge, MEPU 20261115-195033)."""

from __future__ import annotations

import subprocess
from pathlib import Path


def branches_with_store(root: Path) -> list[str]:
    """Local branches other than the current one whose tree has a store at `<root>/.sldb/`
    (its `store.yaml`, or the `core/store_index.yaml` of a store never declared); empty outside git."""
    rel = _git(root, "rev-parse", "--show-prefix")
    if rel is None:
        return []
    current = (_git(root, "branch", "--show-current") or "").strip()
    heads = (_git(root, "for-each-ref", "--format=%(refname:short)", "refs/heads") or "").split()
    targets = [f"{rel.strip()}.sldb/{name}" for name in ("store.yaml", "core/store_index.yaml")]
    return [b for b in heads if b != current and (_git(root, "ls-tree", "--full-tree", "--name-only", b, "--", *targets) or "").strip()]


def _git(cwd: Path, *args: str) -> str | None:
    try:
        run = subprocess.run(["git", *args], cwd=cwd, capture_output=True, text=True, check=False)
    except OSError:
        return None
    return run.stdout if run.returncode == 0 else None
