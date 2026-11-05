"""Whether the repository's ignore rules match the store's split.

`.sldb/` (the declaration and `core/`) is versioned whole, since the past of the tree is read
from git; `.sldb_cache/` is regenerable and ignored (docs/architecture/derived-store-boundary.md).
Rules are evaluated with `git check-ignore --no-index`, so a tracked file does not hide a rule
that would ignore it, and any rule that covers the cache counts, not only the literal line.
"""

from __future__ import annotations

import subprocess
from pathlib import Path

from sldb.store.layout import cache_dir


def gitignore_policy(store_path: Path) -> dict[str, bool] | None:
    """`{core_ignored, declaration_ignored, cache_ignored, ok}` for the store's repository;
    None outside a git work tree. `ok` is: the cache ignored, nothing of `.sldb/` ignored."""
    root = store_path.resolve().parent
    if _git(root, "rev-parse", "--is-inside-work-tree") != 0:
        return None
    core = _ignored(root, store_path / "core" / "store_index.yaml")
    declaration = _ignored(root, store_path / "store.yaml")
    cache = _ignored(root, cache_dir(store_path) / "locks" / "store.lock")
    return {"core_ignored": core, "declaration_ignored": declaration, "cache_ignored": cache, "ok": cache and not core and not declaration}


def _ignored(root: Path, path: Path) -> bool:
    return _git(root, "check-ignore", "--quiet", "--no-index", str(path.resolve().relative_to(root.resolve()))) == 0


def _git(root: Path, *argv: str) -> int:
    try:
        return subprocess.run(["git", *argv], cwd=root, capture_output=True, check=False).returncode
    except OSError:
        return 1
