"""`code_facts`: the facts of a file, a directory or the whole tree, through `sldb.code.scan`."""

from __future__ import annotations

import os
from pathlib import Path
from typing import Any

from sldb.api.code.requested_files import requested_files
from sldb.code.ids import Ids
from sldb.code.runtime import GRAMMARS, available
from sldb.code.scan import scan_file


def code_facts(root: str | Path, paths: list[str] | None = None) -> dict[str, list]:
    """`{"facts": [...], "skipped": [...]}` for `paths` under `root` (the whole tree when `None`).

    Raises:
        ValueError: A path is absolute, outside `root` or missing (nothing is scanned).
        RuntimeError: A fact came without `span` or `source_hash` (a reader bug).
    """
    root = Path(root)
    files = requested_files(root, paths)
    readable = [rel for rel in files if _has_grammar(rel)]
    idgen = Ids()
    facts = idgen.flush([f for rel in readable for f in scan_file(rel, root, idgen)])
    for f in facts:
        _require_anchor(f)
    return {"facts": facts, "skipped": sorted(set(files) - set(readable), key=lambda r: tuple(r.split("/")))}


def _has_grammar(rel: str) -> bool:
    return os.path.splitext(rel)[1] in GRAMMARS and available(rel)


def _require_anchor(f: dict[str, Any]) -> None:
    if not f.get("span") or not f.get("source_hash"):
        raise RuntimeError(f"fact {f.get('id')} of {f.get('path')} has no span or source_hash: a bug of its reader")
