"""Batch operations over tracked documents: `docs track --glob` and `stores update --prune-missing`."""
from __future__ import annotations
import glob
from pathlib import Path
from typing import Any
from sldb.api.documents.track_document_file import track_document_file
from sldb.api.documents.untrack_document import untrack_document
from sldb.cli.store_context import get_store_context
from sldb.core.exceptions import SLDBError
from sldb.links.tracked import tracked_documents

def _track_one(args: Any, path: str, failed: list[str]) -> bool:
    try: track_document_file(args.store, args.model, path, None, args.pythonpath, args.force)
    except SLDBError as exc: failed.append(f"{path}: {exc}"); return False
    return True

def track_glob(args: Any) -> int:
    """Track every file matching `args.glob`; the ones already tracked are skipped."""
    sp, root = get_store_context(args.store, mode="readonly")
    known = {p for _, p in tracked_documents(sp, root)}
    files = [f for f in sorted(glob.glob(args.glob, recursive=True)) if Path(f).is_file()]
    todo = [f for f in files if Path(f).resolve() not in known]
    failed: list[str] = []
    done = [f for f in todo if _track_one(args, f, failed)]
    print(f"Tracked {len(done)}, skipped {len(files) - len(todo)} already tracked, failed {len(failed)}")
    [print(f"  failed {line}") for line in failed]
    return 1 if failed else 0

def missing_documents(sp: Path, root: Path) -> list[str]:
    return [name for name, path in tracked_documents(sp, root) if not path.exists()]

def prune_missing(args: Any) -> list[str]:
    """Stop tracking the documents whose file no longer exists; returns their names."""
    sp, root = get_store_context(args.store)
    names = missing_documents(sp, root)
    [untrack_document(args.store, name, args.pythonpath) for name in names]
    return names
