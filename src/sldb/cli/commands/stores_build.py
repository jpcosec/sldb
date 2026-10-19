"""`sldb stores declare` and `sldb stores build`: the store rebuilt from what it declares.

`declare` writes `.sldb/store.yaml` from the current index (once, to adopt the layout). `build`
makes the store match the declaration: links, models, predicates, generators (such as
`selfdoc python-sync`), the tracked files, then the indexes. `build --check` does it in a
scratch copy of the sources and fails when that copy is not a valid store, or when what it
tracks differs from the local store.
"""

from __future__ import annotations

from pathlib import Path
from typing import Any

from sldb.api.stores.apply_declaration import apply_includes, apply_links, apply_models, apply_predicates, undeclared
from sldb.api.stores.declare_store import declare_store
from sldb.api.stores.store_declaration import load_declaration, save_declaration
from sldb.api.stores.store_skeleton import write_empty_store
from sldb.api.stores.update_store_indexes import update_store_indexes
from sldb.cli.output_format import emit
from sldb.cli.store_context import get_store_context
from sldb.store.layout import store_exists


def declare_command(args: Any) -> int:
    store, root = get_store_context(args.store, mode="readonly")
    declaration = declare_store(store, root)
    if args.write:
        print(f"Wrote {save_declaration(store, declaration)}")
        return 0
    emit(declaration.model_dump(), "yaml", "")
    return 0


def build_store(store: Path, root: Path) -> dict[str, Any]:
    """Apply the declaration to the store at `store` (created when absent) and report it."""
    declaration = load_declaration(store)
    if not store_exists(store):
        write_empty_store(store)
    report = {"links": apply_links(store, root, declaration), "models": apply_models(store, root, declaration)}
    report["predicates_changed"] = apply_predicates(store, declaration)
    report.update(_track(store, root, declaration))
    update_store_indexes(store, str(root))
    report["undeclared"] = undeclared(store, root, declaration)
    return report


def _track(store: Path, root: Path, declaration) -> dict[str, list[str]]:
    """Sources first (generators read them), then what the generators wrote."""
    from sldb.cli.commands.stores_build_generators import run_generators

    tracked = apply_includes(store, root, declaration)
    generated = run_generators(store, root, declaration)
    return {"tracked": tracked + apply_includes(store, root, declaration), "generated": generated}


def build_command(args: Any) -> int:
    if args.check:
        from sldb.cli.commands.stores_build_check import check_command

        return check_command(args)
    store, root = get_store_context(args.store)
    report = build_store(store, root)
    emit(report, args.format, _summary(report))
    return 1 if report["undeclared"] else 0


def _summary(report: dict[str, Any]) -> str:
    counts = ", ".join(f"{k}: {len(v)}" for k, v in report.items() if isinstance(v, list))
    flagged = "" if not report["undeclared"] else "\nundeclared (tracked, but no include rule names them): " + ", ".join(report["undeclared"])
    return f"built: {counts}{flagged}"
