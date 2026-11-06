"""Writes a palette (PaletteDoc) to a store."""

from __future__ import annotations

from pathlib import Path

from sldb.api.notations.notation_payloads import palette_payload
from sldb.api.notations.store_writer import StoreWriter
from sldb.api.notations.sync_constants import PALETTES_DIR
from sldb.api.notations.sync_report import SyncReport
from sldb.notations.palette import load_palette, palette_ref


class PaletteSync(StoreWriter):
    """Writes a palette (PaletteDoc) to a store."""

    def sync(self, name_or_path: str | Path = "default", *, base: Path | None = None, finish: bool = True) -> SyncReport:
        """Upsert the palette; rebuild edges unless `finish` is false."""
        palette = load_palette(name_or_path, base)
        report = SyncReport(spec_id=palette.name)
        self.prepare()
        existing = self.existing_documents()
        path = self.root / PALETTES_DIR / f"{palette.name}.md"
        self.upsert(existing, report, "PaletteDoc", palette.name, path, palette_payload(palette))
        report.notation = palette_ref(palette.name)
        return self.finish(report) if finish else report
