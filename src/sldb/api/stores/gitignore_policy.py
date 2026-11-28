"""Whether the repository's ignore rules match the store's split.

`.sldb/` (the declaration and `core/`) is versioned whole, since the past of the tree is read
from git; `.sldb_cache/` is regenerable and ignored (docs/architecture/derived-store-boundary.md).
Rules are evaluated with `git check-ignore --no-index`, so a tracked file does not hide a rule
that would ignore it, and any rule that covers the cache counts, not only the literal line.
"""

from __future__ import annotations

from pathlib import Path

from sldb.ports.git import git_ok
from sldb.store.layout import cache_dir


def gitignore_policy(store_path: Path) -> dict[str, bool] | None:
    """`{core_ignored, declaration_ignored, cache_ignored, ok}` for the store's repository;
    None outside a git work tree. `ok` is: the cache ignored, nothing of `.sldb/` ignored."""
    root = store_path.resolve().parent
    if not git_ok(root, "rev-parse", "--is-inside-work-tree"):
        return None
    core = _ignored(root, store_path / "core" / "store_index.yaml")
    declaration = _ignored(root, store_path / "store.yaml")
    cache = _ignored(root, cache_dir(store_path) / "locks" / "store.lock")
    return {"core_ignored": core, "declaration_ignored": declaration, "cache_ignored": cache, "ok": cache and not core and not declaration}


def _ignored(root: Path, path: Path) -> bool:
    return git_ok(root, "check-ignore", "--quiet", "--no-index", str(path.resolve().relative_to(root.resolve())))
