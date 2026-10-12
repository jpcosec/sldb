"""`sldb predicates export/sync`: keep predicate definitions in a versioned YAML file (name -> {axis, description})."""
from __future__ import annotations
import sys
from pathlib import Path
from typing import Any
import yaml
from sldb.cli.store_context import get_store_context
from sldb.core.exceptions import SLDBStoreError
from sldb.store.io import load_store_index, save_store_index
from sldb.store.models import PredicateEntry
from sldb.store.predicates import validate_predicates

def to_mapping(entries: list[PredicateEntry]) -> dict[str, dict[str, str]]:
    return {e.name: {"axis": e.axis, "description": e.description} for e in sorted(entries, key=lambda e: e.name)}

def _read(path: str) -> dict[str, Any]:
    data = yaml.safe_load(sys.stdin if path == "-" else Path(path).read_text("utf-8")) or {}
    if not isinstance(data, dict): raise SLDBStoreError("The predicates file must map name -> {axis, description}.")
    return data

def _entries(data: dict[str, Any]) -> list[PredicateEntry]:
    return [PredicateEntry(name=n, axis=str((v or {}).get("axis", "")).upper(), description=str((v or {}).get("description", ""))) for n, v in data.items()]

def plan_sync(current: list[PredicateEntry], wanted: list[PredicateEntry], prune: bool) -> tuple[list[PredicateEntry], dict[str, list[str]]]:
    cur, want = {e.name: e for e in current}, {e.name: e for e in wanted}
    rep = {"created": [n for n in want if n not in cur], "updated": [n for n in want if n in cur and cur[n] != want[n]], "removed": [n for n in cur if prune and n not in want]}
    keep = [e for n, e in cur.items() if n not in want and n not in rep["removed"]]
    return keep + list(want.values()), rep

def export_command(args: Any) -> int:
    sp, _ = get_store_context(args.store, mode="readonly")
    text = yaml.safe_dump(to_mapping(load_store_index(sp).predicates), sort_keys=False, allow_unicode=True)
    if args.file == "-": print(text, end="")
    else: Path(args.file).write_text(text, "utf-8"); print(f"Exported predicates to {args.file}")
    return 0

def sync_command(args: Any) -> int:
    sp, _ = get_store_context(args.store)
    wanted, idx = _entries(_read(args.file)), load_store_index(sp)
    if errs := validate_predicates(wanted): raise SLDBStoreError(" ".join(errs))
    idx.predicates, rep = plan_sync(idx.predicates, wanted, args.prune)
    if any(rep.values()): save_store_index(sp, idx)
    print("; ".join(f"{k}: {', '.join(v) or '-'}" for k, v in rep.items()))
    return 0
