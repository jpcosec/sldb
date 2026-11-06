"""The state one open transaction keeps over a store (`sldb.api.transaction`): how deeply it is
nested, what every touched file held before its first write, and what to forget after a rollback."""

from __future__ import annotations

from pathlib import Path
from typing import Iterable

from sldb.api.documents.transaction_paths import inside, store_signatures, unsnapshotted_drift
from sldb.api.model_registry.model_files import forget_store_caches
from sldb.api.stores.store_location import StoreLocation
from sldb.store.edge_index.compose import invalidate_composed_edge_indexes
from sldb.store.io import invalidate_index_cache
from sldb.store.io.rollback import RollbackError, restore_all, snapshot
from sldb.store.io.shards import invalidate_shard_cache


class TransactionState:
    """One store's open transaction: `depth` counts the nested `with` blocks sharing it, `saved`
    holds the first-seen bytes (or absence) of each file touched, `models` the models whose
    caches a rollback forgets, and `signatures` the store as it was on entry, to catch a file
    moved without a snapshot."""

    def __init__(self, location: StoreLocation, pythonpath: str | None) -> None:
        self.location, self.pythonpath, self.depth = location, pythonpath, 0
        self.saved: dict[Path, bytes | None] = {}
        self.models: set[str] = set()
        self.signatures = store_signatures(location.store_path)

    @property
    def store_path(self) -> Path:
        return self.location.store_path

    @property
    def root(self) -> Path:
        return self.location.project_root

    def remember(self, paths: Iterable[Path], model: str | None = None) -> None:
        """Snapshot `paths` (the first snapshot of a path wins) and note `model` as touched."""
        snapshot(paths, self.saved)
        if model is not None:
            self.models.add(model)

    def inside(self, raw: str | Path) -> Path:
        """`raw` resolved against the project root; a path outside it is refused."""
        return inside(self.root, raw)

    def relative(self, path: Path) -> str:
        try:
            return path.resolve().relative_to(self.root.resolve()).as_posix()
        except ValueError:
            return str(path)

    def rollback(self, original: BaseException) -> None:
        """Every touched file back as it was and the caches forgotten; what could not be put
        back is raised as `RollbackError`, chained to `original`."""
        failed = restore_all(self.saved)
        new, changed = unsnapshotted_drift(self.signatures, self.store_path, self.saved)
        failed += [path for path in new if not _unlink(path)] + changed
        self.forget_caches()
        if failed:
            raise RollbackError([self.relative(path) for path in failed]) from original

    def forget_caches(self) -> None:
        """The existing invalidation functions, so no in-memory copy outlives the restore."""
        for model in sorted(self.models):
            forget_store_caches(self.store_path, model)
        invalidate_index_cache()
        invalidate_shard_cache()
        invalidate_composed_edge_indexes()


def _unlink(path: Path) -> bool:
    try:
        path.unlink(missing_ok=True)
        return True
    except OSError:
        return False
