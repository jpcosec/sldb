"""`build_store`: the store made to match its declaration, in one report. Links, models,
predicates, the declared files, the generators, the indexes, then what the declaration misses
(`undeclared`, `missing`), and last the scaffold of folders and seeds (`scaffold`).

Generators are sldb commands and `sldb.api` does not import `sldb.cli`, so the caller hands
them in as `generate(store, root, declaration) -> list[str]`; without it none runs."""

from __future__ import annotations

from pathlib import Path
from typing import Any, Callable

from sldb.api.stores.apply_declaration import apply_includes, apply_links, apply_models, apply_predicates, missing_declared, undeclared
from sldb.api.stores.scaffold_store import scaffold_store
from sldb.api.stores.store_declaration import StoreDeclaration, declared_store, load_declaration
from sldb.api.stores.store_skeleton import write_empty_store
from sldb.api.stores.update_store_indexes import update_store_indexes
from sldb.store.layout import store_exists

Generate = Callable[[Path, Path, StoreDeclaration], list[str]]


def build_store(store: str | Path | None, *, apply: bool = True, generate: Generate | None = None) -> dict[str, Any]:
    """Apply the declaration to the store (created when absent) and report it.

    Args:
        store: The store (`.sldb` directory or its project) or None for the nearest declared one.
        apply: With it, the build; without it nothing is written: the write lists come back
            empty, `predicates_changed` false, and `scaffold`, `undeclared` and `missing` say
            what is pending.
        generate: Runs the declaration's generators, `(store, root, declaration) -> commands run`.

    Returns:
        `links`, `models`, `predicates_changed`, `tracked`, `generated`, `undeclared`,
        `missing` and `scaffold` (`created`, `rewritten`, `present`, `conflicts`).
    """
    store_path, root = declared_store(store)
    declaration = load_declaration(store_path)
    if not apply:
        return _planned(store_path, root, declaration)
    return _built(store_path, root, declaration, generate)


def _built(store_path: Path, root: Path, declaration: StoreDeclaration, generate: Generate | None) -> dict[str, Any]:
    if not store_exists(store_path):
        write_empty_store(store_path)
    report = {"links": apply_links(store_path, root, declaration), "models": apply_models(store_path, root, declaration)}
    report["predicates_changed"] = apply_predicates(store_path, declaration)
    report.update(_track(store_path, root, declaration, generate))
    update_store_indexes(store_path, str(root))
    report.update(_pending(store_path, root, declaration, apply=True))
    return report


def _track(store_path: Path, root: Path, declaration: StoreDeclaration, generate: Generate | None) -> dict[str, list[str]]:
    """Sources first (generators read them), then what the generators wrote."""
    tracked = apply_includes(store_path, root, declaration)
    generated = generate(store_path, root, declaration) if generate is not None else []
    return {"tracked": tracked + apply_includes(store_path, root, declaration), "generated": generated}


def _planned(store_path: Path, root: Path, declaration: StoreDeclaration) -> dict[str, Any]:
    report: dict[str, Any] = {"links": [], "models": [], "predicates_changed": False, "tracked": [], "generated": []}
    report.update(_pending(store_path, root, declaration, apply=False))
    return report


def _pending(store_path: Path, root: Path, declaration: StoreDeclaration, apply: bool) -> dict[str, Any]:
    missing = {"undeclared": undeclared(store_path, root, declaration) if store_exists(store_path) else [], "missing": missing_declared(root, declaration)}
    return {**missing, "scaffold": scaffold_store(store_path, apply=apply).lists()}
