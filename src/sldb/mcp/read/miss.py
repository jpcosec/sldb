"""A question about something the store does not have is not an error: it is a signal.

The read functions mark the answer with `signal` (a class of the closed catalog and the name
that was asked for); the server turns the mark into a log entry and suggestions."""

from __future__ import annotations

from typing import Any


def missing(signal_class: str, name: str, answer: dict[str, Any], candidates: list[str] | None = None) -> dict[str, Any]:
    """`answer` marked as an unmet request of `signal_class` for `name`, optionally with the
    names to suggest from (otherwise the server looks them up in the store by class)."""
    mark: dict[str, Any] = {"class": signal_class, "name": name}
    if candidates is not None:
        mark["candidates"] = candidates
    return {**answer, "signal": mark}
