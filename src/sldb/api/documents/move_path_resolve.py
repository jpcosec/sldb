"""The checks before a move: the path exists, the destination is free and stays inside the project."""

from __future__ import annotations

from pathlib import Path

from sldb.api.documents.move_path_remap import Remap
from sldb.api.documents.transaction_paths import inside
from sldb.api.stores.store_location import StoreLocation
from sldb.core.exceptions import SLDBStoreError


def resolve_move(location: StoreLocation, source: str | Path, destination: str | Path) -> Remap:
    """The `Remap` of moving `source` to `destination`, or `SLDBStoreError` naming what is wrong;
    nothing has been touched at that point."""
    root = location.project_root.resolve()
    src, dst = inside(root, source), inside(root, destination)
    _refuse(root, location.store_path.resolve(), src, dst, (source, destination))
    return Remap(src.relative_to(root).as_posix(), dst.relative_to(root).as_posix(), src.is_dir())


def _refuse(root: Path, store: Path, src: Path, dst: Path, given: tuple) -> None:
    if not (src.exists() or src.is_symlink()):
        raise SLDBStoreError(f"Cannot move '{given[0]}': it does not exist.")
    if src == root or src == store or store.is_relative_to(src):
        raise SLDBStoreError(f"Cannot move '{given[0]}': it holds the project root or the store.")
    if dst.exists() or dst.is_symlink():
        raise SLDBStoreError(f"Cannot move to '{given[1]}': a file or directory already exists there.")
    if dst.is_relative_to(src):
        raise SLDBStoreError(f"Cannot move '{given[0]}' into itself ('{given[1]}').")
