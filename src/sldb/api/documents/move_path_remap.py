"""What a moved path becomes: the old and new project-relative paths, and whether it is a directory."""

from __future__ import annotations

from typing import NamedTuple


class Remap(NamedTuple):
    """`old` -> `new` (project-relative, POSIX, no trailing slash)."""

    old: str
    new: str
    is_dir: bool

    def apply(self, value: str) -> str | None:
        """`value` after the move: the new path when it is the old one, or under it for a
        directory (`old/` prefix, so `dirzero` is not `dir`); None when the move leaves it alone."""
        if value == self.old:
            return self.new
        if self.is_dir and value.startswith(self.old + "/"):
            return self.new + value[len(self.old):]
        return None
