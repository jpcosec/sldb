"""The fields a document write changed, as dotted paths through two payloads.

`save_document_payload` receives the whole payload, so it cannot name the field it
changed without comparing the previous value against the new one. These helpers do
that comparison, nested keys included (`address.city`), so a journal entry can carry
the field it actually wrote.
"""

from __future__ import annotations

from typing import Any


def changed_paths(before: Any, after: Any) -> list[str]:
    """Dotted paths whose values differ between `before` and `after`.

    Dicts are compared recursively; a key removed or added appears as its own path,
    and a nested change appears as `parent.child`. Non-dict values compared unequal
    yield the empty string, which the caller turns into the root key.
    """
    if isinstance(before, dict) and isinstance(after, dict):
        paths: list[str] = []
        for key in sorted(set(before) | set(after)):
            for tail in changed_paths(before.get(key), after.get(key)):
                paths.append(f"{key}.{tail}" if tail else key)
        return paths
    if before == after:
        return []
    return [""]


def field_label(before: Any, after: Any) -> str | None:
    """The field a payload write changed: its dotted paths joined, or None when nothing did."""
    paths = changed_paths(before, after)
    return ", ".join(paths) if paths else None
