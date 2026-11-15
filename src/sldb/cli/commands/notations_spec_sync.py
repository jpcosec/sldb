"""`sldb notations sync --spec/--catalog`: reconcilia specs de diagrama y un `vistas.yml` con el store.

Migrado de `spec2viz diagram sync`, `spec2viz catalog sync` y `spec2viz catalog validate`
(`--check`). El informe es el de `format_report` (una linea por spec); con `--json`, la lista de
`SyncReport.to_dict()`. Los avisos salen tambien como findings por stderr.
"""

from __future__ import annotations

import json
import sys
from pathlib import Path
from typing import Any

from sldb.api.notations import SpecSync, check_catalog, find_store, format_report, load_spec, report_findings, sync_catalog
from sldb.cli.alert_sink import report


def is_spec_sync(args: Any) -> bool:
    """Si el sync es de specs o de un catalogo (y no de una notacion o paleta sola)."""
    return bool(getattr(args, "spec", None) or getattr(args, "catalog", None))


def spec_sync(args: Any) -> int:
    """`--spec` (uno o varios), `--catalog` o `--catalog --check`."""
    if args.spec and args.catalog or args.palette:
        raise SystemExit("--spec and --catalog are separate syncs, and --palette syncs on its own")
    if args.catalog and args.notation:
        raise SystemExit("--notation applies to --spec; a vistas.yml names each view's notation")
    if args.check:
        return _check(args) if args.catalog else _fail("--check validates a --catalog")
    return _catalog(args) if args.catalog else _specs(args)


def _fail(message: str) -> int:
    print(f"Error: {message}", file=sys.stderr)
    return 1


def _store(args: Any, start: Path) -> Path | None:
    return Path(args.store) if args.store else find_store(start.resolve().parent)


def _specs(args: Any) -> int:
    store = _store(args, Path(args.spec[0]))
    if store is None:
        return _fail("no `.sldb` store found above the spec; pass --store.")
    sync = SpecSync(store, pythonpath=args.pythonpath, validate=load_spec)
    try:
        reports = [sync.sync(path, notation=args.notation) for path in args.spec]
    except Exception as exc:
        return _fail(f"syncing specs: {type(exc).__name__}: {exc}")
    return _emit(args, reports)


def _invalid(entry: dict, exc: Exception) -> None:
    print(f"Invalid: {entry['vista'] or entry['spec']}: {type(exc).__name__}: {exc}", file=sys.stderr)


def _catalog(args: Any) -> int:
    store = _store(args, Path(args.catalog))
    if store is None:
        return _fail("no `.sldb` store found above the config; pass --store.")
    if not _catalog_ok(args, store):
        return 1
    try:
        reports = sync_catalog(SpecSync(store, pythonpath=args.pythonpath, validate=load_spec), Path(args.catalog), prune=args.prune)
    except Exception as exc:
        return _fail(f"syncing catalog: {type(exc).__name__}: {exc}")
    return _emit(args, reports)


def _catalog_ok(args: Any, store: Path) -> bool:
    """Todo o nada: una ruta, spec o notacion invalida frena el sync antes de escribir (el `src` no)."""
    problems = [(entry, exc) for entry, exc in check_catalog(Path(args.catalog), store, args.pythonpath, include_src=False) if exc]
    for entry, exc in problems:
        _invalid(entry, exc)
    return not problems


def _check(args: Any) -> int:
    """Valida el catalogo sin escribir: una linea `Valid:` o `Invalid:` por spec."""
    store = _store(args, Path(args.catalog))
    results = check_catalog(Path(args.catalog), store, args.pythonpath)
    for entry, exc in results:
        if exc is not None:
            _invalid(entry, exc)
            continue
        notation = f" (notation {entry['notation']})" if entry["notation"] else ""
        print(f"Valid: {entry['vista'] or entry['spec']}: {Path(entry['spec']).name}{notation}")
    return 1 if any(exc is not None for _, exc in results) else 0


def _emit(args: Any, reports: list) -> int:
    if args.json:
        print(json.dumps([r.to_dict() for r in reports], indent=2, ensure_ascii=False))
    else:
        print("\n".join(format_report(r) for r in reports))
    findings = [f for r in reports for f in report_findings(r)]
    report(findings, text=False)
    for finding in findings:
        print(finding.line() + (f"\n    fix     : {finding.fix}" if finding.fix else ""), file=sys.stderr)
    return 1 if args.strict and findings else 0
