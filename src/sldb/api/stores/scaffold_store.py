"""`scaffold_store`: the folders and seed files a store declares, created or restored
(`docs/architecture/store-declaration.md`). Idempotent: a run over a scaffolded store reports
everything as `present`. Writes go through `sldb.api.transaction`, so a failure halfway leaves
the project as it was."""

from __future__ import annotations

from pathlib import Path

from sldb.api.documents.transaction import Transaction, transaction
from sldb.api.stores.scaffold_report import ScaffoldReport
from sldb.api.stores.scaffold_sources import seed_bytes
from sldb.api.stores.seed import Seed
from sldb.api.stores.store_declaration import StoreDeclaration, declared_store, load_declaration
from sldb.core.exceptions import SLDBStoreError


def scaffold_store(store: str | Path | None, *, declaration: StoreDeclaration | None = None, apply: bool = False, template_root: str | Path | None = None) -> ScaffoldReport:
    """Create the declared folders and seed files, or report what a run with `apply` would do.

    Args:
        store: The store (`.sldb` directory or its project) or None for the nearest declared one.
        declaration: `folders` and `seeds` given in process, used instead of `store.yaml`'s
            and never written to it.
        apply: Write; without it nothing changes and the report says what would.
        template_root: Where a relative `file:` source is read from; the store directory by default.

    Returns:
        The paths created, rewritten, present or in conflict, and whether it was applied.

    Raises:
        SLDBStoreError: A folder or seed path outside the project root, or a source that cannot be read.
    """
    store_path, root = declared_store(store)
    wanted = declaration if declaration is not None else load_declaration(store_path)
    templates = Path(template_root) if template_root is not None else store_path
    report = ScaffoldReport(applied=apply)
    plan = _plan(wanted, store_path, root, templates)
    for outcome, _target, _seed, relative in plan:
        report.add(outcome, relative)
    if apply:
        _apply(store_path, root, templates, plan)
    return report


def _plan(wanted: StoreDeclaration, store_path: Path, root: Path, templates: Path) -> list[tuple[str, Path, Seed | None, str]]:
    """Folders first, then seeds, each with its outcome and resolved target."""
    folders = [(_folder_outcome(root, folder), root / folder, None, folder) for folder in wanted.folders]
    return folders + [_seed_plan(seed, store_path, root, templates) for seed in wanted.seeds]


def _seed_plan(seed: Seed, store_path: Path, root: Path, templates: Path) -> tuple[str, Path, Seed, str]:
    target = _inside(root, seed.path)
    data = seed_bytes(seed, store_path, root, templates)
    return _seed_outcome(seed, target, data, root), target, seed, seed.path


def _folder_outcome(root: Path, folder: str) -> str:
    target = _inside(root, folder)
    if target.is_dir():
        return "present"
    return "conflicts" if target.exists() or _blocked(root, target) else "created"


def _seed_outcome(seed: Seed, target: Path, data: bytes, root: Path) -> str:
    if target.is_dir() or _blocked(root, target):
        return "conflicts"
    if not target.exists():
        return "created"
    if seed.mode == "if_missing" or target.read_bytes() == data:
        return "present"
    return "rewritten"


def _blocked(root: Path, target: Path) -> bool:
    """An ancestor of `target` below `root` exists and is not a directory: nothing can go there."""
    return any(p.exists() and not p.is_dir() for p in target.parents if p != root.resolve() and p.is_relative_to(root.resolve()))


def _inside(root: Path, raw: str) -> Path:
    path = Path(raw)
    if path.is_absolute():
        raise SLDBStoreError(f"scaffold path {raw!r} must be relative to the project root")
    target = (root / path).resolve()
    if target == root.resolve() or not target.is_relative_to(root.resolve()):
        raise SLDBStoreError(f"scaffold path {raw!r} is outside the project root {root}")
    return target


def _apply(store_path: Path, root: Path, templates: Path, plan: list) -> None:
    with transaction(store_path, str(root)) as tx:
        for outcome, target, seed, _relative in plan:
            if outcome not in ("created", "rewritten"):
                continue
            if seed is None:
                target.mkdir(parents=True)
            else:
                _write_seed(tx, seed, target, seed_bytes(seed, store_path, root, templates), outcome)


def _write_seed(tx: Transaction, seed: Seed, target: Path, data: bytes, outcome: str) -> None:
    tx.write_file(target, data)
    if not seed.tracked:
        return
    if outcome == "rewritten":
        tx.untrack(seed.document["name"])
    tx.track(target, seed.document["model"], seed.document["name"])
