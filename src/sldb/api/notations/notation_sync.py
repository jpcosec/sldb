"""Synchronize visual palettes and notations to an SLDB store."""

from __future__ import annotations

from pathlib import Path

from sldb.api.notations.notation_parts import prune, sync_palette_of, write_notation
from sldb.api.notations.palette_sync import PaletteSync
from sldb.api.notations.store_writer import StoreWriter
from sldb.api.notations.sync_constants import _MANAGED_MODELS, MODEL_REFS, NOTATIONS_DIR, PALETTES_DIR, RELATION_TYPES_DIR
from sldb.api.notations.sync_report import SyncReport
from sldb.notations.notation import load_notation, notation_ref

_StoreWriter = StoreWriter


class NotationSync(StoreWriter):
    """Writes a notation (NotationDoc, GlyphDoc, LinkDoc and its PaletteDoc) to a store."""

    def sync(self, name_or_path: str | Path, *, finish: bool = True) -> SyncReport:
        """Upsert the notation and its palette, prune stale glyphs and links."""
        notation = load_notation(name_or_path)
        report = SyncReport(spec_id=notation.name, notation=notation_ref(notation.name))
        self.prepare()
        palette = sync_palette_of(self, notation, name_or_path, report)
        existing = self.existing_documents()
        current = write_notation(self, existing, report, notation, palette)
        prune(self, existing, report, notation, current)
        return self.finish(report) if finish else report


def sync_palette(store: Path | str, name_or_path: str | Path = "default", pythonpath: str | None = None, actor: str = "sldb") -> SyncReport:
    """Synchronize a palette into the store."""
    return PaletteSync(store, pythonpath, actor).sync(name_or_path)


def sync_notation(store: Path | str, name_or_path: str | Path, pythonpath: str | None = None, actor: str = "sldb") -> SyncReport:
    """Synchronize a notation and its palette into the store."""
    return NotationSync(store, pythonpath, actor).sync(name_or_path)


__all__ = ["SyncReport", "PaletteSync", "NotationSync", "sync_palette", "sync_notation"]
