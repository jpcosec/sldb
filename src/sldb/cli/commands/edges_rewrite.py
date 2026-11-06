"""`sldb edges referrers TARGET` and `sldb edges rewrite TARGET --to NEW | --remove [--dry-run]`:
CLI adapters over `sldb.api.referrers` and `sldb.api.rewrite_references` (GD22).

With `--format json` the first prints the list of `Referrer` and the second the `RewriteReport`,
exactly the bodies `GET /edges/referrers` and `POST /edges/rewrite` answer; `--envelope` wraps
them in `data`. `--to` and `--remove` exclude each other and one is required (argparse: exit 2,
`cli/usage` in the envelope). A target that is unknown or ambiguous, or a payload the model
refuses, leaves every document as it was and exits through the envelope's typed error.
"""

from __future__ import annotations

from typing import Any

from sldb.api.edges.referrers import referrers
from sldb.api.edges.rewrite_references import rewrite_references
from sldb.cli.output_format import emit


def edges_referrers(args: Any) -> int:
    """Print every reference to `args.target`; 0 always."""
    found = [referrer.to_dict() for referrer in referrers(args.store, args.target, args.pythonpath)]
    emit(found, args.format, "\n".join(_referrer_line(item) for item in found) or f"No references to {args.target}")
    return 0


def edges_rewrite(args: Any) -> int:
    """Rewrite or remove every reference to `args.target` (or report it with `--dry-run`); 0 always."""
    report = rewrite_references(args.store, args.target, args.to, dry_run=args.dry_run, pythonpath=args.pythonpath).to_dict()
    lines = [_change_line(item) for item in report["changed"]] + [f"skipped {item['source']} ({item['location']}): {item['reason']}" for item in report["skipped"]]
    summary = f"{'would change' if args.dry_run else 'changed'} {len(report['changed'])} reference(s), skipped {len(report['skipped'])}"
    emit(report, args.format, "\n".join([*lines, summary]))
    return 0


def _referrer_line(item: dict[str, Any]) -> str:
    where = f"{item['location']}" if item["origin"] == "mention" else f"{item['source']} .{item['field']}" + ("" if item["index"] is None else f"[{item['index']}]")
    return f"{item['origin']}: {where}"


def _change_line(item: dict[str, Any]) -> str:
    where = item["location"] if item["location"] else f"{item['source']} .{item['field']}" + ("" if item["index"] is None else f"[{item['index']}]")
    return f"{where}: {item['before']!r} -> {item['after']!r}"
