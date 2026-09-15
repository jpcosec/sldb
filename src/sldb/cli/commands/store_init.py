from __future__ import annotations
from pathlib import Path
from typing import Any
from sldb.store.io import save_semantic_dag, save_semantic_index, save_store_index
from sldb.store.layout import store_exists
from sldb.store.models import SemanticDAG, StoreIndex, SemanticIndex
from sldb.store.predicates import default_predicates
from sldb.store.catalog import register_project_store

def init_store(args: Any) -> int:
    root = Path(args.path).resolve()
    sp = root / ".sldb"
    if _already_initialized(sp, args.force):
        return 0
    if store_exists(sp):
        _remove_store(sp)
    _create_store(sp)
    _register_globally(sp)
    print(f"Initialized store at {sp}")
    return 0


def _already_initialized(store_path: Path, force: bool) -> bool:
    if store_exists(store_path) and not force:
        print(f"Store already exists at {store_path}. Use --force to reinitialize.")
        return True
    return False


def _remove_store(store_path: Path) -> None:
    import shutil
    shutil.rmtree(store_path)


def _create_store(sp: Path) -> None:
    save_store_index(sp, StoreIndex(predicates=default_predicates()))
    save_semantic_dag(sp, SemanticDAG(equivalences={}))
    save_semantic_index(sp, SemanticIndex())


def _register_globally(store_path: Path) -> None:
    from sldb.store.resolver import global_store_path
    global_store = global_store_path().resolve()
    if store_path.resolve() == global_store:
        return
    if not global_store.exists():
        _create_store(global_store)
    register_project_store(store_path)
