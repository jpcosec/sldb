"""`sldb stores build --check`: rebuild the store in a scratch copy of the sources and compare.

The copy holds what git versions (and untracked, unignored files), minus `.sldb/core/`,
`.sldb/runtime/` and the paths the declaration lists as `derived`;
linked stores are reached through symlinks so their relative paths still resolve. The check
fails when the build fails, the built store does not pass `stores check`, a tracked document
is not declared, or what the copy tracks (model, path, name) differs from the local store.
"""

from __future__ import annotations

import contextlib
import io
import shutil
import subprocess
import tempfile
from pathlib import Path
from typing import Any

from sldb.api.stores.declared_includes import tracked_rows
from sldb.api.stores.store_declaration import load_declaration
from sldb.cli.output_format import emit
from sldb.cli.store_context import get_store_context
from sldb.store.io import invalidate_index_cache
from sldb.store.layout import store_exists

ALWAYS_DERIVED = (".sldb/core/", ".sldb/runtime/")


def check_command(args: Any) -> int:
    store, root = get_store_context(args.store, mode="readonly")
    with tempfile.TemporaryDirectory(prefix="sldb-build-check-") as scratch:
        report = check_build(store, root, Path(scratch))
    emit(report, args.format, _summary(report))
    return 0 if report["ok"] else 1


def check_build(store: Path, root: Path, scratch: Path) -> dict[str, Any]:
    """Build a copy of the sources under `scratch` and compare it with the local store."""
    from sldb.cli.commands.stores_build import build_store

    copy = _prepared_copy(store, root, scratch / root.name)
    built_store = copy / store.relative_to(root)
    built = build_store(built_store, copy)
    integrity = _integrity(built_store)
    differences = _differences(store, root, built_store, copy) if store_exists(store) else []
    ok = integrity == 0 and not built["undeclared"] and not differences
    return {"ok": ok, "integrity_exit": integrity, "undeclared": built["undeclared"], "differences": differences}


def _prepared_copy(store: Path, root: Path, copy: Path) -> Path:
    """The sources copied without what is derived, with the linked stores reachable."""
    declaration = load_declaration(store)
    _copy_sources(root, copy, store, (*ALWAYS_DERIVED, *declaration.derived))
    _link_siblings(root, copy, declaration.links)
    return copy


def _integrity(store: Path) -> int:
    from sldb.cli.main import main

    with contextlib.redirect_stdout(io.StringIO()):
        return main(["stores", "check", "--store", str(store), "--quiet"])


def _copy_sources(root: Path, copy: Path, store: Path, derived: tuple[str, ...]) -> Path:
    listed = subprocess.run(["git", "ls-files", "--cached", "--others", "--exclude-standard", "-z"], cwd=root, capture_output=True, check=True).stdout
    for name in filter(None, listed.decode().split("\0")):
        if not name.startswith(derived) and (root / name).is_file():
            (copy / name).parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2(root / name, copy / name)
    (copy / store.relative_to(root)).mkdir(parents=True, exist_ok=True)
    return copy


def _link_siblings(root: Path, copy: Path, links: list[dict]) -> None:
    for link in links:
        project = (root / link["path"]).resolve().parent
        target = (copy / link["path"]).parent
        if not target.exists() and not Path(link["path"]).is_absolute():
            target.parent.mkdir(parents=True, exist_ok=True)
            target.symlink_to(project, target_is_directory=True)


def _differences(store: Path, root: Path, built_store: Path, copy: Path) -> list[str]:
    invalidate_index_cache()
    local = {(m, p, n) for m, p, n in tracked_rows(store, root)}
    rebuilt = {(m, p, n) for m, p, n in tracked_rows(built_store, copy)}
    return [f"only local: {r}" for r in sorted(local - rebuilt)] + [f"only rebuilt: {r}" for r in sorted(rebuilt - local)]


def _summary(report: dict[str, Any]) -> str:
    head = "PASS: the sources rebuild the store" if report["ok"] else "FAIL: the sources do not rebuild the store"
    lines = [head, f"  stores check exit: {report['integrity_exit']}"]
    lines += [f"  undeclared: {p}" for p in report["undeclared"]] + [f"  {d}" for d in report["differences"][:50]]
    return "\n".join(lines)
