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

from sldb.api.stores.build_store import build_store as api_build_store
from sldb.api.stores.declare_store import declare_store
from sldb.api.stores.store_declaration import declared_store, save_declaration
from sldb.cli.commands.stores_build_generators import run_generators
from sldb.cli.commands.stores_link_alert import link_missing_what
from sldb.cli.output_format import emit
from sldb.cli.store_context import get_store_context


def declare_command(args: Any) -> int:
    store, root = get_store_context(args.store, mode="readonly")
    declaration = declare_store(store, root)
    if args.write:
        print(f"Wrote {save_declaration(store, declaration)}")
        return 0
    emit(declaration.model_dump(), "yaml", "")
    return 0


def build_store(store: Path, root: Path) -> dict[str, Any]:
    """`sldb.api.build_store` with the CLI's generators; `root` is the store's project
    (kept for the callers that pass it: `stores build --check`)."""
    return api_build_store(store, apply=True, generate=run_generators)


def build_command(args: Any) -> int:
    if args.check:
        from sldb.cli.commands.stores_build_check import check_command

        return check_command(args)
    store, root = declared_store(args.store)
    report = build_store(store, root)
    emit(report, args.format, _summary(report))
    return 1 if report["undeclared"] or report["missing"] or report["include_conflicts"] else 0


def _summary(report: dict[str, Any]) -> str:
    counts = ", ".join(f"{k}: {len(v)}" for k, v in report.items() if isinstance(v, list) and k not in ("links_missing", "include_conflicts"))
    flagged = "".join(f"\n{key}: " + ", ".join(report[key]) for key in ("undeclared", "missing") if report[key])
    absent = "".join(f"\nalert: [build/link-missing] {link['name']}: {link_missing_what(link)}" for link in report.get("links_missing", []))
    conflicts = "".join(f"\nerror: [{c['code']}] {c['subject']}: {c['what']}" for c in report["include_conflicts"])
    return f"built: {counts}{flagged}{conflicts}{absent}"
