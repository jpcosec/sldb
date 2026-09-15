from pathlib import Path

from sldb.store.layout import store_exists


def global_store_path() -> Path:
    return Path.home() / ".sldb"


def find_local_store(start: Path | None = None) -> Path | None:
    current = (start or Path.cwd()).resolve()
    for directory in [current, *current.parents]:
        candidate = directory / ".sldb"
        if store_exists(candidate):
            return candidate
    return None


def find_project_store(start: Path | None = None) -> Path | None:
    """Find the closest project store, reserving the home store for fallback."""
    global_store = global_store_path().resolve()
    for store in ancestor_stores(start):
        if store != global_store:
            return store
    return None


def ancestor_stores(start: Path | None = None) -> list[Path]:
    """Return valid stores from the current project outward, without mutation."""
    current = (start or Path.cwd()).resolve()
    return [candidate for directory in [current, *current.parents] if store_exists(candidate := directory / ".sldb")]
