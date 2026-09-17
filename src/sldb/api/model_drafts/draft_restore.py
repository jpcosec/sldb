"""Snapshot the files a promotion rewrites, and put them back if the promotion fails.

Moved here from `sldb.cli.commands.models_validate_utils`, which re-exports these names.
"""

from __future__ import annotations

import contextlib
from collections.abc import Iterator
from pathlib import Path

from sldb.api.stores.open_store import open_store
from sldb.store.layout import core_dir, semantic_dag_path, semantic_index_path


def store_index_files(store: str | Path | None) -> list[Path]:
    """Every file a model reindex may rewrite: the store core indexes and the semantic runtime indexes."""
    sp = open_store(store).store_path
    return [*(p for p in core_dir(sp).rglob("*") if p.is_file()), semantic_index_path(sp), semantic_dag_path(sp)]


@contextlib.contextmanager
def restored_on_failure(paths: list[Path]) -> Iterator[None]:
    """Snapshot ``paths``; if the block raises, write them back and re-raise."""
    snapshot = {p: p.read_bytes() if p.exists() else None for p in paths}
    try:
        yield
    except BaseException:
        _restore(snapshot)
        raise


def _restore(snapshot: dict[Path, bytes | None]) -> None:
    """Write every snapshotted file back, deleting the ones that did not exist."""
    for p, content in snapshot.items():
        if content is None:
            p.unlink(missing_ok=True)
        else:
            p.write_bytes(content)
