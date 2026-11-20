"""Everything a move will do, worked out before anything is touched."""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Any

from sldb.api.documents.move_path_fields import planned_fields
from sldb.api.documents.move_path_files import markdown_files, moved_entries
from sldb.api.documents.move_path_links import rewrite_links
from sldb.api.documents.move_path_remap import Remap
from sldb.api.documents.move_path_report import MovePathReport
from sldb.api.documents.move_path_resolve import resolve_move
from sldb.api.documents.runtime_documents import load_runtime_documents
from sldb.api.stores.indexed_documents import indexed_documents
from sldb.api.stores.store_location import StoreLocation
from sldb.store.layout import cache_dir


@dataclass
class MovePlan:
    """The moves, the field rewrites `(document, payload, changes)`, the Markdown files whose
    links change `(file, changes)` and the tracked documents by path."""

    root: Path
    remap: Remap
    dirs: list[str]
    files: list[str]
    fields: list[tuple[Any, dict[str, Any], list[dict[str, Any]]]]
    links: list[tuple[str, list[dict[str, Any]]]]
    tracked: dict[str, dict[str, str]]

    def report(self, dry_run: bool) -> MovePathReport:
        """The plan as a `MovePathReport`."""
        moves = [{"source": f, "destination": self.remap.apply(f) or f} for f in self.files]
        return MovePathReport(source=self.remap.old, destination=self.remap.new, dry_run=dry_run, moves=moves, fields=[c for _, _, cs in self.fields for c in cs], links=[c for _, cs in self.links for c in cs])


def build_plan(location: StoreLocation, source: str | Path, destination: str | Path, pythonpath: str | None) -> MovePlan:
    """Check the move and gather what it rewrites; raises before anything is touched."""
    remap = resolve_move(location, source, destination)
    root = location.project_root.resolve()
    dirs, files = moved_entries(root, remap)
    docs = load_runtime_documents(location.store_path, pythonpath)
    tracked = {d["path"]: d for d in indexed_documents(location.store_path)}
    links = _links(root, remap, [location.store_path.resolve(), cache_dir(location.store_path).resolve()])
    return MovePlan(root, remap, dirs, files, planned_fields(docs, remap), links, tracked)


def _links(root: Path, remap: Remap, skip: list[Path]) -> list[tuple[str, list[dict[str, Any]]]]:
    found = []
    for file in markdown_files(root, skip):
        _, changes = rewrite_links(_text(root / file), file, remap)
        if changes:
            found.append((file, changes))
    return found


def _text(path: Path) -> str:
    try:
        return path.read_text(encoding="utf-8")
    except UnicodeDecodeError:
        return ""
