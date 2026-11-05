"""`sldb stores migrate-layout`: move a store's cache from `.sldb/runtime/` to `.sldb_cache/`.

Until 2026-11-04 the regenerable half of a store lived inside it, at `.sldb/runtime/`, and the
repository ignored `.sldb/core/` and `.sldb/runtime/`. Now `.sldb/` is versioned whole and the
cache is its sibling `.sldb_cache/`, ignored (docs/architecture/derived-store-boundary.md). The
migration moves the content of `.sldb/runtime/` there (edges, sections, semantic, graphs, locks),
deletes the journal without archiving it (the past of the store is git's: owner's decision,
2026-10-29), removes `.sldb/runtime/` and rewrites the root `.gitignore`: the lines ignoring
`.sldb/core/` or `.sldb/runtime/` go, `.sldb_cache/` comes in, every other line stays as it was.
"""

from __future__ import annotations

import shutil
from pathlib import Path

from sldb.api.stores.gitignore_lines import rewrite_for_split
from sldb.api.stores.open_store import open_store
from sldb.core.exceptions import SLDBStoreError
from sldb.store.layout import cache_dir, store_exists

JOURNAL_DIR = "journal"
JOURNAL_LOCK = Path("locks") / "journal.lock"


def legacy_runtime_dir(store_path: Path) -> Path:
    """Where the cache lived before 2026-11-04: `.sldb/runtime/`."""
    return store_path / "runtime"


def migrate_layout(store: str | Path | None = None, force: bool = False) -> dict:
    """Move the store's cache to `.sldb_cache/` and fix the root `.gitignore`.

    Args:
        store: The store (`.sldb` directory, its project, an alias, or None to discover it the
            way every other `stores` command does).
        force: Replace a `.sldb_cache/` that already exists with content: it is deleted first.
            Without `.sldb/runtime/` there is nothing to move and nothing is refused: the
            `.gitignore` is still fixed, so running it twice is safe.

    Returns:
        `{store, cache, moved, journal_removed, runtime_removed, gitignore: {path, removed, added}}`:
        what moved (directory and file names), whether a journal was deleted, and the
        `.gitignore` lines dropped and whether `.sldb_cache/` was added.

    Raises:
        SLDBStoreError: `.sldb_cache/` exists with content and `force` is False.
    """
    store_path = _store_dir(store)
    runtime, cache = legacy_runtime_dir(store_path), cache_dir(store_path)
    if runtime.is_dir() and cache.is_dir() and any(cache.iterdir()):
        if not force:
            raise SLDBStoreError(f"{cache} exists and is not empty; pass --force to replace it with the content of {runtime}.")
        shutil.rmtree(cache)
    report = _move_runtime(runtime, cache)
    return {"store": str(store_path), "cache": str(cache), **report, "gitignore": rewrite_for_split(store_path.parent / ".gitignore")}


def _store_dir(store: str | Path | None) -> Path:
    """The `.sldb` directory: a `--store` naming the project is taken as its `.sldb`."""
    store_path = open_store(store, mode="default").store_path
    child = store_path / ".sldb"
    if not store_exists(store_path) and not legacy_runtime_dir(store_path).is_dir() and (store_exists(child) or legacy_runtime_dir(child).is_dir()):
        return child
    return store_path


def _move_runtime(runtime: Path, cache: Path) -> dict:
    """Everything under `runtime` to `cache`, except the journal and its lock, then `runtime` goes."""
    if not runtime.is_dir():
        return {"moved": [], "journal_removed": False, "runtime_removed": False}
    journal_removed = _drop_journal(runtime)
    cache.mkdir(parents=True, exist_ok=True)
    moved = [child.name for child in sorted(runtime.iterdir())]
    for name in moved:
        shutil.move(str(runtime / name), str(cache / name))
    shutil.rmtree(runtime)
    return {"moved": moved, "journal_removed": journal_removed, "runtime_removed": True}


def _drop_journal(runtime: Path) -> bool:
    """The journal and its lock are deleted, not moved; True when there was a journal."""
    journal = runtime / JOURNAL_DIR
    existed = journal.exists()
    shutil.rmtree(journal, ignore_errors=True)
    (runtime / JOURNAL_LOCK).unlink(missing_ok=True)
    return existed
