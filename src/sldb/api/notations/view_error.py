"""The error raised when the store lacks what the notation contract needs."""

from __future__ import annotations


class ViewError(ValueError):
    """The store does not have what the notation contract needs (spec, notation, glyphs)."""
