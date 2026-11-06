"""`sldb stores scaffold [--apply]`: the declared folders and seeds, planned or written
(`sldb.api.scaffold_store`). Exit 1 when a path is in conflict (held by the wrong kind of entry)."""

from __future__ import annotations

from typing import Any

from sldb.api.stores.scaffold_report import ScaffoldReport
from sldb.api.stores.scaffold_store import scaffold_store
from sldb.cli.output_format import emit


def scaffold_command(args: Any) -> int:
    report = scaffold_store(args.store, apply=args.apply)
    emit(report.model_dump(), args.format, _summary(report))
    return 1 if report.conflicts else 0


def _summary(report: ScaffoldReport) -> str:
    verb = "scaffolded" if report.applied else "scaffold pending"
    counts = ", ".join(f"{outcome}: {len(paths)}" for outcome, paths in report.lists().items())
    conflicts = f"\nconflicts: {', '.join(report.conflicts)}" if report.conflicts else ""
    return f"{verb}: {counts}{conflicts}"
