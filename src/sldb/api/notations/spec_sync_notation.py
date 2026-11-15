"""La notacion de un spec durante su sincronizacion: se resuelve antes de tocar el store.

Migrado del cuerpo de `spec2viz.sldb_sync.SpecSync.sync`; reutiliza `NotationSync` de sldb.
"""

from __future__ import annotations

from pathlib import Path
from typing import Any

from sldb.api.notations.notation_sync import NotationSync
from sldb.api.notations.spec_notation import resolve_spec_notation
from sldb.api.notations.sync_report import SyncReport
from sldb.notations.notation import DEFAULT_NOTATIONS
from sldb.notations.notation_spec import NotationSpec

_MERGED = ("created", "updated", "deleted", "relation_types_added", "unresolved")


def _merge(report: SyncReport, sub: SyncReport) -> None:
    for attr in _MERGED:
        getattr(report, attr).extend(getattr(sub, attr))
    report.notation = sub.notation


def sync_spec_notation(writer: Any, spec: dict, notation: str | Path | None, report: SyncReport) -> None:
    """Resuelve la notacion (`None` = la del tipo, `"none"` = sin notacion), prepara el store y,
    si es builtin o YAML, la sincroniza; una que ya esta en el store no se reescribe."""
    diagram_type = str(spec.get("type") or "")
    chosen = DEFAULT_NOTATIONS.get(diagram_type) if notation is None else notation
    resolved = resolve_spec_notation(chosen, diagram_type, report.spec_id, writer.store_path, writer.pythonpath)
    writer.prepare()
    if isinstance(resolved, NotationSpec):
        _merge(report, NotationSync(writer.store_path, writer.pythonpath, writer.actor).sync(chosen, finish=False))
    elif resolved:
        report.notation = resolved
