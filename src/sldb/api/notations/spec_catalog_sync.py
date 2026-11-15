"""`sync_catalog`: sincroniza cada spec de un `vistas.yml` y reconcilia los SpecDoc del catalogo.

Migrado de `spec2viz.sldb_sync.sync_catalog`. Nuevo en sldb: los `SpecDoc` con metadatos de
catalogo (categoria, nav o resumen) que ya no lista el `vistas.yml` son huerfanos; con
`prune=True` se borran con sus nodos y aristas, sin el quedan como aviso en `unresolved`.
"""

from __future__ import annotations

from pathlib import Path
from typing import Any

from sldb.api.notations.spec_catalog import catalog_entries
from sldb.api.notations.spec_sync_steps import prune_spec, with_problems
from sldb.api.notations.sync_report import SyncReport

ORPHAN_PREFIX = "orphan SpecDoc:"


def _in_catalog(doc: Any) -> bool:
    payload = doc.payload or {}
    return any(payload.get(k) for k in ("category", "nav", "summary"))


def catalog_orphans(existing: dict, listed: set[str]) -> list[str]:
    """Los `SpecDoc` con metadatos de catalogo cuyo id no esta en `listed`."""
    return sorted(name for (model, name), doc in existing.items() if model == "SpecDoc" and name not in listed and _in_catalog(doc))


def _drop(sync: Any, existing: dict, report: SyncReport, name: str) -> None:
    """Borra el `SpecDoc` huerfano y sus `SpecNodeDoc` y `RelationDoc`."""
    prune_spec(sync, existing, report, name, set())
    sync.delete(existing, report, "SpecDoc", name)


def reconcile_catalog(sync: Any, config: Path, listed: set[str], prune: bool) -> SyncReport | None:
    """Un informe con los huerfanos del catalogo (borrados con `prune`), o None si no hay."""
    existing = sync.existing_documents()
    orphans = catalog_orphans(existing, listed)
    if not orphans:
        return None
    report = SyncReport(spec_id=f"catalog {Path(config).name}")
    if not prune:
        report.unresolved.extend(f"{ORPHAN_PREFIX}{name}: no longer listed in {Path(config).name}; pass --prune to delete it" for name in orphans)
        return with_problems(report)
    return with_problems(sync.finish(_drop_all(sync, existing, report, orphans)))


def _drop_all(sync: Any, existing: dict, report: SyncReport, orphans: list[str]) -> SyncReport:
    for name in orphans:
        _drop(sync, existing, report, name)
    return report


def sync_catalog(sync: Any, config: Path, prune: bool = False) -> list[SyncReport]:
    """Sincroniza cada spec de un `vistas.yml` con su notacion y sus metadatos de catalogo; si una
    ruta del registro no resuelve o es ambigua, no escribe nada y lanza ese error tipado."""
    entries = catalog_entries(config)
    for entry in entries:
        if entry["errors"]:
            raise entry["errors"][0]
    reports = [sync.sync(entry["spec"], notation=entry["notation"], catalog=entry["catalog"]) for entry in entries]
    orphans = reconcile_catalog(sync, config, {r.spec_id for r in reports}, prune)
    return reports + ([orphans] if orphans is not None else [])
