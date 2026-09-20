"""`sldb journal`: read a store's write journal and verify its hash chain."""

from __future__ import annotations

import json
from datetime import datetime
from typing import Any

import yaml

from sldb.api.journal import journal as read_journal
from sldb.api.journal import verify_journal
from sldb.api.stores.open_store import open_store


class JournalCLI:
    """The write journal surface: show entries and verify the chain."""

    def run(self, args: Any) -> int:
        """Dispatch `journal show|verify`; verify exits 1 when the chain is broken."""
        return {"show": self._show, "verify": self._verify}[args.journal_command](args)

    def _show(self, args: Any) -> int:
        entries = read_journal(args.store, limit=args.limit, since=_since(args.since), address=args.address)
        payload = {"store": str(open_store(args.store, mode="readonly").store_path), "entries": [e.model_dump() for e in entries]}
        return _print(payload, args.format, _text_entries)

    def _verify(self, args: Any) -> int:
        report = verify_journal(args.store)
        _print(report.model_dump(), args.format, _text_verify)
        return 0 if report.valid else 1


def _print(payload: dict, fmt: str, text_fn) -> int:
    if fmt == "json":
        print(json.dumps(payload, indent=2, default=str))
    elif fmt == "yaml":
        print(yaml.safe_dump(_json_safe(payload), sort_keys=False, allow_unicode=True))
    else:
        print(text_fn(payload))
    return 0


def _json_safe(payload: dict) -> dict:
    return json.loads(json.dumps(payload, default=str))


def _since(value: str | None) -> datetime | None:
    return datetime.fromisoformat(value) if value else None


def _text_entries(payload: dict) -> str:
    entries = payload["entries"]
    if not entries:
        return f"No journal entries in {payload['store']}"
    return "\n".join(f"{e['timestamp']} {e['operation']} {e['address']}" for e in entries)


def _text_verify(payload: dict) -> str:
    return f"{'PASS' if payload['valid'] else 'FAIL'}: journal chain ({payload['entries']} entries)"
