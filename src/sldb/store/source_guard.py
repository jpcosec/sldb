"""How a surface opens a tracked document through the read guard (SEGURIDAD resto 2).

`source_read` decides whether a tracked path may be read; this module gives each kind of
surface its one way to act on that verdict, with the finding codes `stores check` gives it
(`store/path-outside-root`, `store/symlink-not-read`):

- a command whose argument names ONE document fails with `SLDBDocumentTargetError` (exit 1);
- an aggregate surface (edges, records, segments, the project graph) logs it as a warning and
  goes on without the document;
- a write opens with `O_NOFOLLOW`, so a symlink swapped in after the check is not followed.
"""

from __future__ import annotations

import errno
import logging
import os
from pathlib import Path

from sldb.store.exceptions import SLDBDocumentTargetError
from sldb.store.source_read import OUTSIDE_ROOT, SYMLINK, read_source_text, unreadable_reason

logger = logging.getLogger(__name__)

#: The finding code of each `unreadable_reason` (the same `stores check` reports).
READ_CODES = {OUTSIDE_ROOT: "store/path-outside-root", SYMLINK: "store/symlink-not-read"}
_WHY = {OUTSIDE_ROOT: "the path resolves outside the project root", SYMLINK: "the path is a symlink"}
_NOFOLLOW = getattr(os, "O_NOFOLLOW", 0)


def unread_line(root: Path, path: Path, subject: str) -> str | None:
    """`[code] subject: why; not read`, or None when `path` may be read. Names the tracked path
    only by `subject`: where a symlink points is never printed."""
    if (reason := unreadable_reason(root, path)) is None:
        return None
    return f"[{READ_CODES[reason]}] {subject}: {_WHY[reason]}; sldb does not read it"


def refuse_unread(root: Path, path: Path, subject: str) -> None:
    """`SLDBDocumentTargetError` naming the finding when `path` must not be read nor written."""
    if (line := unread_line(root, path, subject)) is not None:
        raise SLDBDocumentTargetError(line)


def target_text(root: Path, path: Path, subject: str) -> str:
    """The text of the ONE document a command names; `SLDBDocumentTargetError` when it must not be read."""
    refuse_unread(root, path, subject)
    return read_source_text(path)


def aggregate_text(root: Path, path: Path, subject: str) -> str | None:
    """The text of one document of many, or None (warned with its finding) when it must not be read."""
    if (line := unread_line(root, path, subject)) is not None:
        logger.warning(line)
        return None
    return read_source_text(path)


def target_write(root: Path, path: Path, text: str, subject: str) -> None:
    """Write the ONE document a command names; `SLDBDocumentTargetError` when it must not be
    read (nor written): outside the root, or a symlink (checked, and again by `O_NOFOLLOW`)."""
    refuse_unread(root, path, subject)
    write_source_text(path, text)


def write_source_text(path: Path, text: str) -> None:
    """Write `text` (UTF-8) to `path`, see `write_source_bytes`."""
    write_source_bytes(path, text.encode("utf-8"))


def write_source_bytes(path: Path, data: bytes) -> None:
    """Write `data` to `path` without following a symlink in its last component (`O_NOFOLLOW`):
    one there, even one swapped in after a check, fails as `store/symlink-not-read`, nothing written."""
    with open(_open_nofollow(path, os.O_WRONLY | os.O_CREAT | os.O_TRUNC, "write"), "wb") as f:
        f.write(data)


def read_source_bytes(path: Path) -> bytes:
    """The file's bytes, opened with `O_NOFOLLOW` (see `write_source_bytes`)."""
    with open(_open_nofollow(path, os.O_RDONLY, "read"), "rb") as f:
        return f.read()


def _open_nofollow(path: Path, flags: int, verb: str) -> int:
    try:
        return os.open(path, flags | _NOFOLLOW, 0o644)
    except OSError as exc:
        if exc.errno != errno.ELOOP:
            raise
        raise SLDBDocumentTargetError(f"[{READ_CODES[SYMLINK]}] {path.name}: {_WHY[SYMLINK]}; sldb does not {verb} it") from exc
