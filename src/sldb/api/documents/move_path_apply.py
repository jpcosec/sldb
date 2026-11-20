"""Carry a `MovePlan` out inside a transaction: fields, then links, then the files themselves."""

from __future__ import annotations

from pathlib import Path

from sldb.api.documents.move_path_links import rewrite_links
from sldb.api.documents.move_path_plan import MovePlan
from sldb.api.documents.relocate_file import relocate_file
from sldb.api.documents.transaction import Transaction


def apply_plan(tx: Transaction, plan: MovePlan) -> None:
    """Write the plan; a failure restores the moved files here and, on the way out, the transaction restores the store."""
    for doc, payload, _ in plan.fields:
        tx.update(doc.path, payload)
    for file, _ in plan.links:
        _relink(tx, plan, file)
    _move_files(tx, plan)


def _relink(tx: Transaction, plan: MovePlan, file: str) -> None:
    path = plan.root / file
    text = path.read_text(encoding="utf-8")  # re-read: a field rewrite may have rewritten this very document
    new, _ = rewrite_links(text, file, plan.remap)
    doc = plan.tracked.get(file)
    if doc is not None:
        tx.untrack(file)
    tx.write_file(path, new.encode("utf-8"))
    if doc is not None:
        tx.track(path, doc["model"], doc["name"])


def _move_files(tx: Transaction, plan: MovePlan) -> None:
    done: list[tuple[str, str]] = []
    try:
        _run_moves(tx, plan, done)
    except BaseException:
        _undo(plan, done)
        raise


def _run_moves(tx: Transaction, plan: MovePlan, done: list[tuple[str, str]]) -> None:
    for d in plan.dirs:
        (plan.root / (plan.remap.apply(d) or d)).mkdir(parents=True, exist_ok=True)
    for old in plan.files:
        done.append((old, plan.remap.apply(old) or old))
        _move_one(tx, plan, *done[-1])
    _drop_empty(plan)


def _move_one(tx: Transaction, plan: MovePlan, old: str, new: str) -> None:
    if old in plan.tracked:
        tx.move(old, new)
    else:
        relocate_file(plan.root / old, plan.root / new)


def _drop_empty(plan: MovePlan) -> None:
    for d in reversed(plan.dirs):
        _rmdir(plan.root / d)


def _undo(plan: MovePlan, done: list[tuple[str, str]]) -> None:
    for old, new in reversed(done):
        here, back = plan.root / new, plan.root / old
        if (here.exists() or here.is_symlink()) and not (back.exists() or back.is_symlink()):
            relocate_file(here, back)
    for d in reversed(plan.dirs):
        _rmdir(plan.root / (plan.remap.apply(d) or d))
    _prune(plan.root, (plan.root / plan.remap.new).parent)


def _prune(root: Path, path: Path) -> None:
    while path != root and _rmdir(path):
        path = path.parent


def _rmdir(path: Path) -> bool:
    try:
        path.rmdir()
        return True
    except OSError:
        return False
