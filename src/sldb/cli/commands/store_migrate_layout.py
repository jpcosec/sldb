"""`sldb stores migrate-layout`: the CLI adapter over `sldb.api.stores.migrate_layout`."""

from __future__ import annotations

from typing import Any

from sldb.api.stores.migrate_layout import migrate_layout


def migrate_layout_command(args: Any) -> int:
    report = migrate_layout(args.store, force=args.force)
    print(_summary(report))
    return 0


def _summary(report: dict) -> str:
    moved = ", ".join(report["moved"]) or "nothing to move"
    lines = [f"{report['store']}: {moved} -> {report['cache']}"]
    if report["journal_removed"]:
        lines.append("journal removed (not archived: the store's past is read from git)")
    if report["runtime_removed"]:
        lines.append(f"{report['store']}/runtime removed")
    ignore = report["gitignore"]
    dropped = ", ".join(f"`{line.strip()}`" for line in ignore["removed"]) or "nothing"
    lines.append(f"{ignore['path']}: removed {dropped}; {'added' if ignore['added'] else 'already had'} `.sldb_cache/`")
    return "\n".join(lines)
