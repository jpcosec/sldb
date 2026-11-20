"""How a store link is read: by its recorded path, and by the store's name when that path is not there.

A link is `{name, path}`. The name is the linked store's identity and is the same on every
machine; the path is where its repository happened to be when the link was recorded. So a
link is read in two steps: the recorded path (relative to the linking project's root, or
kept as written when typed as `/abs`, `~/x` or `$VAR/x`, with `~` and variables expanded
on every read), and, when no store is there, the store this machine's catalog knows under that name.
"""

from __future__ import annotations

import os
from pathlib import Path

KEPT_PREFIXES = ("/", "~", "$")


def kept_as_written(text: str) -> bool:
    """Whether `text` is a form that can be recorded as typed: absolute, home or variable."""
    return text.startswith(KEPT_PREFIXES)


def expand_link_path(text: str) -> str:
    """`text` with `~` and environment variables expanded; an unset variable stays as typed."""
    return os.path.expanduser(os.path.expandvars(text))


def resolve_link_path(root: Path, text: str) -> Path:
    """The absolute path a recorded link points to, read from the project root `root`."""
    path = Path(expand_link_path(text))
    return (path if path.is_absolute() else root / path).resolve()


def resolve_link(root: Path, name: str, text: str) -> Path:
    """Where the link `name` points on this machine.

    The recorded path when a store is there; else the store the machine's catalog (the global
    store) knows as `name`; else the recorded path, absent, for the caller to report.
    """
    from sldb.store.catalog import catalog_store
    from sldb.store.layout import store_exists

    recorded = resolve_link_path(root, text)
    if store_exists(recorded):
        return recorded
    known = catalog_store(name)
    return known if known is not None and known != (root / ".sldb").resolve() else recorded
