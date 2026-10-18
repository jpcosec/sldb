"""Imports a later binding shadows in the same scope (spec section 4.1).

`from a import X` followed, in the same scope, by `def X(...)`, `class X` or `X = ...`
leaves the name bound to the later definition: a reference after it does not reach the
import. Such a binding is marked `shadowed_at` (the line of the rebinding), and reference
resolution skips it from that line on instead of claiming the import.
"""

from __future__ import annotations


def mark_shadowed(file: dict) -> None:
    """Add `shadowed_at` to every import binding of `file` that a later same-scope binding rebinds."""
    rebinds = [(s["parent"], s["name"], s["line"]) for s in file["symbols"]] + [(r["owner"], r["name"], r["line"]) for r in file.get("rebinds", [])]
    for binding in file["imports"]:
        later = [line for owner, name, line in rebinds if owner == binding["owner"] and name == binding["local"] and line > binding["line"]]
        if later:
            binding["shadowed_at"] = min(later)


def active(binding: dict, line: int) -> bool:
    """Whether the import still binds its name at `line` (it did not happen after, and was not shadowed before)."""
    return binding["line"] <= line and line < binding.get("shadowed_at", float("inf"))
