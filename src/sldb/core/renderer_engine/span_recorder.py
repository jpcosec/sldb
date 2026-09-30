"""Records where each marker wrote its value during a render.

The renderer is the only component that knows which characters of the output
came from which field, so spans are collected while rendering instead of being
re-parsed afterwards. Each recorded value is wrapped in private-use sentinels
(``U+E000 id U+E001 text U+E002``) that :mod:`sldb.core.segments.sentinel_decoder`
strips, turning the sentinels into character offsets over the canonical text.
"""

from __future__ import annotations

from contextlib import contextmanager
from typing import Any, Iterator

OPEN, SEP, CLOSE = "\ue000", "\ue001", "\ue002"


class SpanRecorder:
    """Collects marker metadata and wraps rendered values in sentinels."""

    def __init__(self) -> None:
        """Start an empty recorder with no list-item path prefix."""
        self.metas: list[dict[str, Any]] = []
        self.prefix: str = ""
        self.scalar_root: str | None = None

    def wrap(self, text: str, meta: dict[str, Any]) -> str:
        """Register ``meta`` and return ``text`` wrapped in sentinels.

        Args:
            text: The rendered surface of a value; may be empty.
            meta: Metadata for the span (path, marker kind, traits...).

        Returns:
            The sentinel-wrapped text carrying the new span id.
        """
        self.metas.append(meta)
        return f"{OPEN}{len(self.metas) - 1}{SEP}{text}{CLOSE}"

    def path_for(self, name: str) -> str:
        """Field path of ``name`` under the active list-item prefix.

        Args:
            name: The marker's property name.

        Returns:
            ``name`` at the root, ``root/i`` for a scalar item, else ``root/i/name``.
        """
        if not self.prefix:
            return name
        if self.scalar_root == name:
            return self.prefix
        return f"{self.prefix}/{name}"

    def meta_for(self, marker: Any) -> dict[str, Any]:
        """Span metadata for a parsed marker at the current prefix.

        Args:
            marker: A parsed ``Marker`` from ``sldb.core.handlers.utils``.

        Returns:
            A mapping with the field ``path``, the ``marker`` kind and its ``traits``.
        """
        return {"path": self.path_for(marker.name), "marker": marker.kind, "traits": list(marker.traits)}

    @contextmanager
    def item_scope(self, prefix: str, scalar_root: str | None) -> Iterator[None]:
        """Scope every path recorded inside to one list item.

        Args:
            prefix: Path of the item, such as ``steps/2``.
            scalar_root: Root property name when the item is a scalar, else None.

        Yields:
            None, with the prefix active for the duration of the block.
        """
        saved = (self.prefix, self.scalar_root)
        self.prefix, self.scalar_root = prefix, scalar_root
        try:
            yield
        finally:
            self.prefix, self.scalar_root = saved
