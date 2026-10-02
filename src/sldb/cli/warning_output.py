"""Route `sldb` library warnings to stderr, which is the CLI's job and not the library's.

`sldb.api` reports advisory conditions (the global-store fallback, for one) through
`logging` so an embedding application can decide where they go. The CLI is that
application for `python -m sldb`, and it wants them on stderr with the lowercase
`[warning]` prefix the surface has always printed.

The handler resolves `sys.stderr` on every record rather than binding it once: the
handler is installed once per process, but `sys.stderr` can be replaced afterwards (an
embedding app redirecting output, pytest's capture), and a bound stream would keep
writing to the stale one.
"""

from __future__ import annotations

import logging
import sys

_FORMAT = "[%(levelname)s] %(message)s"


class _StderrHandler(logging.StreamHandler):
    """A stream handler that looks up `sys.stderr` at emit time, not at construction."""

    _sldb_cli_warnings = True

    @property
    def stream(self):  # type: ignore[override]
        return sys.stderr

    @stream.setter
    def stream(self, value) -> None:
        """Ignore the base class assigning a bound stream in `__init__`."""

    def format(self, record: logging.LogRecord) -> str:
        record.levelname = record.levelname.lower()
        return super().format(record)


def install_warning_handler() -> None:
    """Send WARNING and above from the `sldb` logger to stderr, once per process."""
    logger = logging.getLogger("sldb")
    if any(getattr(handler, "_sldb_cli_warnings", False) for handler in logger.handlers):
        return
    handler = _StderrHandler()
    handler.setFormatter(logging.Formatter(_FORMAT))
    logger.addHandler(handler)
    if not logger.isEnabledFor(logging.WARNING):
        logger.setLevel(logging.WARNING)
