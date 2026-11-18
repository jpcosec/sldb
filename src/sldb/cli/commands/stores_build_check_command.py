"""`sldb stores build --check` as a command: where the scratch copy goes (a temporary directory, or
DIR with `--keep`), the report and its alerts. The check itself is `stores_build_check.check_build`.
"""

from __future__ import annotations

import sys
import tempfile
from pathlib import Path
from typing import Any

from sldb.api.stores.store_declaration import declared_store
from sldb.cli.commands.stores_build_check import copy_path, check_build
from sldb.cli.output_format import emit
from sldb.core.finding import Finding


def check_command(args: Any) -> int:
    store, root = declared_store(args.store)
    report = _checked_report(store, root, getattr(args, "keep", None))
    if report is None:
        return 2
    emit(report, args.format, _summary(report))
    _report_alerts(report, args.format)
    return 0 if report["ok"] else 1


def _checked_report(store: Path, root: Path, keep: str | None) -> dict[str, Any] | None:
    """`check_build` in a temporary directory, or in DIR with `--keep` (left there and named in
    the report as `kept`); None when DIR is not new or empty."""
    if not keep:
        with tempfile.TemporaryDirectory(prefix="sldb-build-check-") as tmp:
            return check_build(store, root, Path(tmp))
    scratch = _keep_directory(Path(keep))
    if scratch is None:
        return None
    return {**check_build(store, root, scratch), "kept": str(copy_path(root, scratch))}


def _keep_directory(keep: Path) -> Path | None:
    """`--keep DIR`: DIR must not exist or be empty (the copy stays there, pass or fail)."""
    keep = keep.resolve()
    if keep.exists() and (not keep.is_dir() or any(keep.iterdir())):
        print(f"Error: --keep {keep} is not empty (or not a directory); give a new or empty directory", file=sys.stderr)
        return None
    keep.mkdir(parents=True, exist_ok=True)
    return keep


def _report_alerts(report: dict, fmt: str) -> None:
    from sldb.cli import alert_sink

    alert_sink.report([Finding(**a) for a in report["alerts"]], text=fmt not in ("json", "yaml"))


def _summary(report: dict[str, Any]) -> str:
    head = "PASS: the sources rebuild the store" if report["ok"] else "FAIL: the sources do not rebuild the store"
    lines = [head, f"  stores check exit: {report['integrity_exit']}"] + ([f"  kept: {report['kept']}"] if report.get("kept") else []) + [f"  error: [{e['code']}] {e['subject']}: {e['what']}" for e in report["errors"]]
    lines += [f"  undeclared: {p}" for p in report["undeclared"]] + [f"  declared, no file: {p}" for p in report["missing"]]
    lines += [f"  {d}" for d in report["differences"][:50]]
    return "\n".join(lines)
