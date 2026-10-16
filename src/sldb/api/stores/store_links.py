"""The links a store records, each with the state of its target computed when asked.

The state is never persisted: a link whose target moved or was never cloned on this machine
is reported as `missing` or `not-a-store`, never raised and never hidden.
"""

from __future__ import annotations

from pathlib import Path

from sldb.store.io import load_store_index
from sldb.store.layout import project_root, store_exists


def store_links(store_path: Path) -> list[dict[str, str]]:
    """Every direct link of the store, sorted by name.

    Args:
        store_path: The linking store's `.sldb` directory.

    Returns:
        One `{name, path, resolved, status}` per link: `path` as recorded, `resolved` the
        absolute `.sldb` it points to, `status` one of `ok`, `missing` (no directory there)
        or `not-a-store` (a directory that holds no store).
    """
    root = project_root(store_path)
    entries = sorted(load_store_index(store_path).stores, key=lambda e: e.name)
    return [_link_state(root, e.name, e.path) for e in entries]


def find_link(store_path: Path, name: str) -> dict[str, str] | None:
    """The direct link recorded under `name`, with its state, or None when there is none."""
    return next((link for link in store_links(store_path) if link["name"] == name), None)


def _link_state(root: Path, name: str, path: str) -> dict[str, str]:
    resolved = Path(path) if Path(path).is_absolute() else (root / path).resolve()
    status = "ok" if store_exists(resolved) else ("not-a-store" if resolved.exists() else "missing")
    return {"name": name, "path": path, "resolved": str(resolved), "status": status}
