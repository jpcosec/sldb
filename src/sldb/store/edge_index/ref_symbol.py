"""A bare symbol of a pron form, told apart from a quoted string."""

from __future__ import annotations


class RefSymbol(str):
    """A bare symbol read from a form (`model`, `Table`), as opposed to a "quoted string"."""
