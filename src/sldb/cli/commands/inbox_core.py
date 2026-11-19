import json
from pathlib import Path
from typing import Any

import yaml

from sldb.cli.store_context import get_store_context
from sldb.api.stores.store_discovery import _resolve_store_arg
from sldb.core.exceptions import SLDBStoreError
from sldb.store.layout import project_root, store_exists
from sldb.store.resolver import find_local_store


def get_desk_root(args: Any) -> Path:
    if args.desk_root:
        return Path(args.desk_root).resolve()
    if args.store:
        return (project_root(require_store_dir(args.store)) / "desk").resolve()
    return default_desk_root()


def require_store_dir(store_arg: str) -> Path:
    """Resolve `--store` and refuse a directory that holds no `.sldb` store."""
    store_path = _resolve_store_arg(store_arg).resolve()
    if not store_exists(store_path):
        raise SLDBStoreError(f"No .sldb store at '{store_arg}': pass the .sldb directory of the project (or use --desk-root).")
    return store_path


def default_desk_root() -> Path:
    local_store = find_local_store()
    if local_store is not None:
        return (project_root(local_store) / "desk").resolve()
    return (Path.cwd() / "desk").resolve()


def get_store_context_safe(args: Any) -> tuple[Path, Path] | None:
    if args.desk_root and not args.store:
        return None
    if args.store:
        return get_store_context(args.store)
    local_store = find_local_store()
    if local_store is None:
        return None
    return local_store, project_root(local_store)


def print_payload(payload: Any, fmt: str) -> None:
    if fmt == "yaml":
        print(yaml.safe_dump(payload, sort_keys=False, allow_unicode=True))
        return
    print(json.dumps(payload, indent=2, default=str))
