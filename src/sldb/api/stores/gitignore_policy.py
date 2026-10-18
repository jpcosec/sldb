"""Whether the repository's ignore rules keep `.sldb/core` versionable and `.sldb/runtime` out.

The split is sldb's (core is the durable store, runtime is local derived state), but only
deskops checked it, with a test of its own (inbox 20260904). Rules are evaluated with
`git check-ignore --no-index`, so a tracked file does not hide a rule that would ignore it.
"""

from __future__ import annotations

import subprocess
from pathlib import Path


def gitignore_policy(store_path: Path) -> dict[str, bool] | None:
    """`{core_ignored, runtime_ignored, ok}` for the store's repository; None outside a git work tree."""
    root = store_path.resolve().parent
    if _git(root, "rev-parse", "--is-inside-work-tree") != 0:
        return None
    core = _ignored(root, store_path / "core" / "store_index.yaml")
    runtime = _ignored(root, store_path / "runtime" / "locks" / "store.lock")
    return {"core_ignored": core, "runtime_ignored": runtime, "ok": runtime and not core}


def _ignored(root: Path, path: Path) -> bool:
    return _git(root, "check-ignore", "--quiet", "--no-index", str(path.resolve().relative_to(root.resolve()))) == 0


def _git(root: Path, *argv: str) -> int:
    try:
        return subprocess.run(["git", *argv], cwd=root, capture_output=True, check=False).returncode
    except OSError:
        return 1
