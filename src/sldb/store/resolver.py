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
