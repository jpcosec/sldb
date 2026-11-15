"""The signal log: an append-only JSONL file in the store's cache.

It lives in `<project>/.sldb_cache/signals.jsonl` (`sldb.store.layout.cache_dir`), beside the
other derived files and ignored by git. It is not store state: no tracked document or linked
store is written, so a server at level 0 can log without breaking "reading writes nothing"."""

from __future__ import annotations

import json
import os
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

from sldb.store.layout import cache_dir


class SignalLog:
    """One JSON object per line: at, tool, arguments, signal_class, suggestions, actor."""

    def __init__(self, store_path: Path, actor: str | None = None) -> None:
        self.path = cache_dir(store_path) / "signals.jsonl"
        self.actor = actor

    def append(self, tool: str, arguments: dict[str, Any], signal_class: str, suggestions: list[str]) -> dict[str, Any]:
        """Record one signal with a single `O_APPEND` write and return the entry."""
        at = datetime.now(timezone.utc).isoformat(timespec="milliseconds").replace("+00:00", "Z")
        entry = {"at": at, "tool": tool, "arguments": arguments, "signal_class": signal_class, "suggestions": suggestions, "actor": self.actor}
        self.path.parent.mkdir(parents=True, exist_ok=True)
        fd = os.open(self.path, os.O_WRONLY | os.O_APPEND | os.O_CREAT, 0o644)
        try:
            os.write(fd, (json.dumps(entry, ensure_ascii=False, default=str) + "\n").encode("utf-8"))
        finally:
            os.close(fd)
        return entry

    def entries(self) -> list[dict[str, Any]]:
        """Every entry, oldest first; a missing file is an empty log and a torn line is skipped."""
        if not self.path.is_file():
            return []
        lines = self.path.read_text(encoding="utf-8").splitlines()
        return [entry for entry in map(_parsed, lines) if entry is not None]


def _parsed(line: str) -> dict[str, Any] | None:
    try:
        entry = json.loads(line)
    except ValueError:
        return None
    return entry if isinstance(entry, dict) else None
